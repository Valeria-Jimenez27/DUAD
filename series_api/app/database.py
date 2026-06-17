import os
from contextlib import contextmanager

from pathlib import Path
try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent.parent / ".env")
except ImportError:
    pass

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


class Base(DeclarativeBase):
    pass


_DATABASE_URL = os.environ.get("DATABASE_URL")

if _DATABASE_URL:
    engine = create_engine(_DATABASE_URL, echo=False)
    SessionLocal = sessionmaker(bind=engine)
else:
    engine = None
    SessionLocal = None


@contextmanager
def get_db():
    if SessionLocal is None:
        raise RuntimeError(
            "DATABASE_URL no está configurado. "
            "Creá un archivo .env basado en .env.example."
        )
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
