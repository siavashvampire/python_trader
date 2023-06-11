from app.log_title.model.log_title_model import LogTitleModel
from core.database.database import session


def get_log_title(id_in: int = 0, name: int = 0) -> LogTitleModel:
    temp = None

    if id_in != 0:
        temp: LogTitleModel = session.query(LogTitleModel).filter(LogTitleModel.id == id_in).first()
    elif name != "":
        temp: LogTitleModel = session.query(LogTitleModel).filter(LogTitleModel.name == name).first()

    if temp is not None:
        return temp

    return LogTitleModel()


def add_log_title(name: str) -> bool:
    temp = LogTitleModel()
    temp.name = name
    return temp.insert()


def get_all_log_title() -> list[LogTitleModel]:
    return session.query(LogTitleModel).all()
