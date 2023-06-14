from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from core.database.Base import Base

user = 'Comp_462_siavash'
password = 'VamPire1468'
host = '127.0.0.1'
port = 3306
database = 'Comp_462'


def get_connection() -> Engine:
    return create_engine(
        url="mysql://{0}:{1}@{2}:{3}/{4}".format(
            user, password, host, port, database
        )
    )


engine = get_connection()

session = sessionmaker(bind=engine)()

def create_db() -> None:
    from app.user.model.user_model import UserModel
    from app.country.model.country_model import CountryModel
    from app.candle.model.candle_model import CandleModel
    from app.market_trading.model.trading_model import TradingModel
    from app.log_title.model.log_title_model import LogTitleModel
    from app.logging.model.log_model import LogModel

    UserModel()
    CountryModel()
    CandleModel()
    TradingModel()
    LogTitleModel()
    LogModel()

    Base.metadata.create_all(engine)

    # session.add(ed_user)
