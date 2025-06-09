from core.dispatcher import dp, bot
import asyncio

async def main() -> None: 
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())