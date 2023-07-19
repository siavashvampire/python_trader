from app.country.api import get_country
from app.market_trading.model.trading_model import TradingModel
from core.database.database import session


def get_trading(id_in: int = 0) -> TradingModel:
    temp = None

    if id_in != 0:
        temp: TradingModel = session.query(TradingModel).filter(TradingModel.id == id_in).first()

    if temp is not None:
        return temp

    return TradingModel()


def get_trading_by_country_currency(currency_from: str, country_to: str) -> TradingModel:
    """
        get trade by country currency
    :param currency_from: country from currency
    :param country_to: country to currency
    :return:
        get trade or None if cant find any trade
    """
    country_from = get_country(currency=currency_from)
    country_to = get_country(currency=country_to)
    temp = None
    # country_to =
    if country_from.id != 0 and country_to.id != 0:
        temp: TradingModel = session.query(TradingModel).filter(TradingModel.country_from == country_from.id,
                                                                TradingModel.country_to == country_to.id).first()

    if temp is not None:
        return temp

    return TradingModel()


def get_all_trades_by_country_id( country_id: int) -> list[TradingModel]:
    """
        get trade by country currency
    :param currency_from: country from currency
    :param country_to: country to currency
    :return:
        get trade or None if cant find any trade
    """

    temp: list[TradingModel] = session.query(TradingModel).filter(TradingModel.country_from == country_id).all()
    temp2: list[TradingModel] = session.query(TradingModel).filter(TradingModel.country_to == country_id).all()

    temp.extend(temp2)
    return temp


def add_trading(country_from: int, country_to: int) -> bool:
    temp = TradingModel()
    temp.country_from = country_from
    temp.country_to = country_to
    return temp.insert()


def get_all_trading() -> list[TradingModel]:
    return session.query(TradingModel).all()
