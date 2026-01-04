import asyncio
from loader import bot, dp
from handlers import user_handlers, fsm_handlers, stat_handlers
from database.db_sqlite import init_db


async def main():
    init_db()

    dp.include_router(fsm_handlers.router)
    dp.include_router(user_handlers.router)
    dp.include_router(stat_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
