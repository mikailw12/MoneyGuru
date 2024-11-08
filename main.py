import asyncio
from aiogram import Bot, Dispatcher
from config import TOKEN
from my_handlers import router
from database import Base, engine

async def main():
    Base.metadata.create_all(engine)
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as e:
        print(f'Бот выключен, {e}')
    
