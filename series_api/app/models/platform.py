import uuid
from typing import TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

if TYPE_CHECKING:
    from .series import Series


class Platform(Base):
    __tablename__ = "platforms"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    series: Mapped[list["Series"]] = relationship("Series", back_populates="platform")

    def __repr__(self) -> str:
        return f"<Platform {self.name!r}>"
