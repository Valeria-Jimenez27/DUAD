from sqlalchemy import (create_engine,MetaData,Table,Column,Integer,String,ForeignKey,Date)

DB_URI = "postgresql://postgres:postgres@localhost:5432/orms_practice"
engine = create_engine(DB_URI, echo=True)

metadata_obj = MetaData()

users = Table(
    "users",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(30), nullable=False),
    Column("birth_date", Date, nullable=False),
    Column("email", String(100), nullable=False, unique=True),
)

addresses = Table(
    "addresses",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("street", String(100), nullable=False),
    Column("city", String(100), nullable=False),
    Column("user_id", Integer, ForeignKey("users.id"), nullable=False),
)

cars = Table(
    "cars",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("brand", String(100), nullable=False),
    Column("model", String(100), nullable=False),
    Column("user_id", Integer, ForeignKey("users.id"), nullable=True),
)

metadata_obj.create_all(engine)