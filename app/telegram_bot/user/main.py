from telegram import Update, Message
from telegram.ext import ContextTypes

from app.telegram_bot.user.api import get_user
from core.config.Config import bot_admin_id


async def without_access_user(update: Update, context: ContextTypes) -> None:
    admin_user = get_user(id_in=bot_admin_id[0])

    await update.effective_message.reply_html(
        rf"you dont have access to bot please contact {admin_user.mention_html()} to give you access")
