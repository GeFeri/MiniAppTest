import os
import httpx
from typing import Any, Dict, List, Optional

API_BASE = os.getenv("API_BASE_URL", "").rstrip("/")
API_TIMEOUT = int(os.getenv("API_TIMEOUT", "10"))
API_BEARER = os.getenv("API_BEARER")  # опционально

def _headers() -> Dict[str, str]:
    h = {"Accept": "application/json"}
    if API_BEARER:
        h["Authorization"] = f"Bearer {API_BEARER}"
    return h

async def create_invite(
    department: int,
    first_name: str,
    last_name: str,
    telegram_username: Optional[str] = None,
    expires_in_hours: int = 48,
) -> Dict[str, Any]:
    url = f"{API_BASE}/invites/"
    payload = {
        "department": department,
        "first_name": first_name,
        "last_name": last_name,
        "telegram_username": telegram_username,
        "expires_in_hours": expires_in_hours,
    }
    async with httpx.AsyncClient(timeout=API_TIMEOUT) as client:
        r = await client.post(url, json=payload, headers=_headers())
        r.raise_for_status()
        return r.json()

async def activate_invite(tg_id: int, key: str) -> Dict[str, Any]:
    url = f"{API_BASE}/invites/activate/"
    payload = {
        "telegram_id": tg_id,
        "invite_key": key
    }
    async with httpx.AsyncClient(timeout=API_TIMEOUT) as client:
        r = await client.post(url, json=payload, headers=_headers())
        r.raise_for_status()
        return r.json()


async def get_upcoming_events(days: int = 7) -> List[Dict[str, Any]]:
    url = f"{API_BASE}/events/upcoming"
    params = {"days": days}
    async with httpx.AsyncClient(timeout=API_TIMEOUT) as client:
        r = await client.get(url, params=params, headers=_headers())
        r.raise_for_status()
        return r.json()

async def get_upcoming_birthdays(days: int = 7) -> List[Dict[str, Any]]:
    url = f"{API_BASE}/birthdays/upcoming"
    params = {"days": days}
    async with httpx.AsyncClient(timeout=API_TIMEOUT) as client:
        r = await client.get(url, params=params, headers=_headers())
        r.raise_for_status()
        return r.json()
