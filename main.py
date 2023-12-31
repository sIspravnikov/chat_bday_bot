import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config_reader import config
from handlers import common, birthday, start, auth


async def main():
   logging.basicConfig(
      level=logging.INFO,
      format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
   )
   dispatcher = Dispatcher(storage=MemoryStorage())
   bot = Bot(config.bot_token.get_secret_value())

   dispatcher.include_router(start.router)
   dispatcher.include_router(common.router)
   dispatcher.include_router(birthday.router)
   dispatcher.include_router(auth.router)

   await dispatcher.start_polling(bot)


if __name__ == '__main__':
   asyncio.run(main())