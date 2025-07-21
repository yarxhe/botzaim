# src/handlers.py
import logging
from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from . import database as db
from . import keyboards as kb
from . import config

logger = logging.getLogger(__name__)
States = config.States

def get_days_left(due_date_str: str) -> str:
    try:
        due_date = datetime.strptime(due_date_str, "%d.%m.%Y").date()
        delta = (due_date - datetime.now().date()).days
        if delta < 0:
            days = abs(delta)
            return f"просрочено на {days} д."
        elif delta == 0:
            return "сегодня"
        else:
            return f"{delta} д."
    except (ValueError, TypeError):
        return "неизвестно"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("--- Triggered start (/start command) ---")
    context.user_data.clear()
    await update.message.reply_photo(
        photo=open(config.BOT_PHOTO_PATH, 'rb'),
        caption="Привет! Я ваш личный финансовый помощник."
    )
    await update.message.reply_text(
        text="Главное меню. Выберите действие:",
        reply_markup=kb.get_main_menu_keyboard(),
        parse_mode='Markdown'
    )

async def start_from_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("--- Triggered start_from_callback (Back to menu button) ---")
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text="Главное меню. Выберите действие:",
        reply_markup=kb.get_main_menu_keyboard(),
        parse_mode='Markdown'
    )

async def my_debts_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("--- Triggered my_debts_menu ---")
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    creditors = db.get_creditors(user_id)
    if not creditors:
        await query.edit_message_text(text="🎉 У вас нет долгов!", reply_markup=kb.get_main_menu_keyboard())
        return
    total = db.get_total_debt(user_id)
    text = f"Общая сумма ваших долгов: *{total}* руб.\n\nВыберите кредитора:"
    await query.edit_message_text(text, reply_markup=kb.get_list_keyboard('debt', creditors), parse_mode='Markdown')

async def their_debts_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("--- Triggered their_debts_menu ---")
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    debtors = db.get_debtors(user_id)
    if not debtors:
        await query.edit_message_text(text="🎉 Вам никто не должен!", reply_markup=kb.get_main_menu_keyboard())
        return
    total = db.get_total_receivables(user_id)
    text = f"Общая сумма, которую вам должны: *{total}* руб.\n\nВыберите должника:"
    await query.edit_message_text(text, reply_markup=kb.get_list_keyboard('receivable', debtors), parse_mode='Markdown')

# --- Диалог добавления ---
async def add_record_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info("--- Triggered add_record_start (Conversation) ---")
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="Какую запись вы хотите добавить?", reply_markup=kb.get_add_type_keyboard())
    return States.CHOOSE_TYPE

