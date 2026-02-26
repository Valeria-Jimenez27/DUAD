from sqlalchemy import create_engine
from Manage_data import Base

DB_URI = "postgresql://postgres:postgres@localhost:5432/orms_practice"
engine = create_engine(DB_URI, echo=True)


def test_connection():
    try:
        with engine.connect() as connection:
            print("Connection successful!")

        Base.metadata.create_all(engine)
        print("Tables created successfully!")

    except Exception as e:
        print("Connection failed:", e)


if __name__ == "__main__":
    test_connection()