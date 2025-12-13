"""
Skill Manager - Manages skills with official API + fallback pattern.

Production approach:
1. Try official Skills API (container.skills) if available
2. Fall back to prompt injection if API not accessible

This ensures the app works regardless of API access level while being
ready for the official API when available.

See: https://platform.claude.com/docs/en/build-with-claude/skills-guide
"""

from pathlib import Path
from dataclasses import dataclass, field
import anthropic
from ..config import get_settings
from ..models import SkillDomain

SKILLS_DIR = Path(__file__).resolve().parent.parent.parent / "skills"

# Beta feature identifiers for official Skills API
BETAS = ["code-execution-2025-08-25", "skills-2025-10-02"]


@dataclass
class SkillInfo:
    """Information about a skill."""
    domain: SkillDomain
    skill_id: str | None = None  # None means fallback to prompt injection
    version: str | None = None
    display_title: str = ""
    content: str | None = None  # Cached content for prompt injection


@dataclass
class SkillManager:
    """Manages skills with official API + prompt injection fallback."""

    _skills: dict[SkillDomain, SkillInfo] = field(default_factory=dict)
    _initialized: bool = False
    _use_official_api: bool = False  # Will be True if Skills API is accessible
    _client: anthropic.Anthropic | None = None

    def __post_init__(self):
        settings = get_settings()
        self._client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

    async def initialize(self) -> None:
        """Initialize skills - try official API, fall back to local loading."""
        if self._initialized:
            return

        # First, try the official Skills API
        if await self._try_official_api():
            print("Using official Skills API")
            self._use_official_api = True
        else:
            print("Skills API not available - using prompt injection fallback")
            self._use_official_api = False
            await self._load_local_skills()

        self._initialized = True

    async def _try_official_api(self) -> bool:
        """Try to use the official Skills API. Returns True if successful."""
        try:
            # Try to list skills to check if API is accessible
            existing_skills = self._client.beta.skills.list(source="custom", betas=BETAS)

            # Build a map of display_title -> skill for reuse
            existing_by_title = {s.display_title: s for s in existing_skills.data}

            # If we get here, API is accessible - upload or reuse skills
            for domain in SkillDomain:
                skill_dir = SKILLS_DIR / domain.value
                if not skill_dir.exists():
                    continue

                try:
                    skill_info = await self._upload_or_reuse_skill(
                        domain, skill_dir, existing_by_title
                    )
                    if skill_info:
                        self._skills[domain] = skill_info
                except Exception as e:
                    print(f"Warning: Failed to upload skill {domain.value}: {e}")

            return len(self._skills) > 0

        except anthropic.NotFoundError:
            # Skills API not available
            return False
        except Exception as e:
            print(f"Skills API check failed: {e}")
            return False

    async def _upload_or_reuse_skill(
        self, domain: SkillDomain, skill_dir: Path, existing_by_title: dict
    ) -> SkillInfo | None:
        """Upload a skill or reuse existing one if display_title matches."""
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            return None

        display_title = f"Interview Copilot - {domain.value.replace('_', ' ').title()}"

        # Check if skill with this display_title already exists
        if display_title in existing_by_title:
            existing = existing_by_title[display_title]
            print(f"Reusing existing skill: {display_title} (id={existing.id})")
            return SkillInfo(
                domain=domain,
                skill_id=existing.id,
                version=existing.latest_version,
                display_title=display_title
            )

        # Create new skill
        return await self._upload_skill(domain, skill_dir, display_title)

    async def _upload_skill(
        self, domain: SkillDomain, skill_dir: Path, display_title: str
    ) -> SkillInfo | None:
        """Upload a single skill to Anthropic via official API."""
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            return None

        # Extract skill name from YAML frontmatter
        skill_content = skill_md.read_text()
        skill_name = self._extract_skill_name(skill_content, domain)

        files = []
        # Folder name must match the 'name' field in SKILL.md frontmatter
        dir_name = skill_name
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

        skill = self._client.beta.skills.create(
            display_title=display_title,
            files=files,
            betas=BETAS
        )

        print(f"Created new skill: {display_title} (id={skill.id})")
        return SkillInfo(
            domain=domain,
            skill_id=skill.id,
            version=skill.latest_version,
            display_title=display_title
        )

    def _extract_skill_name(self, content: str, domain: SkillDomain) -> str:
        """Extract skill name from YAML frontmatter."""
        import re
        # Look for name field in YAML frontmatter
        if content.startswith("---"):
            end = content.find("---", 3)
            if end != -1:
                frontmatter = content[3:end]
                match = re.search(r'^name:\s*(.+)$', frontmatter, re.MULTILINE)
                if match:
                    return match.group(1).strip()
        # Fallback: convert domain value (underscores to hyphens)
        return domain.value.replace("_", "-")

    async def _load_local_skills(self) -> None:
        """Load skills from local files for prompt injection."""
        for domain in SkillDomain:
            skill_dir = SKILLS_DIR / domain.value
            if not skill_dir.exists():
                continue

            content = self._load_skill_content(skill_dir, domain)
            if content:
                self._skills[domain] = SkillInfo(
                    domain=domain,
                    display_title=f"Interview Copilot - {domain.value.replace('_', ' ').title()}",
                    content=content
                )

    def _load_skill_content(self, skill_dir: Path, domain: SkillDomain) -> str | None:
        """Load skill content from local files."""
        content_parts = []

        # Load SKILL.md
        skill_md = skill_dir / "SKILL.md"
        if skill_md.exists():
            content_parts.append(f"=== SKILL: {domain.value.upper()} ===\n")
            # Strip YAML frontmatter if present
            text = skill_md.read_text()
            if text.startswith("---"):
                # Find end of frontmatter
                end = text.find("---", 3)
                if end != -1:
                    text = text[end + 3:].strip()
            content_parts.append(text)

        # Load reference files
        refs_dir = skill_dir / "references"
        if refs_dir.exists():
            for ref_file in refs_dir.glob("*.md"):
                content_parts.append(f"\n--- Reference: {ref_file.name} ---\n")
                content_parts.append(ref_file.read_text())

        return "\n".join(content_parts) if content_parts else None

    def get_skill_config(self, domain: SkillDomain) -> dict | None:
        """Get container.skills config for official API."""
        if not self._use_official_api:
            return None

        skill_info = self._skills.get(domain)
        if not skill_info or not skill_info.skill_id:
            return None

        return {
            "type": "custom",
            "skill_id": skill_info.skill_id,
            "version": "latest"
        }

    def get_skills_config(self, domains: list[SkillDomain]) -> list[dict]:
        """Get container.skills config for multiple domains."""
        if not self._use_official_api:
            return []

        configs = []
        for domain in domains:
            config = self.get_skill_config(domain)
            if config:
                configs.append(config)
        return configs

    def get_skill_content(self, domain: SkillDomain) -> str | None:
        """Get skill content for prompt injection."""
        skill_info = self._skills.get(domain)
        return skill_info.content if skill_info else None

    def get_skills_content(self, domains: list[SkillDomain]) -> str:
        """Get combined skill content for prompt injection."""
        contents = []
        for domain in domains:
            content = self.get_skill_content(domain)
            if content:
                contents.append(content)
        return "\n\n".join(contents) if contents else ""

    @property
    def available_domains(self) -> list[SkillDomain]:
        """Get list of available skill domains."""
        return list(self._skills.keys())

    @property
    def is_initialized(self) -> bool:
        return self._initialized

    @property
    def using_official_api(self) -> bool:
        return self._use_official_api


# Global skill manager instance
skill_manager = SkillManager()
