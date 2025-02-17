from typing import List, TYPE_CHECKING

from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models import Base

if TYPE_CHECKING:
    from models.organization import Organization


class Building(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    address: Mapped[str] = mapped_column(nullable=False)
    latitude: Mapped[float] = mapped_column(nullable=False)
    longitude: Mapped[float] = mapped_column(nullable=False)

    organizations: Mapped[List["Organization"]] = relationship("Organization", back_populates="building")
