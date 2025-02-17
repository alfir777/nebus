from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from dependencies.security import verify_api_key
from utils.fill_random_data import fill_test_data

router = APIRouter(tags=["Common"])


@router.get("/fill-test-data", description="Заполнить БД тестовыми данными")
async def fill_data(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    _: bool = Depends(verify_api_key),
) -> dict[str, str]:
    try:
        await fill_test_data(session)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    return {"Fill test data": "Success"}
