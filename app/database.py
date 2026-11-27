from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
 
# Database URL
DATABASE_URL = "sqlite:///./tasks.db"

# Create database engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Create database session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Create base class
Base = declarative_base()

def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()
