import os
from dotenv import load_dotenv

load_dotenv()  # Извлекаем переменные окружения из файла .env

# BOT
TOKEN = os.environ.get("TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
ADMIN_ID = [int(os.environ.get("ADMIN_ID_1")), ]
PAYMENT_TOKEN = os.environ.get('PAYMENT_TOKEN')
EXEL_FILENAME = os.environ.get('EXEL_FILENAME')
SHEET_NAME = os.environ.get('SHEET_NAME')

# PostgresSQL
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

#  FAQ
FAQ = {
    1: ['Question 1', 'Answer 1'],
    2: ['Question 2', 'Answer 2'],
    3: ['Question 3', 'Answer 3'],
    4: ['Question 4', 'Answer 4'],
}
