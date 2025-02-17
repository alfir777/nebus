from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from repositories.organization import OrganizationRepository
from services.organization import OrganizationService


def get_organization_service(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
):
    repo = OrganizationRepository(session=session)
    return OrganizationService(organization_repo=repo)
