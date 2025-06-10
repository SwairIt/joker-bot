from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from database.engine import session_maker

from middlewares.db import DbSessionMiddleware

from handlers.common.start import router as start_router
from handlers.common.admin import router as admin_router
from handlers.common.group import group_router

from config import settings

import logging



logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

dp = Dispatcher()
bot = Bot(
    token=settings.BOT_TOKEN.get_secret_value(),
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

bot.my_admins_list = []

dp.update.middleware.register(DbSessionMiddleware(session_maker))
dp.include_routers(start_router, admin_router, group_router)