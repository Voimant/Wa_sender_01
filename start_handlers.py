from aiogram.types import Message, CallbackQuery
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from keyboards import main_menu_markup

router = Router()


@router.message(Command('start'))
async def get_cmd_start(mess: Message):
    await mess.answer('Вас приветствует Бот, для дальнейшего использования введите пароль авторизации')


@router.callback_query(F.data == 'cancel')
async def get_canc(call: CallbackQuery, state: FSMContext):
    await call.message.answer('Вернулись В главное меню', reply_markup=main_menu_markup)
    await state.clear()

@router.message(Command('cancel'))
async def get_canc(mess: Message, state: FSMContext):
    await mess.answer('Вернулись В главное меню', reply_markup=main_menu_markup)
    await state.clear()