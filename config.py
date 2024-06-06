import os
from dotenv import load_dotenv

load_dotenv()  # Извлекаем переменные окружения из файла .env
#BOT
TOKEN = os.environ.get("TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
ADMIN_ID = [int(os.environ.get("ADMIN_ID_1")),]
PAYMENT_TOKEN = os.environ.get('PAYMENT_TOKEN')
EXEL_FILENAME = os.environ.get('EXEL_FILENAME')
SHEET_NAME = os.environ.get('SHEET_NAME')
# PostgresSQL
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")




