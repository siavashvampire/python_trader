from telegram import User

from app.telegram_bot.user.model.user_model import TelegramUser
from core.database.database import session


def get_user(id_in: int = 0, user_id: int = 0, user: User = None) -> TelegramUser:
    id_check = 0

    if id_in != 0:
        id_check = id_in

    if user is not None:
        id_check = user.id

    if id_check != 0:
        temp = session.query(TelegramUser).filter(TelegramUser.id == id_check).first()
        if temp is not None:
            return temp
    if user_id != 0:
        temp = session.query(TelegramUser).filter(TelegramUser.user_id == user_id).first()
        if temp is not None:
            return temp

    return TelegramUser(id=user.id, username=user.username, first_name=user.first_name,
                        last_name=user.last_name)


def add_user(user_in: User) -> bool:
    return get_user(user=user_in).insert_user()


def get_all_user() -> list[TelegramUser]:
    return session.query(TelegramUser).all()


def check_exist_user(user_in: User) -> bool:
    return get_user(user=user_in).check_exist_user()


def check_admin_user(user_in: User) -> bool:
    return get_user(user=user_in).check_admin()


def check_access_user(user_in: User) -> bool:
    return get_user(user=user_in).check_access()


def set_user_access(id_in: int, cond: str) -> None:
    if cond == 'accept':
        cond = 1
    else:
        cond = 0
    get_user(id_in).change_access(cond)
