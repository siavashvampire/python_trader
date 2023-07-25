from time import sleep
from telegram import Update, Message
from telegram.ext import ContextTypes

from app.country.api import get_country
from app.logging.api import get_log_by_title
from app.market_trading.api import get_trading
from app.telegram_bot.user.api import add_user
from core.config.Config import bot_admin_id
from app.telegram_bot.core.markups.markup import get_user_accept_reject_markup

from app.telegram_bot.core.markups.markup import get_main_markup


async def start_new_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.deleteMessage(chat_id=update.effective_message.chat.id, message_id=update.effective_message.id)

    user = update.effective_message.from_user

    # noinspection PyTypeChecker
    temp_message: Message = await update.effective_message.reply_text(
        "welcome to quotex trading bot , " + user.first_name)

    flag = add_user(user)
    sleep(2)

    await context.bot.deleteMessage(chat_id=update.effective_message.chat.id, message_id=temp_message.id)

    if flag:
        chat_data = context.chat_data
        chat_data['app'] = 'user'
        chat_data['state'] = 'insert_wait_for_accept'
        await update.effective_message.reply_text("You have been added to quotex users correctly")

        await update.effective_message.reply_text("we send your user to admin for checking access")

        # await update.effective_message.reply_html(
        #     rf"you dont have access to bot plz contact {admin_user.mention_html()} to give you access")

        await context.bot.send_message(bot_admin_id[0],
                                       "user with first name " + user.first_name + "\n user = @" + user.username,
                                       reply_markup=get_user_accept_reject_markup(user.id))
    else:
        await update.effective_message.reply_text("Sorry ,we cant add you to quotex users")


async def start_exist_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.deleteMessage(chat_id=update.effective_message.chat.id, message_id=update.effective_message.id)
    user = update.effective_message.from_user

    # noinspection PyTypeChecker
    temp_message: Message = await update.effective_message.reply_text(
        "Hello " + user.first_name + ", Welcome to the qoutex")

    sleep(1)
    await context.bot.deleteMessage(chat_id=update.effective_message.chat.id, message_id=temp_message.id)

    await update.effective_message.reply_text("your already are quotex user")


async def say_start_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.effective_message.reply_text("please start bot with /start command")


async def main_app(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_data = context.chat_data
    chat_data['app'] = 'main_app'
    await context.bot.deleteMessage(chat_id=update.effective_message.chat.id, message_id=update.effective_message.id)
    await update.effective_message.reply_html("welcome", reply_markup=get_main_markup())


async def admin_system_check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_data = context.chat_data
    chat_data['app'] = 'admin_system_check'
    await context.bot.deleteMessage(chat_id=update.effective_message.chat.id, message_id=update.effective_message.id)
    await update.effective_message.reply_chat_action('choose_sticker')
    # trades = get_all_trading()
    # text = ""
    # for trade in trades:
    #     name = trade.currency_disp() + " " + trade.country_from_rel.flag_unicode + " " + trade.country_to_rel.flag_unicode
    #     win = len(get_log_by_title_by_trading(trade.id, 7))
    #     lose = len(get_log_by_title_by_trading(trade.id, 8))
    #     total = win + lose
    #     if total != 0:
    #         percent = round(win / total, 2)
    #         text_temp = "accuracy for " + name + " is : " + str(percent)
    #     else:
    #         text_temp = "no trade is logged for " + name
    #
    #     text += text_temp
    #     text += "\n"

    sleep(1)

    win = len(get_log_by_title(7))
    lose = len(get_log_by_title(8))
    sell = len(get_log_by_title(2))
    buy = len(get_log_by_title(4))

    if sell + buy != win + lose:
        await update.effective_message.reply_html(
            "total trade is not correct : win : {win}, lose : {lose}, sell : {sell}, buy : {buy}".format(win=win,
                                                                                                         lose=lose,
                                                                                                         sell=sell,
                                                                                                         buy=buy))
        return

    errors = get_log_by_title(1)

    if len(errors) > 0:
        await update.effective_message.reply_html("we have {n_error} errors in system".format(n_error = len(errors)))
        error_text = ""
        for error in errors:
            trade = get_trading(error.trading_id)
            country_from = get_country(trade.country_from)
            country_to = get_country(trade.country_to)
            currency_disp = country_from.currency + "_" + country_to.currency
            error_text += "error happened in trade " + currency_disp + " error text : " + error.text + "\n"

        await update.effective_message.reply_html(error_text)
        return

    await update.effective_message.reply_html("system all correct")
