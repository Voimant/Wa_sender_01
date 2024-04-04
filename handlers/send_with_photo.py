from aiogram.types import Message, CallbackQuery
from aiogram import F, Router, Bot
from aiogram.fsm.context import FSMContext
from whatsapp_api_client_python import API

from Wasender.send_wa import sender_list_with_pict
from config import INST, TOKEN_WA, TOKEN_TG
from keyboards import main_menu_markup, sender_keys_markup, send_cancel_markup, cancel_markup
from aiogram.filters.state import State, StatesGroup

bot = Bot(token=TOKEN_TG)
router = Router()
greenAPI = API.GreenApi(INST, TOKEN_WA)

"""******************ОТПРАВКА СООБЩЕНИЙ В WA с КАРТИНКОЙ******************"""
class SendTextPict(StatesGroup):
    input_text = State()
    input_pict = State()
    sender_text_pict = State()
    test_send = State()


@router.callback_query(F.data == 'with_pict')
async def send_text(call: CallbackQuery, state: FSMContext):
    await call.message.answer('Введите текст рассылки')
    await state.set_state(SendTextPict.input_text)


@router.message(SendTextPict.input_text)
async def  get_input_text(mess: Message, state: FSMContext):
    if mess.text is not None:
        await state.update_data(input_text=mess.text)
        await mess.answer('Прикрепите картинку, текст вводить не нужно', reply_markup=cancel_markup)
        await state.set_state(SendTextPict.input_pict)
    else:
        await mess.answer('Что то пошло не так, убедитесь что отправили текст', reply_markup=sender_keys_markup)



@router.message(SendTextPict.input_pict, F.photo)
async def get_input_pict(mess: Message, state: FSMContext):
    try:
        file_i = mess.photo[-1].file_id
        file = await bot.get_file(file_i)
        await bot.download_file(file.file_path, 'send_photo.jpg')
        await state.set_state(SendTextPict.test_send)
        await mess.answer('Введите свой номер телефона для тестовой рассылки (в формате 79991111111',
                          reply_markup=cancel_markup)
    except Exception as e:
        print(e)
        await state.clear()
        await mess.answer("Что то пошло не так, попробуйте заново", reply_markup=main_menu_markup)


@router.message(SendTextPict.test_send)
async def send_test_message(mess: Message, state: FSMContext):
    if mess.text.isdigit() is True:
        await state.update_data(test_send=mess)
        data = await state.get_data()
        print(mess.text)
        notif = greenAPI.serviceMethods.checkWhatsapp(f'{mess.text}')
        if notif.code == 200:
            greenAPI.sending.sendFileByUpload(f'{mess.text}@c.us', "send_photo.jpg", "send_photo.jpg", data['input_text'])
            await mess.answer('Сообщение доставлено, проверье правильность рассылки и нажмите отправить',reply_markup=send_cancel_markup)
            await state.set_state(SendTextPict.sender_text_pict)
        else:
            await mess.answer('У номера нет аккаунта', reply_markup=main_menu_markup)
            await state.clear()

    else:
        await mess.answer('что то пошло не так, проверьте правильность номера,'
                          ' должно быть 11 цифр в формате 79999999999', reply_markup=cancel_markup)
        await state.set_state(SendTextPict.test_send)


@router.callback_query(SendTextPict.sender_text_pict)
async def get_send_with_pict(call: CallbackQuery, state: FSMContext):
    if call.data == 'send':
        data = await state.get_data()
        chat_id = call.from_user.id
        sender_list_with_pict(data['input_text'])
        data = await state.get_data()
        print(data)
        await call.message.answer("Рассылка окончена", reply_markup=main_menu_markup)
        await state.clear()
    else:
        await state.clear()
        await call.message.answer('Меню', reply_markup=main_menu_markup)





