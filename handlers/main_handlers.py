import datetime

from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from keyboards import main_menu_markup, sender_keys_markup

router = Router()


@router.message(F.text == 'Taborka32167')
async def get_auth(mess: Message):
    await mess.answer('Готовы начать рассылку?', reply_markup=main_menu_markup)



@router.callback_query(F.data == 'begin_send')
async def sender_message_whatsup(call: CallbackQuery, state: FSMContext):
    await call.message.answer('Какую отправку будем совершать?', reply_markup=sender_keys_markup)



@router.callback_query(F.data == 'upload_static')
async def upload_report(call: CallbackQuery):
    try:
        path = FSInputFile('Wasender/report.txt')
        await call.message.answer_document(document=path, caption='Отчет о неотпраленных номерах', reply_markup=main_menu_markup)
    except Exception as err:
        with open('report_erros.txt', 'a') as file:
            file.write(f'\n{str(err)} ----{datetime.date.today()}')

    try:
        path_2 = FSInputFile('Wasender/send_report.txt')
        await call.message.answer_document(document=path_2, caption='Отчет о отпраленных номерах', reply_markup=main_menu_markup)
    except Exception as err:
        with open('report_erros.txt', 'a') as file:
            file.write(f'\n{str(err)} ----{datetime.date.today()}')



