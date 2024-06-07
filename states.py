from aiogram.fsm.state import StatesGroup, State


class HandlerState(StatesGroup):
    """Класс состояний"""
    payment = State()


class Newsletter(StatesGroup):
    """Класс состояний для рассылок"""
    message = State()
