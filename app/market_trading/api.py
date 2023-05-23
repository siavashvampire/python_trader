from app.country.model.country_model import CountryModel
from app.market_trading.model.trading_model import TradingModel
from core.database.database import session
from random import randint


def get_trading(id_in: int = 0) -> TradingModel:
    temp = None

    if id_in != 0:
        temp: TradingModel = session.query(TradingModel).filter(TradingModel.id == id_in).first()

    if temp is not None:
        return temp

    return TradingModel()


def add_trading(country_from: int, country_to: int) -> bool:
    temp = TradingModel()
    temp.country_from = country_from
    temp.country_to = country_to
    return temp.insert()


def get_all_trading() -> list[TradingModel]:
    return session.query(TradingModel).all()


def get_trading_predict(country_from: CountryModel, country_to: CountryModel) -> bool:
    value = randint(0, 1)
    if value == 1:
        return True

    return False
