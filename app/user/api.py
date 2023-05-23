from app.user.model.user_model import UserDB
from core.database.database import session


def get_user(id_in: int = 0, user_id: int = 0, user: User = None) -> UserDB:
    id_check = 0

    if id_in != 0:
        id_check = id_in

    if user is not None:
        id_check = user.id

    if id_check != 0:
        temp = session.query(UserDB).filter(UserDB.id == id_check).first()
        if temp is not None:
            return temp
    if user_id != 0:
        temp = session.query(UserDB).filter(UserDB.user_id == user_id).first()
        if temp is not None:
            return temp

    return UserDB(id=user.id, username=user.username, first_name=user.first_name,
                  last_name=user.last_name)


def add_user(user_in: User) -> bool:
    return get_user(user=user_in).insert_user()


def get_all_user() -> list[UserDB]:
    return session.query(UserDB).all()


def check_exist_user(user_in: User) -> bool:
    return get_user(user=user_in).check_exist_user()
