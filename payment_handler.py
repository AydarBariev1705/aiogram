from aiogram import Bot
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils import clear_cart, add_to_exel, get_cart, set_total_cost
from config import PAYMENT_TOKEN
from handlers import HandlerState
from keyboards import main_keyboard, to_main
from aiogram.fsm.context import FSMContext


async def order(callback: CallbackQuery, state: FSMContext):
    await state.set_state(HandlerState.payment)
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(
            text=f"Pay", pay=True
        )
    )
    keyboard.add(to_main)
    cart = await get_cart(tg_id=callback.from_user.id,)
    total_cost, msg = await set_total_cost(cart)

    await callback.bot.send_invoice(
        chat_id=callback.from_user.id,
        title='Order title',
        description='Order description',
        payload='Payment trough bot',
        provider_token=PAYMENT_TOKEN,
        currency='rub',
        prices=[
            LabeledPrice(
                label='Total cost',
                amount=total_cost * 100,
            )
        ],
        photo_url='https://ilogteh.ru/wp-content/uploads/2017/06/oplata-tovara-dlya-eksporta.jpg',
        photo_size=100,
        photo_width=800,
        photo_height=450,
        need_name=True,
        need_phone_number=True,
        need_shipping_address=True,
        request_timeout=15,
        is_flexible=False,
        reply_markup=keyboard.adjust(2).as_markup()
    )


async def process_pre_checkout_query(pre_checkout: PreCheckoutQuery, bot: Bot):
    print('Checking order')
    await bot.answer_pre_checkout_query(pre_checkout.id, ok=True)


async def successful_payment(message: Message, bot: Bot, state: FSMContext):
    msg = (f'Thank you for your order! Total cost {message.successful_payment.total_amount // 100} '
           f'{message.successful_payment.currency}')

    await add_to_exel(message.successful_payment.dict())
    await clear_cart(message.from_user.id)
    await bot.send_message(message.from_user.id, text=msg, reply_markup=main_keyboard())
    await state.clear()
