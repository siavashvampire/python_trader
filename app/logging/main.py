from pyrogram import filters
from pyrogram import Client
from pyrogram.types import Message

from app.logging.api import get_log_by_user
from core.pyrogram.custom_filter import user_exist_filter
from core.style.thumb import thumbs_up, thumbs_down


@Client.on_message(filters.command("get_log") & user_exist_filter)
def get_trading_command(client: Client, message: Message):
    user_id = message.from_user.id

    logs = get_log_by_user(telegram_id=user_id)

    text = ""
    for log in logs:
        country_from = log.country_from_rel
        country_to = log.country_to_rel

        text += country_from.name + " / " + country_to.name + "  "

        if log.predict:
            text += thumbs_up
        else:
            text += thumbs_down

        text += "\n"

    if text == "":
        text = "you dont have log yet"

    message.reply_text(text)
