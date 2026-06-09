from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# Enterprise SQLAlchemy 2.0 Engine
engine = create_engine(
    str(settings.SQLALCHEMY_DATABASE_URI),
    pool_pre_ping=True, 
    pool_size=10,
    max_overflow=20
)

# Database Session Factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarative Base for ORM Models
Base = declarative_base()

def get_db():
    """Dependency injection for secure database sessions."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()