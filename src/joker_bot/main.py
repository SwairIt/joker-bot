from core.dispatcher import dp, bot
import asyncio

from database.engine import create_db


async def on_startup(bot):
    await create_db()

async def main() -> None: 
    dp.startup.register(on_startup)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())