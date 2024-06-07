from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram.filters import Command, Filter

from utils import get_users, create_newsletter
from config import ADMIN_ID

admin = Router()


class Newsletter(StatesGroup):
    message = State()


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
    tg_user_list = []
    for user in await get_users():
        try:
            await message.send_copy(chat_id=user.tg_id)
            tg_user_list.append(user.tg_id)
        except:
            pass
    if tg_user_list:
        await create_newsletter(tg_user_list=tg_user_list, message=message.text)
    await message.answer('Sending completed successfully')
    await state.clear()
