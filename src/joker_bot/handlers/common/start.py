from aiogram import Router, types, F
from aiogram.filters import CommandStart, or_f

from filters.chat_types import ChatTypeFilter

from kbds.inline import jokes_kbd
from kbds.reply import start_kbd


router = Router()

router.message.filter(ChatTypeFilter(["private"]))


@router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer("Добро пожаловать в Анекдот Мастер! Выберите пункт меню 😜", reply_markup=start_kbd())


@router.message(F.text == "Анекдоты")
async def jokes_cmd(message: types.Message):
    await message.answer('Выберите что хотите сделать 😀', reply_markup=jokes_kbd())


@router.message(F.text == "О боте")
async def about(message: types.Message):
    await message.answer('Лучший бот 😀\n<b><i>by @HiL1ne</i></b>')


@router.callback_query(or_f(F.data == "white_joke", F.data == "black_joke", F.data == "top_jokes"))
async def joke_cmd(callback: types.CallbackQuery):

    await callback.answer()
    await callback.message.answer(f"Я задолбался эту фигню делать! 😭")


# @router.callback_query(F.data == "jokes")
# async def jokes(callback: types.CallbackQuery):
#     await callback.answer('Вы выбрали пункт "анекдоты"')
#     await callback.message.answer("Выберите что хотите сделать 😀", reply_markup=jokes_kbd())