from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command, Filter

from states import Newsletter
from utils import get_users, create_newsletter
from config import ADMIN_ID

admin = Router()


class AdminProtect(Filter):
    """Фильтр для проверки прав администратора у пользователя"""

    async def __call__(self, message: Message):
        return message.from_user.id in ADMIN_ID


@admin.message(AdminProtect(), Command('newsletter'))
async def newsletter(message: Message, state: FSMContext):
    """Функция для начала рассылки пользователям"""
    await state.set_state(Newsletter.message)
    await message.answer('Send message to Users')


@admin.message(AdminProtect(), Command('apanel'))
async def apanel(message: Message, ):
    """ Функция для отображения доступных команд администратора"""
    await message.answer('Available commands: /newsletter')


@admin.message(AdminProtect(), Newsletter.message)
async def newsletter_message(message: Message, state: FSMContext):
    """ Функция рассылки сообщений пользователям"""
    await message.answer('Wait...Sending begins')
    tg_user_list = []
    for user in await get_users():
        try:
            await message.send_copy(
                chat_id=user.tg_id,
            )
            tg_user_list.append(user.tg_id)
        except:
            pass
    if tg_user_list:
        await create_newsletter(
            tg_user_list=tg_user_list,
            message=message.text,
        )
    await message.answer('Sending completed successfully')
    await state.clear()
