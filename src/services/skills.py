"""
Skill Manager - Manages skills via the official Claude Skills API.

This module handles:
1. Uploading custom skills to Anthropic
2. Tracking skill_ids for each domain
3. Providing skill configurations for container.skills parameter

See: https://platform.claude.com/docs/en/build-with-claude/skills-guide
"""

import asyncio
from pathlib import Path
from dataclasses import dataclass, field
import anthropic
from ..config import get_settings
from ..models import SkillDomain

SKILLS_DIR = Path(__file__).resolve().parent.parent.parent / "skills"

# Beta feature identifiers
BETAS = ["code-execution-2025-08-25", "skills-2025-10-02"]


@dataclass
class SkillInfo:
    """Information about an uploaded skill."""
    domain: SkillDomain
    skill_id: str
    version: str
    display_title: str


@dataclass
class SkillManager:
    """Manages custom skills via the official Skills API."""

    _skills: dict[SkillDomain, SkillInfo] = field(default_factory=dict)
    _initialized: bool = False
    _client: anthropic.Anthropic | None = None

    def __post_init__(self):
        settings = get_settings()
        self._client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

    async def initialize(self) -> None:
        """Upload all skills to Anthropic and store their IDs."""
        if self._initialized:
            return

        # Upload each skill domain
        for domain in SkillDomain:
            skill_dir = SKILLS_DIR / domain.value
            if not skill_dir.exists():
                continue

            try:
                skill_info = await self._upload_skill(domain, skill_dir)
                if skill_info:
                    self._skills[domain] = skill_info
            except Exception as e:
                # Log error but continue with other skills
                print(f"Warning: Failed to upload skill {domain.value}: {e}")

        self._initialized = True

    async def _upload_skill(self, domain: SkillDomain, skill_dir: Path) -> SkillInfo | None:
        """Upload a single skill to Anthropic."""
        # Check for existing skill first to avoid re-uploading
        existing = await self._find_existing_skill(domain)
        if existing:
            return existing

        # Prepare files for upload
        files = []

        # Add SKILL.md (required)
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            return None

        # Use the domain name as the directory prefix
        dir_name = f"{domain.value}_skill"
        files.append((f"{dir_name}/SKILL.md", skill_md.read_bytes(), "text/markdown"))

        # Add reference files
        refs_dir = skill_dir / "references"
        if refs_dir.exists():
            for ref_file in refs_dir.glob("*.md"):
                files.append((
                    f"{dir_name}/references/{ref_file.name}",
                    ref_file.read_bytes(),
                    "text/markdown"
                ))

        # Upload via Skills API
        display_title = f"Sales Copilot - {domain.value.title()}"

        skill = self._client.beta.skills.create(
            display_title=display_title,
            files=files,
            betas=BETAS
        )

        return SkillInfo(
            domain=domain,
            skill_id=skill.id,
            version=skill.latest_version,
            display_title=display_title
        )

    async def _find_existing_skill(self, domain: SkillDomain) -> SkillInfo | None:
        """Check if skill already exists in our workspace."""
        try:
            skills = self._client.beta.skills.list(
                source="custom",
                betas=BETAS
            )

            target_title = f"Sales Copilot - {domain.value.title()}"
            for skill in skills.data:
                if skill.display_title == target_title:
                    return SkillInfo(
                        domain=domain,
                        skill_id=skill.id,
                        version=skill.latest_version,
                        display_title=skill.display_title
                    )
        except Exception:
            pass

        return None

    def get_skill_config(self, domain: SkillDomain) -> dict | None:
        """Get the container.skills config for a domain."""
        skill_info = self._skills.get(domain)
        if not skill_info:
            return None

        return {
            "type": "custom",
            "skill_id": skill_info.skill_id,
            "version": "latest"
        }

    def get_skills_config(self, domains: list[SkillDomain]) -> list[dict]:
        """Get container.skills config for multiple domains."""
        configs = []
        for domain in domains:
            config = self.get_skill_config(domain)
            if config:
                configs.append(config)
        return configs

    def get_skill_id(self, domain: SkillDomain) -> str | None:
        """Get the skill_id for a domain."""
        skill_info = self._skills.get(domain)
        return skill_info.skill_id if skill_info else None

    @property
    def available_domains(self) -> list[SkillDomain]:
        """Get list of domains with uploaded skills."""
        return list(self._skills.keys())

    @property
    def is_initialized(self) -> bool:
        return self._initialized


# Global skill manager instance
skill_manager = SkillManager()
