from engine import SessionLocal, Base, create_tables
from DB import User

create_tables()

db = SessionLocal()

admin = User(
    name="Admin",
    email="admin@example.com",
    password="23456",
    role="admin"
)

db.add(admin)
db.commit()
db.close()

print("Admin created!")