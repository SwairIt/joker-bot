from string import punctuation

from aiogram.filters import Command
from aiogram import F, types, Router, Bot

from filters.chat_types import ChatTypeFilter

group_router = Router()
group_router.message.filter(ChatTypeFilter(['group', 'supergroup']))
group_router.edited_message.filter(ChatTypeFilter(['group', 'supergroup']))


@group_router.message(Command("admin"))
async def get_admins(message: types.Message, bot: Bot):
    chat_id = message.chat.id
    admins_list = await bot.get_chat_administrators(chat_id)
    admins_list = [
        member.user.id
        for member in admins_list
        if member.status == "creator" or member.status == "administrator"
    ]
    bot.my_admins_list = admins_list
    if message.from_user.id in admins_list:
        await message.delete()


def clean_text(text: str):
    return text.translate(str.maketrans('', '', punctuation))