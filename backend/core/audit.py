import hashlib, json
from datetime import datetime, timezone
from typing import Optional

async def write_audit(db, org_id, event_type, payload, user_id=None, previous_hash=None):
    from backend.models.audit import AuditLog
    timestamp = datetime.now(timezone.utc).isoformat()
    entry_data = json.dumps({"org_id": org_id, "event_type": event_type, "payload": payload,
        "user_id": user_id, "timestamp": timestamp, "previous_hash": previous_hash or "GENESIS"}, sort_keys=True)
    entry_hash = hashlib.sha256(entry_data.encode()).hexdigest()
    log = AuditLog(org_id=org_id, event_type=event_type, payload=payload, user_id=user_id,
        timestamp=timestamp, previous_hash=previous_hash or "GENESIS", entry_hash=entry_hash)
    db.add(log)
    await db.flush()
    return log

async def verify_chain(db, org_id):
    from sqlalchemy import select
    from backend.models.audit import AuditLog
    result = await db.execute(select(AuditLog).where(AuditLog.org_id == org_id).order_by(AuditLog.id))
    logs = result.scalars().all()
    for i, log in enumerate(logs):
        entry_data = json.dumps({"org_id": log.org_id, "event_type": log.event_type,
            "payload": log.payload, "user_id": log.user_id, "timestamp": log.timestamp,
            "previous_hash": log.previous_hash}, sort_keys=True)
        if hashlib.sha256(entry_data.encode()).hexdigest() != log.entry_hash:
            return False
        if i > 0 and log.previous_hash != logs[i-1].entry_hash:
            return False
    return True
