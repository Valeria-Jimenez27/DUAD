from sqlalchemy import create_engine


DB_URI = "postgresql://postgres:postgres@localhost:5432/orms_practice"
engine = create_engine(DB_URI, echo=True)

try:
    connection = engine.connect()
    print("Connection successful!")
    connection.close()
except Exception as e:
    print("Connection failed:", e)