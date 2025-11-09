from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

invite_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="➕ Создать ключ", callback_data="invite:create")],
    [InlineKeyboardButton(text="🗝️ Активировать ключ", callback_data="invite:activate")],
    [InlineKeyboardButton(text="◀️ Назад", callback_data="menu:main")],
])
