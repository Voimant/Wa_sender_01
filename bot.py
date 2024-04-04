import asyncio
from handlers import main_handlers, send_text, send_video, send_with_photo, upload_handlers
import start_handlers
from aiogram import Dispatcher, Bot
import logging
from config import TOKEN_TG


async def main():
    bot = Bot(token=TOKEN_TG)
    dp = Dispatcher()
    dp.include_routers(start_handlers.router, main_handlers.router,
                       send_text.router,
                       send_video.router, send_with_photo.router,
                       upload_handlers.router
                       )
    logger = logging.getLogger('test_bot')
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

