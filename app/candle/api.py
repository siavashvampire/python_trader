from app.candle.model.candle_model import CandleModel
from core.database.database import session


def get_candle(id_in: int = 0, name: int = 0) -> CandleModel:
    temp = None

    if id_in != 0:
        temp: CandleModel = session.query(CandleModel).filter(CandleModel.id == id_in).first()
    elif name != "":
        temp: CandleModel = session.query(CandleModel).filter(CandleModel.name == name).first()

    if temp is not None:
        return temp

    return CandleModel()


def add_candle(name: str) -> bool:
    temp = CandleModel()
    temp.name = name
    return temp.insert()


def get_all_candle() -> list[CandleModel]:
    return session.query(CandleModel).all()
