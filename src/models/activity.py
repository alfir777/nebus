from typing import Optional, List, TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.constants import DEPTH_OF_ACTIVITY
from core.models import Base

if TYPE_CHECKING:
    from models.organization import Organization
    from models.organization_activity import OrganizationActivity


class Activity(Base):
    __tablename__ = "activities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    parent_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("activities.id"), nullable=True)

    parent: Mapped[Optional["Activity"]] = relationship(
        "Activity",
        remote_side=[id],
        backref="children",
        lazy="selectin",
        join_depth=DEPTH_OF_ACTIVITY,
    )

    organization_activities: Mapped[List["OrganizationActivity"]] = relationship(back_populates="activity")
    organizations: Mapped[List["Organization"]] = relationship(
        secondary="organization_activity",
        back_populates="activities",
        overlaps="organization_activities",
    )
