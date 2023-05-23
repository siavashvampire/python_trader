from pyrogram import filters
from pyrogram import Client
from pyrogram.types import Message, CallbackQuery

from app.logging.api import add_log
from app.user.api import get_user
from core.pyrogram.custom_filter import user_exist_filter, dynamic_data_filter
from core.style.InlineKeyboardMarkup import get_ikm_trading_list
from app.country.api import get_country
from app.market_trading.api import get_trading_predict
from core.style.thumb import thumbs_up, thumbs_down


@Client.on_message(filters.command("get_trading") & user_exist_filter)
def get_trading_command(client: Client, message: Message):
    text = "choose your trading"

    message.reply_text(text, reply_markup=get_ikm_trading_list())


@Client.on_callback_query(dynamic_data_filter("trading_"))
async def pyrogram_data(_, query: CallbackQuery):
    data = query.data
    await query.answer()

    data_split = data.split("_")
    trading_id = int(data_split[1])
    country_from_id = int(data_split[2])
    country_to_id = int(data_split[3])

    country_from = get_country(country_from_id)
    country_to = get_country(country_to_id)

    predict = get_trading_predict(country_from, country_to)
    text = country_from.name + " / " + country_to.name + "  "

    user = get_user(id_in=query.from_user.id)
    user_id = user.user_id
    add_log(user_id, trading_id, predict)

    if predict:
        await query.message.reply_text(text+thumbs_up)
    else:
        await query.message.reply_text(text+thumbs_down)
