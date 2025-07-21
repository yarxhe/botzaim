import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла в корне проекта
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# --- Секреты ---
BOT_TOKEN = os.getenv("BOT_TOKEN")

# --- Настройки базы данных ---
DB_NAME = 'debts.db'

# --- Пути к файлам ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_PATH = os.path.join(BASE_DIR, 'static')
BOT_PHOTO_PATH = os.path.join(STATIC_PATH, 'bot_photo.jpg')
NOTIFICATION_PHOTO_PATH = os.path.join(STATIC_PATH, 'photo_dolg.jpg')
NOTIFICATION_RECEIVABLE_PHOTO_PATH = os.path.join(STATIC_PATH, 'photo_receivable.jpg')

# --- Настройки бота ---
NOTIFICATION_DAYS = 3
NOTIFICATION_TIME = {'hour': 9, 'minute': 0, 'second': 0}

# --- Состояния для ConversationHandler ---
class States:
    CHOOSE_TYPE, ADD_NAME, ADD_AMOUNT, ADD_DATE, ADD_CONFIRMATION = range(5)
    REPAY_AMOUNT = 5