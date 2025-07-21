# src/keyboards.py
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

def get_main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("💰 Мои долги (Я должен)", callback_data="main_my_debts")],
        [InlineKeyboardButton("💸 Мне должны", callback_data="main_their_debts")],
        [InlineKeyboardButton("➕ Добавить новую запись", callback_data="main_add_record")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_add_type_keyboard():
    keyboard = [
        [InlineKeyboardButton("Добавить свой долг", callback_data="add_type_debt")],
        [InlineKeyboardButton("Добавить долг мне", callback_data="add_type_receivable")],
        [InlineKeyboardButton("◀️ Главное меню", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_confirmation_keyboard(flow):
    keyboard = [[
        InlineKeyboardButton("✅ Да, всё верно", callback_data=f"confirm_yes_{flow}"),
        InlineKeyboardButton("❌ Нет, отмена", callback_data="main_menu")
    ]]
    return InlineKeyboardMarkup(keyboard)

def get_list_keyboard(flow, items):
    keyboard = []
    prefix = "creditor" if flow == "debt" else "debtor"
    for item in items:
        keyboard.append([InlineKeyboardButton(item, callback_data=f"{prefix}|{item}")])
    keyboard.append([InlineKeyboardButton("◀️ Главное меню", callback_data="main_menu")])
    return InlineKeyboardMarkup(keyboard)

def get_records_keyboard(flow, name, records):
    keyboard = []
    prefix = "view_debt" if flow == "debt" else "view_receivable"
    for amount, due_date, created_at in records:
        button_text = f"{amount} руб. до {due_date}"
        # ИСПРАВЛЕНИЕ: Заменяем пробел на безопасный символ '|'
        safe_created_at = created_at.replace(" ", "|")
        keyboard.append([InlineKeyboardButton(button_text, callback_data=f"{prefix}|{name}|{safe_created_at}")])
    
    back_callback = "main_my_debts" if flow == "debt" else "main_their_debts"
    keyboard.append([InlineKeyboardButton("◀️ Назад к списку", callback_data=back_callback)])
    return InlineKeyboardMarkup(keyboard)

def get_debt_management_keyboard(creditor, created_at):
    safe_created_at = created_at.replace(" ", "|")
    keyboard = [
        [InlineKeyboardButton("💰 Погасить частично", callback_data=f"repay|debt|{creditor}|{safe_created_at}")],
        [InlineKeyboardButton("✅ Погасить полностью", callback_data=f"close|debt|{creditor}|{safe_created_at}")],
        [InlineKeyboardButton("◀️ Назад к долгам", callback_data=f"creditor|{creditor}")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_receivable_management_keyboard(debtor, created_at):
    safe_created_at = created_at.replace(" ", "|")
    keyboard = [
        [InlineKeyboardButton("💰 Получена часть", callback_data=f"repay|receivable|{debtor}|{safe_created_at}")],
        [InlineKeyboardButton("✅ Долг возвращен полностью", callback_data=f"close|receivable|{debtor}|{safe_created_at}")],
        [InlineKeyboardButton("◀️ Назад к долгам этого человека", callback_data=f"debtor|{debtor}")]
    ]
    return InlineKeyboardMarkup(keyboard)