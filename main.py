# main.py
import logging
from datetime import time
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

# Импортируем наши модули
from src import config, database as db, handlers as h
from src.scheduler import check_due_dates

# Включаем логирование для отладки
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Получаем класс с состояниями из конфига
States = config.States


def main() -> None:
    """Основная функция для запуска бота."""
    
    # Проверяем наличие токена
    if not config.BOT_TOKEN:
        logger.error("BOT_TOKEN не найден! Проверьте .env файл и src/config.py.")
        return

    # Инициализируем базу данных
    db.init_db()

    # Создаем приложение
    application = Application.builder().token(config.BOT_TOKEN).build()

    # --- РЕГИСТРАЦИЯ ОБРАБОТЧИКОВ ---

    # 1. ConversationHandler для добавления новой записи
    add_record_conv = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(h.add_record_start, pattern="^main_add_record$")
        ],
        states={
            States.CHOOSE_TYPE: [
                CallbackQueryHandler(h.add_record_type_chosen, pattern="^add_type_")
            ],
            States.ADD_NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, h.add_record_name)
            ],
            States.ADD_AMOUNT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, h.add_record_amount)
            ],
            States.ADD_DATE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, h.add_record_date)
            ],
            States.ADD_CONFIRMATION: [
                CallbackQueryHandler(h.add_record_confirm, pattern="^confirm_yes_")
            ],
        },
        fallbacks=[
            CommandHandler("cancel", h.cancel_conversation),
            CallbackQueryHandler(h.main_menu_from_conv, pattern="^main_menu$"),
        ],
        per_user=True,
    )

    # 2. ConversationHandler для частичного погашения
    repay_conv = ConversationHandler(
        entry_points=[
            # --- ИСПРАВЛЕНИЕ ЗДЕСЬ ---
            # Шаблон теперь правильно соответствует callback_data 'repay|...'
            # Обратный слэш \ нужен, чтобы символ '|' не считался спецсимволом regex.
            CallbackQueryHandler(h.repay_start, pattern="^repay\|")
        ],
        states={
            States.REPAY_AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, h.repay_amount)]
        },
        fallbacks=[CommandHandler('cancel', h.cancel_conversation)],
        per_user=True
    )
    
    # 3. Регистрируем все обработчики в правильном порядке
    application.add_handler(add_record_conv)
    application.add_handler(repay_conv)
    
    application.add_handler(CommandHandler("start", h.start))
    application.add_handler(CommandHandler("cancel", h.cancel_conversation))
    
    application.add_handler(CallbackQueryHandler(h.my_debts_menu, pattern="^main_my_debts$"))
    application.add_handler(CallbackQueryHandler(h.their_debts_menu, pattern="^main_their_debts$"))
    application.add_handler(CallbackQueryHandler(h.start_from_callback, pattern="^main_menu$"))
    
    application.add_handler(CallbackQueryHandler(h.list_navigation_handler))
    
    # --- ЗАПУСК ПЛАНИРОВЩИКА УВЕДОМЛЕНИЙ ---
    job_queue = application.job_queue
    if job_queue:
        notification_time = time(
            hour=config.NOTIFICATION_TIME["hour"],
            minute=config.NOTIFICATION_TIME["minute"],
            second=config.NOTIFICATION_TIME["second"],
        )
        job_queue.run_daily(check_due_dates, time=notification_time)
        logger.info(f"Notification job scheduled for {notification_time} daily.")
    else:
        logger.warning("JobQueue is not available. Notifications will not be sent.")

    # Запускаем бота
    logger.info("Starting bot...")
    application.run_polling()


if __name__ == "__main__":
    main()