from ..models import TranscriptEntry


class TranscriptStore:
    def __init__(self):
        self._entries: list[TranscriptEntry] = []

    def add(self, entry: TranscriptEntry) -> None:
        self._entries.append(entry)

    def get_all(self) -> list[TranscriptEntry]:
        return list(self._entries)

    def get_recent(self, seconds: float = 60.0) -> list[TranscriptEntry]:
        if not self._entries:
            return []
        latest_time = self._entries[-1].offset_sec
        cutoff = latest_time - seconds
        return [e for e in self._entries if e.offset_sec >= cutoff]

    def get_recent_text(self, seconds: float = 60.0) -> str:
        entries = self.get_recent(seconds)
        lines = [f"[{e.speaker.value}]: {e.text}" for e in entries]
        return "\n".join(lines)

    def get_full_text(self) -> str:
        lines = [f"[{e.speaker.value}]: {e.text}" for e in self._entries]
        return "\n".join(lines)

    def clear(self) -> None:
        self._entries.clear()

    def __len__(self) -> int:
        return len(self._entries)
