import json
from pathlib import Path
from ..models import SkillDomain

REGISTRY_FILE = Path(__file__).resolve().parent.parent.parent / "skills" / ".registry.json"


class SkillRegistry:
    """Maps skill domains to their uploaded skill_ids."""

    def __init__(self):
        self._mapping: dict[str, str] = {}
        self._load()

    def _load(self) -> None:
        if REGISTRY_FILE.exists():
            with open(REGISTRY_FILE) as f:
                self._mapping = json.load(f)

    def _save(self) -> None:
        REGISTRY_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(REGISTRY_FILE, "w") as f:
            json.dump(self._mapping, f, indent=2)

    def register(self, domain: SkillDomain, skill_id: str) -> None:
        self._mapping[domain.value] = skill_id
        self._save()

    def get_skill_id(self, domain: SkillDomain) -> str | None:
        return self._mapping.get(domain.value)

    def get_all(self) -> dict[str, str]:
        return dict(self._mapping)

    def is_registered(self, domain: SkillDomain) -> bool:
        return domain.value in self._mapping

    def clear(self) -> None:
        self._mapping.clear()
        if REGISTRY_FILE.exists():
            REGISTRY_FILE.unlink()
