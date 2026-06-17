import uuid
from typing import TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

if TYPE_CHECKING:
    from .series import Series


class Genre(Base):
    __tablename__ = "genres"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    slug: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    # secondary como string para evitar import circular con series.py
    series: Mapped[list["Series"]] = relationship(
        "Series", secondary="series_genres", back_populates="genres"
    )

    def __repr__(self) -> str:
        return f"<Genre {self.name!r}>"
