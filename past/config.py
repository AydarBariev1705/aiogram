import os
from dotenv import load_dotenv

load_dotenv()  # Извлекаем переменные окружения из файла .env

TOKEN = os.environ.get("TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
ADMIN_ID = [int(os.environ.get("ADMIN_ID_1")),]
TEST_PAYMENT_TOKEN = os.environ.get("TEST_PAYMENT_TOKEN")

# PostgresSQL
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")




