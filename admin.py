from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.markdown import text
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, FSInputFile
from aiogram.filters import Command, CommandStart, Filter
from sqlalchemy import select

from config import CHAT_ID
from database import async_session
from keyboards import main_keyboard, categories_keyboard, subcategories_keyboard
from models import Product
from utils import get_users
from config import ADMIN_ID

admin = Router()


class Newsletter(StatesGroup):
    message = State()
    # confirmm = State()


class AdminProtect(Filter):
    async def __call__(self, message: Message):
        return message.from_user.id in ADMIN_ID


@admin.message(AdminProtect(), Command('newsletter'))
async def newsletter(message: Message, state: FSMContext):
    await state.set_state(Newsletter.message)
    await message.answer('Send message to Users')


@admin.message(AdminProtect(), Command('apanel'))
async def apanel(message: Message, ):
    await message.answer('Available commands: /newsletter')


@admin.message(AdminProtect(), Newsletter.message)
async def newsletter_message(message: Message, state: FSMContext):
    await message.answer('Wait...Sending begins')
    for user in await get_users():
        try:
            await message.send_copy(chat_id=user.tg_id)
        except:
            pass
    await message.answer('Sending completed successfully')
    await state.clear()
