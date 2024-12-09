import aiogram
from aiogram.utils import markdown as md

from core.data import Telegram

bot = aiogram.Bot(
    token=Telegram.bot_token.to_string(),
    parse_mode=aiogram.enums.ParseMode.HTML,
)
