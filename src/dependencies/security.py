from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import APIKeyHeader

from core.config import settings

API_KEY_HEADER = APIKeyHeader(name=settings.security.api_key_name, auto_error=True)


def verify_api_key(api_key: str = Depends(API_KEY_HEADER)) -> str:
    if api_key != settings.security.api_key:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return api_key
