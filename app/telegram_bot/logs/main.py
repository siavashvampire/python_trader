import os

from telegram import Update
from telegram.ext import ContextTypes

from app.country.api import get_country
from app.logging.api import get_log_by_title_by_trading, get_log_by_title
from app.market_trading.api import get_trading, get_all_trades_by_country_id, get_all_trading
from app.telegram_bot.core.markups.markup import get_ikm_trading_list, get_otc_over_all_markup, get_ikm_country_list


async def percent_currency_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query

    await update.effective_message.reply_html("please choose your currency", reply_markup=get_ikm_trading_list())
    await query.answer()


async def percent_all_currency_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    html_code = "all currency"
    await update.effective_message.reply_html(html_code, reply_markup=get_otc_over_all_markup(0))
    await query.answer()


async def percent_location_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await update.effective_message.reply_html("please choose your country", reply_markup=get_ikm_country_list())
    await query.answer()


def extract_trading_id_from_data(init_str: str, data: str) -> int:
    data = data.replace(init_str, "")

    return int(data)


async def percent_currency_show_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    data = str(query.data)
    trading_id = extract_trading_id_from_data("trading_", data)
    trading = get_trading(trading_id)
    html_code = trading.country_from_rel.flag_unicode + " " + trading.country_to_rel.flag_unicode + " " + \
                trading.country_from_rel.currency + " / " + trading.country_to_rel.currency

    await update.effective_message.reply_html(html_code, reply_markup=get_otc_over_all_markup(trading_id))
    await query.answer()


async def separate_otc_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    data = str(query.data)
    png_path = "File/temp/separate_otc_handler_" + str(update.effective_user.id) + ".png"
    trading_id = extract_trading_id_from_data("separate_otc_", data)

    if trading_id != 0:
        win = len(get_log_by_title_by_trading(trading_id, 7))
        lose = len(get_log_by_title_by_trading(trading_id, 8))

        trading = get_trading(trading_id)
        title = trading.currency_disp("/")

    else:
        win = len(get_log_by_title(7))
        lose = len(get_log_by_title(8))
        title = "all currency's"

    if win != 0 or lose != 0:
        import matplotlib.pyplot as plt

        labels = ['win , ' + str(win), 'lose , ' + str(lose)]
        sizes = [win, lose]
        colors = ["limegreen", "firebrick"]
        plt.title(title)
        plt.pie(sizes, labels=labels, colors=colors,
                autopct='%1.1f%%', shadow=True, startangle=140)
        plt.axis('equal')
        plt.savefig(png_path)
        plt.close()
        await update.effective_message.reply_photo(open(png_path, 'rb'))
        os.remove(png_path)
    else:
        await update.effective_message.reply_html("no data have insert yet")
    await query.answer()


async def over_all_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    data = str(query.data)
    png_path = "File/temp/over_all_handler_" + str(update.effective_user.id) + ".png"
    trading_id = extract_trading_id_from_data("over_all_", data)

    if trading_id != 0:
        win = len(get_log_by_title_by_trading(trading_id, 7))
        lose = len(get_log_by_title_by_trading(trading_id, 8))

        trading = get_trading(trading_id)
        title = trading.currency_disp("/")

    else:
        win = len(get_log_by_title(7))
        lose = len(get_log_by_title(8))
        title = "all currency's"

    if win != 0 or lose != 0:
        import matplotlib.pyplot as plt

        labels = ['win , ' + str(win), 'lose , ' + str(lose)]
        sizes = [win, lose]
        colors = ["limegreen", "firebrick"]
        plt.title(title)
        plt.pie(sizes, labels=labels, colors=colors,
                autopct='%1.1f%%', shadow=True, startangle=140)
        plt.axis('equal')
        plt.savefig(png_path)
        plt.close()
        await update.effective_message.reply_photo(open(png_path, 'rb'))
        os.remove(png_path)
    else:
        await update.effective_message.reply_html("no data have insert yet")
    await query.answer()


async def separate_otc_detail_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    data = str(query.data)

    trades = get_all_trading()
    text = ""
    for trade in trades:
        name = trade.currency_disp() + " " + trade.country_from_rel.flag_unicode + " " + trade.country_to_rel.flag_unicode
        win = len(get_log_by_title_by_trading(trade.id, 7))
        lose = len(get_log_by_title_by_trading(trade.id, 8))
        total = win + lose
        if total != 0:
            percent = round(win / total, 2)
            text_temp = "accuracy for " + name + " is : " + str(percent)
        else:
            text_temp = "no trade is logged for " + name

        text += text_temp
        text += "\n"

    await update.effective_message.reply_html(text)

    await query.answer()


async def over_all_detail_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    data = str(query.data)

    trades = get_all_trading()
    text = ""
    for trade in trades:
        name = trade.currency_disp() + " " + trade.country_from_rel.flag_unicode + " " + trade.country_to_rel.flag_unicode
        win = len(get_log_by_title_by_trading(trade.id, 7))
        lose = len(get_log_by_title_by_trading(trade.id, 8))
        total = win + lose
        if total != 0:
            percent = round(win / total * 100, 2)
            text_temp = "accuracy for " + name + " is : " + str(percent) + "%"
        else:
            text_temp = "no trade is logged for " + name

        text += text_temp
        text += "\n"

    await update.effective_message.reply_html(text)

    await query.answer()


async def country_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    data = str(query.data)
    png_path = "File/temp/country_handler_" + str(update.effective_user.id) + ".png"
    country_id = extract_trading_id_from_data("country_", data)
    trades = get_all_trades_by_country_id(country_id)

    win = 0
    lose = 0

    for trade in trades:
        win += len(get_log_by_title_by_trading(trade.id, 7))
        lose += len(get_log_by_title_by_trading(trade.id, 8))

    title = get_country(country_id).name

    if win != 0 or lose != 0:
        import matplotlib.pyplot as plt

        labels = ['win , ' + str(win), 'lose , ' + str(lose)]
        sizes = [win, lose]
        colors = ["limegreen", "firebrick"]
        plt.title(title)
        plt.pie(sizes, labels=labels, colors=colors,
                autopct='%1.1f%%', shadow=True, startangle=140)
        plt.axis('equal')
        plt.savefig(png_path)
        plt.close()
        await update.effective_message.reply_photo(open(png_path, 'rb'))
        os.remove(png_path)
    else:
        await update.effective_message.reply_html("no data have insert yet")
    await query.answer()
