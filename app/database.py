import os
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_DATABASE_PATH = BASE_DIR / "smart_database.db"

if os.getenv("VERCEL") and not os.getenv("DATABASE_URL"):
    DEFAULT_DATABASE_PATH = Path(os.getenv("TMPDIR", "/tmp")) / "smart_database.db"

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"sqlite:///{DEFAULT_DATABASE_PATH}",
)
SQLALCHEMY_DATABASE_URL = DATABASE_URL
DATABASE_PATH = DEFAULT_DATABASE_PATH if DATABASE_URL.startswith("sqlite:///") else None

if DATABASE_URL.startswith("sqlite:///"):
    sqlite_path = Path(DATABASE_URL.replace("sqlite:///", "", 1))
    sqlite_path.parent.mkdir(parents=True, exist_ok=True)

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
