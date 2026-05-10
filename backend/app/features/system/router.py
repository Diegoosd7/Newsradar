from fastapi import APIRouter
from datetime import datetime, timezone

router = APIRouter(tags=["system"])


@router.get("/health", tags=["system"])
def health() -> dict:
    return {"status": "ok", "timestamp": datetime.now(timezone.utc).isoformat()}
