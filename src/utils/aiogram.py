from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import keyboard


class InlineKeyboards:
    @classmethod
    def build_button(
        cls,
        text: str,
        url: str | None = None,
        callback_data: str | None = None,
    ) -> InlineKeyboardButton:
        return InlineKeyboardButton(
            text=text,
            url=url,
            callback_data=callback_data,
        )

    @classmethod
    def build_keyboard(
        cls,
        buttons: list[list[InlineKeyboardButton]],
    ) -> keyboard.InlineKeyboardMarkup:
        return keyboard.InlineKeyboardMarkup(inline_keyboard=buttons)
