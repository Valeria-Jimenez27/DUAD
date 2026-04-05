from dotenv import load_dotenv
load_dotenv()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DB_URI = os.getenv("DB_URI")
engine = create_engine(DB_URI, echo=True)

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

def create_tables():
    try:
        conn = engine.connect()
        print("Connection successful!")
        conn.close()

        import DB
        Base.metadata.create_all(engine)
        print("Tables created successfully!")

    except Exception as e:
        print("Connection failed:", e)
