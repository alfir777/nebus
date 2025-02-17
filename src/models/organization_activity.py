from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from core.models import Base

if TYPE_CHECKING:
    from models.activity import Activity
    from models.organization import Organization


class OrganizationActivity(Base):
    __tablename__ = "organization_activity"

    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"), primary_key=True)
    activity_id: Mapped[int] = mapped_column(ForeignKey("activities.id"), primary_key=True)

    organization: Mapped["Organization"] = relationship(
        back_populates="organization_activities", overlaps="activities,organizations"
    )
    activity: Mapped["Activity"] = relationship(
        back_populates="organization_activities", overlaps="activities,organizations"
    )
