from aiogram import Router, types
from aiogram.filters import CommandStart


router = Router()


@router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer("Добро пожаловать в Анекдот Мастер")