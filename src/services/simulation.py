import json
from pathlib import Path
from ..models import TranscriptEntry, Speaker

SCENARIOS_DIR = Path(__file__).resolve().parent.parent.parent / "scenarios"


class SimulationEngine:
    def __init__(self, scenario_name: str | None = None):
        self.entries: list[TranscriptEntry] = []
        self.current_index: int = 0
        self.scenario_name = scenario_name

        if scenario_name:
            self._load_scenario(scenario_name)

    def _load_scenario(self, name: str) -> None:
        path = SCENARIOS_DIR / f"{name}.json"
        if not path.exists():
            raise FileNotFoundError(f"Scenario not found: {path}")

        with open(path) as f:
            data = json.load(f)

        self.entries = [
            TranscriptEntry(
                offset_sec=entry["offset_sec"],
                speaker=Speaker(entry["speaker"]),
                text=entry["text"],
            )
            for entry in data.get("entries", [])
        ]

    def reset(self) -> None:
        self.current_index = 0

    def next_entry(self) -> TranscriptEntry | None:
        if self.current_index >= len(self.entries):
            return None
        entry = self.entries[self.current_index]
        self.current_index += 1
        return entry

    def has_more(self) -> bool:
        return self.current_index < len(self.entries)

    def peek(self) -> TranscriptEntry | None:
        if self.current_index >= len(self.entries):
            return None
        return self.entries[self.current_index]
