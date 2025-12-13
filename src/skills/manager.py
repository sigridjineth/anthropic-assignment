import argparse
import sys
from pathlib import Path
import anthropic
from anthropic.lib import files_from_dir

from ..config import get_settings
from ..models import SkillDomain
from .registry import SkillRegistry

SKILLS_DIR = Path(__file__).resolve().parent.parent.parent / "skills"


class SkillManager:
    """Manages skill upload and lifecycle."""

    def __init__(self):
        settings = get_settings()
        self.client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
        self.registry = SkillRegistry()
        self.skills_beta = settings.skills_beta

    def upload_skill(self, domain: SkillDomain, force: bool = False) -> str:
        """Upload a skill to Claude and register it."""
        skill_dir = SKILLS_DIR / domain.value

        if not skill_dir.exists():
            raise FileNotFoundError(f"Skill directory not found: {skill_dir}")

        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            raise FileNotFoundError(f"SKILL.md not found in {skill_dir}")

        # Check if already registered
        if self.registry.is_registered(domain) and not force:
            existing_id = self.registry.get_skill_id(domain)
            print(f"Skill '{domain.value}' already registered: {existing_id}")
            return existing_id

        # Read SKILL.md to get display title
        with open(skill_md) as f:
            content = f.read()
            # Extract name from YAML frontmatter
            if content.startswith("---"):
                import yaml
                end_idx = content.index("---", 3)
                frontmatter = yaml.safe_load(content[3:end_idx])
                display_title = frontmatter.get("name", domain.value).replace("-", " ").title()
            else:
                display_title = domain.value.replace("_", " ").title()

        # Upload skill
        print(f"Uploading skill '{domain.value}'...")
        skill = self.client.beta.skills.create(
            display_title=display_title,
            files=files_from_dir(str(skill_dir)),
            betas=[self.skills_beta],
        )

        # Register the skill ID
        self.registry.register(domain, skill.id)
        print(f"Registered skill '{domain.value}': {skill.id}")

        return skill.id

    def upload_all(self, force: bool = False) -> dict[str, str]:
        """Upload all skills from the skills directory."""
        results = {}

        for domain in SkillDomain:
            skill_dir = SKILLS_DIR / domain.value
            if skill_dir.exists() and (skill_dir / "SKILL.md").exists():
                try:
                    skill_id = self.upload_skill(domain, force=force)
                    results[domain.value] = skill_id
                except Exception as e:
                    print(f"Failed to upload {domain.value}: {e}")
                    results[domain.value] = f"ERROR: {e}"

        return results

    def list_skills(self) -> None:
        """List all registered skills."""
        mapping = self.registry.get_all()

        if not mapping:
            print("No skills registered. Run 'skills upload' first.")
            return

        print("\nRegistered Skills:")
        print("-" * 60)
        for domain, skill_id in mapping.items():
            print(f"  {domain:20} -> {skill_id}")
        print("-" * 60)

    def list_remote_skills(self) -> None:
        """List skills from Claude API."""
        print("\nRemote Skills (from Claude API):")
        print("-" * 60)

        try:
            skills = self.client.beta.skills.list(
                source="custom",
                betas=[self.skills_beta],
            )
            for skill in skills.data:
                print(f"  {skill.display_title:20} -> {skill.id}")
        except Exception as e:
            print(f"Error listing skills: {e}")

        print("-" * 60)

    def delete_skill(self, domain: SkillDomain) -> None:
        """Delete a skill from Claude."""
        skill_id = self.registry.get_skill_id(domain)
        if not skill_id:
            print(f"Skill '{domain.value}' not registered locally.")
            return

        try:
            # First delete all versions
            versions = self.client.beta.skills.versions.list(
                skill_id=skill_id,
                betas=[self.skills_beta],
            )
            for version in versions.data:
                self.client.beta.skills.versions.delete(
                    skill_id=skill_id,
                    version=version.version,
                    betas=[self.skills_beta],
                )

            # Then delete the skill
            self.client.beta.skills.delete(
                skill_id=skill_id,
                betas=[self.skills_beta],
            )
            print(f"Deleted skill '{domain.value}': {skill_id}")

            # Remove from registry
            self.registry._mapping.pop(domain.value, None)
            self.registry._save()

        except Exception as e:
            print(f"Error deleting skill: {e}")


def cli():
    parser = argparse.ArgumentParser(description="Manage Claude Skills")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Upload command
    upload_parser = subparsers.add_parser("upload", help="Upload skills")
    upload_parser.add_argument(
        "--domain",
        type=str,
        choices=[d.value for d in SkillDomain],
        help="Specific domain to upload (uploads all if not specified)",
    )
    upload_parser.add_argument(
        "--force",
        action="store_true",
        help="Force re-upload even if already registered",
    )

    # List command
    subparsers.add_parser("list", help="List registered skills")
    subparsers.add_parser("list-remote", help="List skills from Claude API")

    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a skill")
    delete_parser.add_argument(
        "domain",
        type=str,
        choices=[d.value for d in SkillDomain],
        help="Domain to delete",
    )

    args = parser.parse_args()
    manager = SkillManager()

    if args.command == "upload":
        if args.domain:
            manager.upload_skill(SkillDomain(args.domain), force=args.force)
        else:
            manager.upload_all(force=args.force)

    elif args.command == "list":
        manager.list_skills()

    elif args.command == "list-remote":
        manager.list_remote_skills()

    elif args.command == "delete":
        manager.delete_skill(SkillDomain(args.domain))

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    cli()
