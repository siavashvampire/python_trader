from typing import Union

from app.logging.main import log_sender
from app.logging.model.log_model import LogModel
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


def get_log_by_title(title_id: Union[list[int], int]) -> list[LogModel]:
    """
        get log by title id
    :param title_id: title id
    :return:
    """
    if type(title_id) == int:
        title_id = [title_id]
    return session.query(LogModel).filter(LogModel.title.in_(title_id)).all()


def get_log_by_trading(trading_id: Union[list[int], int]) -> list[LogModel]:
    """
        get log by trading id
    :param trading_id: trading id
    :return:
    """
    if type(trading_id) == int:
        trading_id = [trading_id]
    return session.query(LogModel).filter(LogModel.trading_id.in_(trading_id)).all()


def get_log_by_title_by_trading( trading_id: Union[list[int], int],title_id: Union[list[int], int]) -> list[LogModel]:
    """
        get to log by trading id and title id
    :param title_id: title id
    :param trading_id: trading id
    :return:
    """

    if type(title_id) == int:
        title_id = [title_id]
    if type(trading_id) == int:
        trading_id = [trading_id]

    return session.query(LogModel).filter(LogModel.trading_id.in_(trading_id), LogModel.title.in_(title_id)).all()


def add_log(user_id: int, trading_id: int, title: int, text: str) -> bool:
    """
        insert log to database
    :param user_id: user id
    :param trading_id: trade id
    :param title: title id
    :param text: text
    :return:
        return boolean that shows its insert correctly or not
    """
    log_sender.log_queue.put([user_id, trading_id, title, text])
    return True


def get_all_log() -> list[LogModel]:
    """
        get all logs
    :return:
    """
    return session.query(LogModel).all()
