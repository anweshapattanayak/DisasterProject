from database import SessionLocal
import models
import utils

db = SessionLocal()

admin = models.User(
    name="Admin",
    email="admin@gmail.com",
    password=utils.hash_password("admin123"),
    role="admin"
)

db.add(admin)
db.commit()

print("Admin created successfully")