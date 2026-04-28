from database import SessionLocal
import models, utils

db = SessionLocal()

volunteer = models.User(
    name="Volunteer",
    email="volunteer@gmail.com",
    password=utils.hash_password("vol123"),
    role="volunteer"
)

db.add(volunteer)
db.commit()

print("Volunteer created")