async def add_record_type_chosen(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info("--- In Conversation: add_record_type_chosen ---")
    query = update.callback_query
    await query.answer()
    flow = query.data.split('_')[-1]
    context.user_data['flow'] = flow
    context.user_data['messages_to_delete'] = [query.message.message_id] 
    text_prompt = "Введите имя или название, кому ВЫ должны:" if flow == 'debt' else "Введите имя человека, который ВАМ должен:"
    sent_message = await query.message.reply_text(text_prompt)
    context.user_data['messages_to_delete'].append(sent_message.message_id)
    return States.ADD_NAME

async def add_record_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info("--- In Conversation: add_record_name ---")
    context.user_data['name'] = update.message.text
    context.user_data['messages_to_delete'].append(update.message.message_id)
    sent_message = await update.message.reply_text("Отлично! Теперь введите сумму:")
    context.user_data['messages_to_delete'].append(sent_message.message_id)
    return States.ADD_AMOUNT

async def add_record_amount(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info("--- In Conversation: add_record_amount ---")
    context.user_data['messages_to_delete'].append(update.message.message_id)
    try:
        amount = float(update.message.text.replace(',', '.'))
        if amount <= 0:
            sent_message = await update.message.reply_text("Сумма должна быть > 0. Введите еще раз:")
            context.user_data['messages_to_delete'].append(sent_message.message_id)
            return States.ADD_AMOUNT
        context.user_data['amount'] = amount
        sent_message = await update.message.reply_text("Принято. Дата возврата (ДД.ММ.ГГГГ):")
        context.user_data['messages_to_delete'].append(sent_message.message_id)
        return States.ADD_DATE
    except ValueError:
        sent_message = await update.message.reply_text("Неверный формат. Введите число:")
        context.user_data['messages_to_delete'].append(sent_message.message_id)
        return States.ADD_AMOUNT

async def add_record_date(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info("--- In Conversation: add_record_date ---")
    context.user_data['messages_to_delete'].append(update.message.message_id)
    date_text = update.message.text
    try:
        datetime.strptime(date_text, "%d.%m.%Y")
        context.user_data['due_date'] = date_text
        flow = context.user_data['flow']
        name = context.user_data['name']
        amount = context.user_data['amount']
        person_type = "Кому" if flow == 'debt' else "Кто"
        sent_message = await update.message.reply_text(
            f"Проверьте данные:\n\n{person_type}: *{name}*\nСумма: *{amount}* руб.\nДата: *{date_text}*\n\nВсё верно?",
            reply_markup=kb.get_confirmation_keyboard(flow), parse_mode='Markdown')
        context.user_data['messages_to_delete'].append(sent_message.message_id)
        return States.ADD_CONFIRMATION
    except ValueError:
        sent_message = await update.message.reply_text("Неверный формат. Введите дату как ДД.ММ.ГГГГ.")
        context.user_data['messages_to_delete'].append(sent_message.message_id)
        return States.ADD_DATE

async def add_record_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info("--- In Conversation: add_record_confirm ---")
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    name = context.user_data['name']
    amount = context.user_data['amount']
    due_date = context.user_data['due_date']
    if context.user_data['flow'] == 'debt':
        db.add_debt(user_id, name, amount, due_date)
    else:
        db.add_receivable(user_id, name, amount, due_date)
    
    chat_id = query.message.chat_id
    for msg_id in context.user_data.get('messages_to_delete', []):
        try:
            await context.bot.delete_message(chat_id=chat_id, message_id=msg_id)
        except Exception: pass
    
    await context.bot.send_message(chat_id, "✅ Запись успешно добавлена!\n\nГлавное меню:", reply_markup=kb.get_main_menu_keyboard())
    context.user_data.clear()
    return ConversationHandler.END

# --- Диалог частичного погашения ---
async def repay_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info("--- Triggered repay_start (Conversation) ---")
    query = update.callback_query
    await query.answer()
    
    parts = query.data.split('|')
    _, flow, name, *created_at_parts = parts
    created_at = " ".join(created_at_parts)
    
    context.user_data['repay_flow'] = flow
    repay_id = (query.from_user.id, name, created_at)
    context.user_data['repay_id'] = repay_id
    
    debt_info = db.get_debt_by_id(repay_id) if flow == 'debt' else db.get_receivable_by_id(repay_id)
    if not debt_info:
        await query.edit_message_text("Ошибка: долг не найден.")
        return ConversationHandler.END
        
    context.user_data['current_amount'] = debt_info[0]
    context.user_data['menu_message_id'] = query.message.message_id

    prompt_text = "Введите сумму, которую вы погасили:" if flow == 'debt' else "Введите сумму, которую вам вернули:"
    await query.edit_message_text(f"Текущий долг: *{debt_info[0]}* руб.\n\n{prompt_text}", parse_mode='Markdown')
    return States.REPAY_AMOUNT

async def repay_amount(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info("--- In Conversation: repay_amount ---")
    try:
        repay_amount = float(update.message.text.replace(',', '.'))
        current_amount = context.user_data['current_amount']
        
        if not (0 < repay_amount <= current_amount):
            await update.message.reply_text(f"Сумма должна быть > 0 и не > {current_amount} руб.")
            return States.REPAY_AMOUNT
        
        new_amount = round(current_amount - repay_amount, 2)
        flow = context.user_data['repay_flow']
        debt_id = context.user_data['repay_id']
        
        await update.message.delete()
        
        final_text = ""
        if new_amount == 0:
            if flow == 'debt': db.delete_debt(debt_id)
            else: db.delete_receivable(debt_id)
            final_text = "✅ Долг полностью закрыт!"
        else:
            if flow == 'debt': db.update_debt_amount(debt_id, new_amount)
            else: db.update_receivable_amount(debt_id, new_amount)
            final_text = f"✅ Сумма учтена! Остаток долга: *{new_amount}* руб."
        
        menu_message_id = context.user_data.get('menu_message_id')
        await context.bot.edit_message_text(
            chat_id=update.effective_chat.id,
            message_id=menu_message_id,
            text=f"{final_text}\n\nГлавное меню:",
            reply_markup=kb.get_main_menu_keyboard(),
            parse_mode='Markdown'
        )
        context.user_data.clear()
        return ConversationHandler.END
        
    except ValueError:
        await update.message.reply_text("Неверный формат. Введите число.")
        return States.REPAY_AMOUNT

# --- Отмена диалогов ---
async def main_menu_from_conv(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info("--- Cancelling conversation and returning to main menu ---")
    query = update.callback_query
    await query.answer()
    
    chat_id = query.message.chat_id
    for msg_id in context.user_data.get('messages_to_delete', []):
        try:
            await context.bot.delete_message(chat_id=chat_id, message_id=msg_id)
        except Exception: pass
            
    context.user_data.clear()
    await query.edit_message_text(text="Действие отменено. Главное меню:", reply_markup=kb.get_main_menu_keyboard())
    return ConversationHandler.END
    
async def cancel_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info("--- Cancelling conversation with /cancel ---")
    context.user_data.clear()
    await update.message.reply_text("Действие отменено. Чтобы начать заново, введите /start.")
    return ConversationHandler.END

# --- Навигация по спискам и управление долгами ---
async def list_navigation_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = query.from_user.id
    
    parts = data.split('|')
    action = parts[0]

    if action == "creditor":
        name = parts[1]
        records = db.get_debts_by_creditor(user_id, name)
        await query.edit_message_text(f"Ваши долги *{name}*:", reply_markup=kb.get_records_keyboard('debt', name, records), parse_mode='Markdown')

    elif action == "debtor":
        name = parts[1]
        records = db.get_receivables_by_debtor(user_id, name)
        await query.edit_message_text(f"Долги от *{name}*:", reply_markup=kb.get_records_keyboard('receivable', name, records), parse_mode='Markdown')
    
    elif action == "view_debt":
        name, *created_at_parts = parts[1:]
        created_at = " ".join(created_at_parts)
        debt_info = db.get_debt_by_id((user_id, name, created_at))
        if debt_info:
            amount, due_date = debt_info
            days_left = get_days_left(due_date)
            text = (f"Кому: *{name}*\n"
                    f"Сумма: *{amount}* руб.\n"
                    f"Вернуть до: *{due_date}*\n"
                    f"Осталось: *{days_left}*")
            await query.edit_message_text(text, reply_markup=kb.get_debt_management_keyboard(name, created_at), parse_mode='Markdown')

    elif action == "view_receivable":
        name, *created_at_parts = parts[1:]
        created_at = " ".join(created_at_parts)
        receivable_info = db.get_receivable_by_id((user_id, name, created_at))
        if receivable_info:
            amount, due_date = receivable_info
            days_left = get_days_left(due_date)
            text = (f"Кто: *{name}*\n"
                    f"Сумма: *{amount}* руб.\n"
                    f"Вернет до: *{due_date}*\n"
                    f"Осталось: *{days_left}*")
            await query.edit_message_text(text, reply_markup=kb.get_receivable_management_keyboard(name, created_at), parse_mode='Markdown')

    elif action == "close":
        flow, name, *created_at_parts = parts[1:]
        created_at = " ".join(created_at_parts)
        
        if flow == "debt":
            db.delete_debt((user_id, name, created_at))
            await query.answer("✅ Долг погашен!", show_alert=True)
            await my_debts_menu(update, context)
        else: # receivable
            db.delete_receivable((user_id, name, created_at))
            await query.answer("✅ Долг отмечен как возвращенный!", show_alert=True)
            await their_debts_menu(update, context)