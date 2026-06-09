from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db(db: Session) -> None:
    # Checking for the root enterprise administrator
    user = db.query(User).filter(User.email == "arpita.jaiswal@eaios.com").first()
    if not user:
        user = User(
            email="arpita.jaiswal@eaios.com",
            hashed_password=get_password_hash("ExecutiveAccess2026!"),
            full_name="Arpita Jaiswal",
            is_superuser=True,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        logger.info("Superuser created successfully.")
    else:
        logger.info("Superuser already exists in the database.")

def main() -> None:
    logger.info("Initializing enterprise database seed...")
    db = SessionLocal()
    try:
        init_db(db)
        logger.info("Database seeding complete.")
    finally:
        db.close()

if __name__ == "__main__":
    main()