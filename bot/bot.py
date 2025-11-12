import asyncio
import os
import signal
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.keyboard import InlineKeyboardBuilder
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz

from keyboards.main_menu import main_menu
from keyboards.invite_menu import invite_menu
from keyboards.notify_menu import notify_menu
from services.api_client import create_invite, activate_invite, get_upcoming_events, get_upcoming_birthdays
from services.store import SubscriberStore

# -------------------------------
# НАСТРОЙКИ
# -------------------------------
logging.basicConfig(level=logging.INFO)
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
MANAGER_IDS = set(int(x) for x in os.getenv("MANAGER_IDS", "").split(",") if x.strip().isdigit())
WEBAPP_URL = os.getenv("WEBAPP_URL", "https://gladiator-fest.ru")
store = SubscriberStore()

# -------------------------------
# FSM для Invite
# -------------------------------
class InviteForm(StatesGroup):
    dept = State()
    fname = State()
    lname = State()
    username = State()
    expire = State()
async def start(message: types.Message):
    await message.answer(
        "👋 Привет! Это корпоративный бот. Здесь можно:\n"
        "• Получить доступ в MiniApp\n"
        "• Управлять инвайт-ключами\n"
        "• Настроить уведомления о событиях и днях рождения\n\n"
        "Выберите действие ниже 👇",
        reply_markup=main_menu
    )

# Меню
async def menu_nav(callback: types.CallbackQuery):
    data = callback.data
    if data == "menu:main":
        await callback.message.edit_text("📋 Главное меню:", reply_markup=main_menu)
    elif data == "menu:invites":
        await callback.message.edit_text("🧩 Управление инвайт-ключами:", reply_markup=invite_menu)
    elif data == "menu:notify":
        await callback.message.edit_text("🔔 Настройки уведомлений:", reply_markup=notify_menu)
    elif data == "menu:help":
        await callback.message.edit_text(
            "ℹ️ Помощь:\n\n"
            "• 🧩 Инвайт-ключи — для добавления сотрудников.\n"
            "• 🧭 MiniApp — корпоративное приложение.\n"
            "• 🔔 Уведомления — напоминания о событиях и днях рождениях.\n\n"
            "Возврат в главное меню — кнопкой ниже.",
            reply_markup=InlineKeyboardBuilder()
                .button(text="◀️ Назад", callback_data="menu:main")
                .as_markup()
        )

# ----- Invite: Create -----
async def invite_create(callback: types.CallbackQuery, state: FSMContext):
    if callback.from_user.id not in MANAGER_IDS:
        await callback.answer("⛔ Недостаточно прав.")
        return
    await state.set_state(InviteForm.dept)
    await callback.message.edit_text("Введите ID отдела сотрудника:")

async def invite_step_dept(message: types.Message, state: FSMContext):
    await state.update_data(dept=int(message.text))
    await state.set_state(InviteForm.fname)
    await message.answer("Введите имя:")

async def invite_step_fname(message: types.Message, state: FSMContext):
    await state.update_data(fname=message.text)
    await state.set_state(InviteForm.lname)
    await message.answer("Введите фамилию:")

async def invite_step_lname(message: types.Message, state: FSMContext):
    await state.update_data(lname=message.text)
    await state.set_state(InviteForm.username)
    await message.answer("Введите username (или '-' если нет):")

async def invite_step_username(message: types.Message, state: FSMContext):
    await state.update_data(username=message.text.lstrip("@") if message.text != "-" else None)
    await state.set_state(InviteForm.expire)
    await message.answer("Введите срок действия (часов, по умолчанию 48):")

async def invite_step_expire(message: types.Message, state: FSMContext):
    data = await state.get_data()
    exp = int(message.text) if message.text.isdigit() else 48
    try:
        resp = await create_invite(
            department=data["dept"],
            first_name=data["fname"],
            last_name=data["lname"],
            telegram_username=data["username"],
            expires_in_hours=exp,
        )
        key = resp.get("key") or "<unknown>"
        await message.answer(
            f"✅ Инвайт-ключ создан:\n"
            f"👤 {data['fname']} {data['lname']}\n"
            f"🏢 Отдел: {data['dept']}\n"
            f"🕒 Срок: {exp}ч\n\n"
            f"🔑 Ключ: `{key}`",
            parse_mode=ParseMode.MARKDOWN
        )
    except Exception as e:
        await message.answer(f"❌ Ошибка создания инвайта: {e}")
    await state.clear()
    await message.answer("Возврат в меню:", reply_markup=main_menu)

# ----- Invite: Activate -----
async def invite_activate(callback: types.CallbackQuery):
    await callback.message.edit_text("Отправьте инвайт-ключ для активации:")

async def handle_key(message: types.Message):
    try:
        r = await activate_invite(message.from_user.id, message.text)
        if r.get("success"):
            await message.answer("✅ Ключ активирован! Теперь доступен MiniApp.", reply_markup=main_menu)
        else:
            await message.answer("⚠️ Ошибка: ключ недействителен.")
    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")

# ----- Notifications -----
async def notify_on(callback: types.CallbackQuery):
    await store.add(callback.from_user.id)
    await callback.answer("✅ Уведомления включены", show_alert=True)
    await callback.message.edit_text("🔔 Уведомления включены.", reply_markup=notify_menu)

async def notify_off(callback: types.CallbackQuery):
    await store.remove(callback.from_user.id)
    await callback.answer("🔕 Уведомления выключены", show_alert=True)
    await callback.message.edit_text("🚫 Уведомления выключены.", reply_markup=notify_menu)

# ----- Scheduled notifications -----
async def notify_job(bot: Bot):
    subs = await store.all()
    if not subs:
        return
    try:
        events = await get_upcoming_events(days=7)
        bdays = await get_upcoming_birthdays(days=7)
        msg = []
        if events:
            msg.append("📅 События на неделю:")
            for e in events[:5]:
                msg.append(f"• {e.get('title')} — {e.get('date')}")
        if bdays:
            msg.append("\n🎂 Дни рождения:")
            for b in bdays[:10]:
                msg.append(f"• {b.get('first_name')} {b.get('last_name')} — {b.get('birth_date')}")
        text = "\n".join(msg)
        for uid in subs:
            await bot.send_message(uid, text)
    except Exception as e:
        logging.error(f"Notify job failed: {e}")

# ----- Main -----
async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    # регистрация хэндлеров (у тебя уже есть)
    dp.message.register(start, CommandStart())
    dp.callback_query.register(menu_nav, F.data.startswith("menu:"))
    dp.callback_query.register(invite_create, F.data == "invite:create")
    dp.callback_query.register(invite_activate, F.data == "invite:activate")
    dp.message.register(invite_step_dept, InviteForm.dept)
    dp.message.register(invite_step_fname, InviteForm.fname)
    dp.message.register(invite_step_lname, InviteForm.lname)
    dp.message.register(invite_step_username, InviteForm.username)
    dp.message.register(invite_step_expire, InviteForm.expire)
    dp.message.register(handle_key, F.text)
    dp.callback_query.register(notify_on, F.data == "notify:on")
    dp.callback_query.register(notify_off, F.data == "notify:off")

    # планировщик уведомлений
    scheduler = AsyncIOScheduler(timezone=pytz.timezone("Europe/Bucharest"))
    scheduler.add_job(notify_job, CronTrigger(hour=9, minute=0), kwargs={"bot": bot})
    scheduler.start()

    # graceful shutdown
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, lambda: asyncio.create_task(bot.session.close()))

    logging.info("🚀 Bot started. Press Ctrl+C to stop.")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())


