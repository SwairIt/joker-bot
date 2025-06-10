from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from sqlalchemy.ext.asyncio import AsyncSession

from filters.chat_types import ChatTypeFilter

from database.orm_query import orm_get_random_joke, orm_get_jokes, orm_get_joke, orm_add_joke, orm_update_joke, orm_delete_joke
from kbds.inline import all_jokes_kbd

router = Router()

router.message.filter(ChatTypeFilter(["private"]))

@router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer("Добро пожаловать в Анекдот Мастер")
