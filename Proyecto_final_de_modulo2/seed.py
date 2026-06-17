from dotenv import load_dotenv
load_dotenv()

import os
from engine import SessionLocal, create_tables
from DB import User
import bcrypt

def seed_admin():
    create_tables()
    email= os.getenv("ADMIN_EMAIL")
    password= os.getenv("ADMIN_PASSWORD")
    name= os.getenv("ADMIN_NAME", "Admin")

    if not email or not password:
        return
    
    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.email == email).first()
        if existing:
            print("Admin already exists. No changes made.")
            return

        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        admin = User(name=name, email=email, password=hashed, role="admin")
        db.add(admin)
        db.commit()
        print(f"Admin created: {email}")
        print("Change the password after first login!")

    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_admin()