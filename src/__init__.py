import os
from dotenv import load_dotenv

from .logger import setup_logger
from .models import Trade
from .config import DATABASE_URL
from .db import Database

ENV = os.getenv("ENV", "prod")
if ENV == "dev":
    load_dotenv()