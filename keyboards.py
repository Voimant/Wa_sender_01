from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


main_menu_button = [
    [InlineKeyboardButton(text='Начать рассылку', callback_data='begin_send')],
    [InlineKeyboardButton(text='Скачать статистику', callback_data='upload_static')]
]


main_menu_markup = InlineKeyboardMarkup(inline_keyboard=main_menu_button)

sender_keys = [
    [InlineKeyboardButton(text='Загрузить файл с контактами', callback_data='upload_file')],
    [InlineKeyboardButton(text='Текстовая рассылка', callback_data='text_mess')],
    [InlineKeyboardButton(text='С картинкой', callback_data='with_pict')],
    [InlineKeyboardButton(text='С видео', callback_data='with_video')]
]

sender_keys_markup = InlineKeyboardMarkup(inline_keyboard=sender_keys)

send_cancel_button = [[
    InlineKeyboardButton(text='Отправить', callback_data='send'),
    InlineKeyboardButton(text='Отмена', callback_data='cancel')
]]
send_cancel_markup = InlineKeyboardMarkup(inline_keyboard=send_cancel_button)

cancel_button = [[InlineKeyboardButton(text="Отмена", callback_data='cancel')]]
cancel_markup = InlineKeyboardMarkup(inline_keyboard=cancel_button)


