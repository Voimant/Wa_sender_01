from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram import F, Router, Bot
from aiogram.fsm.context import FSMContext
from whatsapp_api_client_python import API

from config import TOKEN_TG, TOKEN_WA, INST
from keyboards import main_menu_markup, sender_keys_markup, send_cancel_markup, cancel_markup
from aiogram.filters.state import State, StatesGroup
from Wasender.send_wa import sender_list_number
router = Router()
bot = Bot(token=TOKEN_TG)
"""*********************ОТПРАВКА СООБЩЕНИЙ В WA ТОЛЬКО ТЕКСТ********************"""


class SendText(StatesGroup):
    input_text = State()
    send_text_mess = State()
    test_send = State()


greenAPI = API.GreenApi(INST, TOKEN_WA)


@router.callback_query(F.data == 'text_mess')
async def send_text(call: CallbackQuery, state: FSMContext):
    await call.message.answer('Введите текст рассылки', reply_markup=cancel_markup)
    await state.set_state(SendText.input_text)


@router.message(SendText.input_text)
async def  get_input_text(mess: Message, state: FSMContext):
    if mess.text is not None:
        await state.update_data(input_text=mess.text)
        await mess.answer('Введите свой номер телефона для тестовой рассылки (в формате 79991111111', reply_markup=cancel_markup)
        await state.set_state(SendText.test_send)
    else:
        await mess.answer('Что то пошло не так, убедитесь что отправили Текст', reply_markup=sender_keys_markup)
        await state.clear()


@router.message(SendText.test_send)
async def send_test_message(mess: Message, state: FSMContext):
    if mess.text.isdigit() is True:
        await state.update_data(test_send=mess)
        data = await state.get_data()
        print(mess.text)
        notif = greenAPI.serviceMethods.checkWhatsapp(f'{mess.text}')
        if notif.code == 200:
            print(notif.code)
            resp = greenAPI.sending.sendMessage(f'{mess.text}@c.us', data['input_text'])
            await mess.answer('Сообщение доставлено, проверье правильность рассылки и нажмите отправить',
                            reply_markup=send_cancel_markup)
            await state.set_state(SendText.send_text_mess)
        else:
            await mess.answer('У номера нет аккаунта', reply_markup=main_menu_markup)
            await state.clear()
    else:
        await mess.answer('что то пошло не так, проверьте правильность номера,'
                          ' должно быть 11 цифр в формате 79999999999', reply_markup=cancel_markup)
        await state.set_state(SendText.test_send)



@router.callback_query(SendText.send_text_mess)
async def send_text_wa(call: CallbackQuery, state: FSMContext):
    if call.data == 'send':
        data = await state.get_data()
        sender_list_number(data['input_text'])
        await call.message.answer('Отправка закончена', reply_markup=main_menu_markup)
        await state.clear()
    else:
        await state.clear()
        await call.message.answer('Меню', reply_markup=main_menu_markup)

