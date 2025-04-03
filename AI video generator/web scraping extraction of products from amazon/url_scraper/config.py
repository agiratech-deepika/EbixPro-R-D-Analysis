import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database credentials
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

# PostgreSQL connection string
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Temp folder for storing extracted files
TEMP_FOLDER = os.getenv("TEMP_FOLDER", "temp/")
if not os.path.exists(TEMP_FOLDER):
    os.makedirs(TEMP_FOLDER)
