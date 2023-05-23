from app.country.model.country_model import CountryModel
from app.logging.model.log_model import LogModel
from app.market_trading.api import get_trading
from app.user.api import get_user
from core.database.database import session


def get_log(id_in: int = 0) -> LogModel:
    temp = None

    if id_in != 0:
        temp: LogModel = session.query(LogModel).filter(LogModel.id == id_in).first()

    if temp is not None:
        return temp

    return LogModel()


def get_log_by_user(telegram_id: int = 0, user_id: int = 0) -> list[LogModel]:
    if user_id == 0:
        user = get_user(id_in=telegram_id)
        user_id = user.user_id
    return session.query(LogModel).filter(LogModel.user_id == user_id).all()


def add_log(user_id: int, trading_id: int, predict: int) -> bool:
    temp = LogModel()
    trading = get_trading(trading_id)
    temp.user_id = user_id
    temp.trading_id = trading.id
    temp.country_from = trading.country_from
    temp.country_to = trading.country_to
    temp.predict = predict
    return temp.insert()


def get_all_trading() -> list[LogModel]:
    return session.query(LogModel).all()
