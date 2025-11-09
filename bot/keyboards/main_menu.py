from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
import os

WEBAPP_URL = os.getenv("WEBAPP_URL", "https://example.com")

main_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🧭 Открыть MiniApp", web_app=WebAppInfo(url=WEBAPP_URL))],
    [InlineKeyboardButton(text="🧩 Инвайт-ключи", callback_data="menu:invites")],
    [InlineKeyboardButton(text="🔔 Уведомления", callback_data="menu:notify")],
    [InlineKeyboardButton(text="ℹ️ Помощь", callback_data="menu:help")],
])
