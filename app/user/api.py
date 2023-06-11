from app.user.model.user_model import UserModel
from core.database.database import session


def get_user(id_in: int = 0, first_name: str = "", last_name: str = "") -> UserModel:
    # TODO:get fght ro id has bayad ro first and last ham bere

    # TODO:check nashode bayad check beshe

    if id_in != 0:
        temp = session.query(UserModel).filter(UserModel.id == id_in).first()
        if temp is not None:
            return temp

    if first_name != "" and last_name != "":
        temp = session.query(UserModel).filter(UserModel.first_name == first_name,
                                               UserModel.last_name == last_name).first()
        if temp is not None:
            return temp

    return UserModel(id=id_in, first_name=first_name, last_name=last_name)


def add_user(first_name: str = "", last_name: str = "") -> bool:
    return get_user(first_name=first_name, last_name=last_name).insert_user()


# TODO:check nashode bayad check beshe


def get_all_user() -> list[UserModel]:
    return session.query(UserModel).all()
    # TODO:check nashode bayad check beshe


def check_exist_user(id_in: int = 0, first_name: str = "", last_name: str = "") -> bool:
    return get_user(id_in, first_name, last_name).check_exist_user()
    # TODO:check nashode bayad check beshe
