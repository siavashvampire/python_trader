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


def get_all_trading() -> list[LogModel]:
    return session.query(LogModel).all()
