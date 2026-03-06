from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DB_URI = "postgresql://postgres:postgres@localhost:5432/fruits_market"
engine = create_engine(DB_URI, echo=True)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

def create_tables():
    try:
        conn = engine.connect()
        print("Connection successful!")
        conn.close()

        Base.metadata.create_all(engine)
        print("Tables created successfully!")

    except Exception as e:
        print("Connection failed:", e)