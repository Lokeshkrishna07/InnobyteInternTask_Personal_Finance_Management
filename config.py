import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).parent / ".env")

basedir = Path(__file__).resolve().parent

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret")
    # SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", f"sqlite:///{basedir / 'data' / 'finance_tracker.db'}")
    SQLALCHEMY_DATABASE_URI = 'sqlite:////Users/lokeshkrishna/Downloads/personal_finance_tracker_full/backend/data/finance_tracker.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BCRYPT_LOG_ROUNDS = int(os.environ.get("BCRYPT_LOG_ROUNDS", 12))
