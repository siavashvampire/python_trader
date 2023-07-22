from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from app.country.api import get_all_country
from app.market_trading.api import get_all_trading


def get_user_accept_reject_markup(user_id: int) -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("accept", callback_data="user_" + str(user_id) + "_accept"),
            InlineKeyboardButton("reject", callback_data="user_" + str(user_id) + "_reject"),
        ]
    ]

    return InlineKeyboardMarkup(keyboard)


def get_otc_over_all_markup(trading_id: int) -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("separate otc", callback_data="separate_otc_" + str(trading_id)),
            InlineKeyboardButton("over all", callback_data="over_all_" + str(trading_id)),
        ]
    ]

    return InlineKeyboardMarkup(keyboard)


def get_main_markup() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("percent for a currency", callback_data="percent_currency"),
            InlineKeyboardButton("percent for a location", callback_data="percent_location"),
        ],
        [
            InlineKeyboardButton("percent for all currency", callback_data="percent_all_currency"),
            InlineKeyboardButton("percent all currency detail", callback_data="percent_all_currency_detail"),
        ]
    ]

    return InlineKeyboardMarkup(keyboard)


def get_ikm_trading_list():
    num_k_in_column = 2
    trading_list = get_all_trading()
    keyboard = []
    keyboard_temp = []

    for trading in trading_list:
        ink = InlineKeyboardButton(trading.country_from_rel.flag_unicode
                                   + " "
                                   + trading.country_to_rel.flag_unicode
                                   + " "
                                   + trading.country_from_rel.currency
                                   + " / "
                                   + trading.country_to_rel.currency
                                   , callback_data="trading_" + str(trading.id))

        keyboard_temp.append(ink)

        if len(keyboard_temp) == num_k_in_column:
            keyboard.append(keyboard_temp)
            keyboard_temp = []

    if len(keyboard_temp) != 0:
        keyboard.append(keyboard_temp)

    return InlineKeyboardMarkup(keyboard)

def get_ikm_country_list():
    num_k_in_column = 2
    country_list = get_all_country()
    keyboard = []
    keyboard_temp = []

    for country in country_list:
        ink = InlineKeyboardButton(country.flag_unicode
                                   + " "
                                   + country.name
                                   + " "
                                   + country.currency
                                   , callback_data="country_" + str(country.id))

        keyboard_temp.append(ink)

        if len(keyboard_temp) == num_k_in_column:
            keyboard.append(keyboard_temp)
            keyboard_temp = []

    if len(keyboard_temp) != 0:
        keyboard.append(keyboard_temp)

    return InlineKeyboardMarkup(keyboard)
