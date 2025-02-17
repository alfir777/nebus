from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey, Integer, ARRAY, String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from core.models import Base

if TYPE_CHECKING:
    from models.activity import Activity
    from models.organization_activity import OrganizationActivity
    from models.building import Building


class Organization(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False, index=True)
    phones: Mapped[List[str]] = mapped_column(ARRAY(String), nullable=True)

    building_id: Mapped[int] = mapped_column(Integer, ForeignKey("buildings.id"), nullable=False)
    building: Mapped["Building"] = relationship(back_populates="organizations")

    organization_activities: Mapped[List["OrganizationActivity"]] = relationship(back_populates="organization")
    activities: Mapped[List["Activity"]] = relationship(
        secondary="organization_activity",
        back_populates="organizations",
        overlaps="organization_activities",
    )
