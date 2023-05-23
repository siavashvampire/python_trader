from app.country.model.country_model import CountryModel
from core.database.database import session


def get_country(id_in: int = 0, name: int = 0) -> CountryModel:
    temp = None

    if id_in != 0:
        temp: CountryModel = session.query(CountryModel).filter(CountryModel.id == id_in).first()
    elif name != "":
        temp: CountryModel = session.query(CountryModel).filter(CountryModel.name == name).first()

    if temp is not None:
        return temp

    return CountryModel()


def add_country(name: str) -> bool:
    temp = CountryModel()
    temp.name = name
    return temp.insert()


def get_all_country() -> list[CountryModel]:
    return session.query(CountryModel).all()
