import uuid
from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, Integer, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

if TYPE_CHECKING:
    from .platform import Platform
    from .genre import Genre
    from .user_series import UserSeries

# Tabla intermedia — Table() es correcto aquí (no es un modelo ORM)
series_genres = Table(
    "series_genres",
    Base.metadata,
    Column("series_id", String(36), ForeignKey("series.id"), primary_key=True),
    Column("genre_id", String(36), ForeignKey("genres.id"), primary_key=True),
)


class Series(Base):
    __tablename__ = "series"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    year_start: Mapped[int] = mapped_column(Integer, nullable=False)
    year_end: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    total_seasons: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    platform_id: Mapped[Optional[str]] = mapped_column(
        String(36), ForeignKey("platforms.id"), nullable=True
    )

    platform: Mapped[Optional["Platform"]] = relationship("Platform", back_populates="series")
    genres: Mapped[list["Genre"]] = relationship(
        "Genre", secondary=series_genres, back_populates="series"
    )
    user_series: Mapped[Optional["UserSeries"]] = relationship(
        "UserSeries", back_populates="series", uselist=False, cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Series {self.title!r} ({self.year_start})>"
