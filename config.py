import os

from dotenv import load_dotenv

load_dotenv()
DB_CONFIG = {
    "host": os.getenv("HOST"),
    "port": os.getenv("PORT"),
    "user": os.getenv("LOGIN"),
    "password": os.getenv("PASSWORD")
}

# Введите страны, в которых необходимо получить самолеты
COUNTRIES = ["Canada", "Sweden", "Korea", "Poland"]
