from telegram import Update
from telegram.ext import ContextTypes

from app.telegram_bot.user.api import set_user_access


async def access_query_handler(update: Update, context: ContextTypes) -> None:
    query = update.callback_query
    data = str(query.data)
    if 'user_' in data:
        data = data.replace("user_", "").split("_")
        user_id = int(data[0])
        set_user_access(user_id, data[1])
        await context.bot.send_message(user_id, "your access has changed to " + data[1])
        if data[1] == "accept":
            await context.bot.send_message(user_id, "please send some thing to me")
        await query.answer()
    else:
        await context.bot.send_message(update.effective_user.id, "command not set")
        return
