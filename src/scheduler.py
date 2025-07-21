# src/scheduler.py
import logging
from telegram.ext import ContextTypes
from . import database as db
from . import config

logger = logging.getLogger(__name__)

NOTIFICATION_DAYS = config.NOTIFICATION_DAYS
MY_DEBT_PHOTO = config.NOTIFICATION_PHOTO_PATH
THEIR_DEBT_PHOTO = config.NOTIFICATION_RECEIVABLE_PHOTO_PATH

async def check_due_dates(context: ContextTypes.DEFAULT_TYPE):
    """Проверяет сроки погашения для ОБОИХ типов долгов и отправляет уведомления."""
    logger.info("Running daily job: Checking all due dates...")
    
    # --- 1. Проверка МОИХ долгов (кому должен Я) ---
    try:
        debts_due_soon = db.get_debts_due_soon(days_ahead=NOTIFICATION_DAYS)
        logger.info(f"Found {len(debts_due_soon)} of MY debts due soon.")
        
        for debt in debts_due_soon:
            user_id = debt['user_id']
            days_left = debt['days_left']
            
            if days_left == 0:
                message = f"🔔 *НАПОМИНАНИЕ: СЕГОДНЯ* крайний срок!\n\n"
            else:
                days_word = "дня" if 1 < days_left < 5 else "дней"
                message = f"🔔 *НАПОМИНАНИЕ: Осталось {days_left} {days_word}* до срока погашения долга.\n\n"
            
            message += (f"Кому: *{debt['name']}*\n"
                        f"Сумма: *{debt['amount']}* руб.\n"
                        f"Вернуть до: *{debt['due_date']}*")
            
            try:
                await context.bot.send_photo(
                    chat_id=user_id, photo=open(MY_DEBT_PHOTO, 'rb'),
                    caption=message, parse_mode='Markdown')
            except Exception as e:
                logger.error(f"Failed to send MY debt notification to {user_id}: {e}")

    except Exception as e:
        logger.error(f"Error checking MY debts: {e}")

    # --- 2. Проверка ИХ долгов (кто должен МНЕ) ---
    try:
        receivables_due_soon = db.get_receivables_due_soon(days_ahead=NOTIFICATION_DAYS)
        logger.info(f"Found {len(receivables_due_soon)} of THEIR debts due soon.")

        for debt in receivables_due_soon:
            user_id = debt['user_id']
            days_left = debt['days_left']

            if days_left == 0:
                message = f"🔔 *НАПОМИНАНИЕ: СЕГОДНЯ* должны вернуть долг!\n\n"
            else:
                days_word = "дня" if 1 < days_left < 5 else "дней"
                message = f"🔔 *НАПОМИНАНИЕ: Через {days_left} {days_word}* вам должны вернуть долг.\n\n"

            message += (f"Кто: *{debt['name']}*\n"
                        f"Сумма: *{debt['amount']}* руб.\n"
                        f"Обещал вернуть до: *{debt['due_date']}*")
            
            try:
                await context.bot.send_photo(
                    chat_id=user_id, photo=open(THEIR_DEBT_PHOTO, 'rb'),
                    caption=message, parse_mode='Markdown')
            except Exception as e:
                logger.error(f"Failed to send THEIR debt notification to {user_id}: {e}")
                
    except Exception as e:
        logger.error(f"Error checking THEIR debts: {e}")