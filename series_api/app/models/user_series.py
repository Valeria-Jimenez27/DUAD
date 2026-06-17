import uuid
from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, Integer, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

if TYPE_CHECKING:
    from .series import Series


class UserSeries(Base):
    __tablename__ = "user_series"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    series_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("series.id"), nullable=False, unique=True
    )
    # Valores válidos: completed, watching, dropped, on_hold, plan_to_watch
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    seasons_watched: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    episodes_watched: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    rating: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # 1-5
    review: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    series: Mapped["Series"] = relationship("Series", back_populates="user_series")

    def __repr__(self) -> str:
        return f"<UserSeries series_id={self.series_id!r} status={self.status!r}>"
