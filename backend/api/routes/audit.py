from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from backend.core.database import get_db
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timezone
import uuid, hashlib, json

router = APIRouter(tags=["audit"])

# In-memory audit log until DB model is added (Sprint 2 phase 2)
_audit_log = []
_last_hash = "0" * 64

def append_audit(event_type: str, entity_id: str, details: dict) -> dict:
    global _last_hash
    now = datetime.now(timezone.utc).isoformat()
    entry = {
        "id": str(uuid.uuid4()),
        "event_type": event_type,
        "entity_id": entity_id,
        "details": details,
        "timestamp": now,
        "prev_hash": _last_hash,
    }
    entry_str = json.dumps({k: v for k, v in entry.items() if k != "hash"}, sort_keys=True)
    entry["hash"] = hashlib.sha256(entry_str.encode()).hexdigest()
    _last_hash = entry["hash"]
    _audit_log.append(entry)
    return entry

def verify_chain(log: list) -> bool:
    if not log:
        return True
    prev = "0" * 64
    for entry in log:
        check = {k: v for k, v in entry.items() if k != "hash"}
        check_str = json.dumps(check, sort_keys=True)
        expected = hashlib.sha256(check_str.encode()).hexdigest()
        if entry.get("hash") != expected:
            return False
        prev = entry["hash"]
    return True

@router.get("/log")
async def get_audit_log(limit: int = 50):
    """Return hash-chained audit log with chain integrity verification."""
    recent = _audit_log[-limit:]
    chain_intact = verify_chain(_audit_log)
    return {
        "events": recent,
        "total": len(_audit_log),
        "chain_intact": chain_intact,
        "last_hash": _last_hash
    }

@router.post("/log")
async def add_audit_event(event_type: str, entity_id: str, details: dict = {}):
    """Add event to hash-chained audit log."""
    entry = append_audit(event_type, entity_id, details)
    return {"status": "logged", "hash": entry["hash"], "id": entry["id"]}
