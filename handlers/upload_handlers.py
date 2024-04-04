from aiogram.types import Message, CallbackQuery
from aiogram import F, Router, Bot
from aiogram.fsm.context import FSMContext
from whatsapp_api_client_python import API

from config import TOKEN_TG, TOKEN_WA, INST
from keyboards import main_menu_markup, sender_keys_markup, send_cancel_markup, cancel_markup
from aiogram.filters.state import State, StatesGroup
from Wasender.send_wa import sender_list_number
router = Router()

bot = Bot(token=TOKEN_TG)


class UploadFile(StatesGroup):
    upload = State()


@router.callback_query(F.data == 'upload_file')
async def  get_upload_file(call: CallbackQuery, state: FSMContext):
    await call.message.answer('Загрузите файл в формате csv', reply_markup=cancel_markup)
    await state.set_state(UploadFile.upload)


@router.message(UploadFile.upload)
async def get_upload_file(mess: Message, state: FSMContext):
    doc = mess.document.file_id
    file = await bot.get_file(doc)
    await bot.download_file(file.file_path, 'Wasender/numbers.csv')
    await mess.answer('Файл успешно загружен', reply_markup=main_menu_markup)

