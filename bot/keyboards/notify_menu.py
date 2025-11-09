from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

notify_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="✅ Включить", callback_data="notify:on")],
    [InlineKeyboardButton(text="🚫 Выключить", callback_data="notify:off")],
    [InlineKeyboardButton(text="◀️ Назад", callback_data="menu:main")],
])
