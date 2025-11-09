import json
import asyncio
from pathlib import Path
from typing import Set

class SubscriberStore:
    def __init__(self, path: str = "subscribers.json"):
        self._path = Path(path)
        self._lock = asyncio.Lock()
        if not self._path.exists():
            self._path.write_text(json.dumps({"subscribers": []}, ensure_ascii=False))

    async def add(self, user_id: int):
        async with self._lock:
            data = json.loads(self._path.read_text())
            subs = set(data.get("subscribers", []))
            subs.add(user_id)
            data["subscribers"] = list(subs)
            self._path.write_text(json.dumps(data, ensure_ascii=False))

    async def remove(self, user_id: int):
        async with self._lock:
            data = json.loads(self._path.read_text())
            subs = set(data.get("subscribers", []))
            subs.discard(user_id)
            data["subscribers"] = list(subs)
            self._path.write_text(json.dumps(data, ensure_ascii=False))

    async def all(self) -> Set[int]:
        async with self._lock:
            data = json.loads(self._path.read_text())
            return set(data.get("subscribers", []))
