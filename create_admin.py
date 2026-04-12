from app.db.session import SessionLocal
from app.models.user import User
from app.services.user.user_service import pwd_context
from app.schemas.user.user_schema import UserRole

db = SessionLocal()

email = "admin@klyo.com"
password = "admin123"
name = "Super Admin"

# Check if admin already exists
existing = db.query(User).filter(User.email == email).first()

if existing:
    print("❌ Admin already exists")
else:
    hashed_password = pwd_context.hash(password)

    admin = User(
        name=name,
        email=email,
        hashed_password=hashed_password,
        role=UserRole.admin
    )

    db.add(admin)
    db.commit()
    print("✅ Admin created successfully")

db.close()