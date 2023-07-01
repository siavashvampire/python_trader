from app.country.model.country_model import CountryModel
from core.database.database import session


def get_country(id_in: int = 0, name: str = "", currency: str = "") -> CountryModel:
    """
        get country by id, name and currency
        one input is enough and the first input is chosen
    :param id_in: country id
    :param name: country name
    :param currency: country currency
    :return:
    """
    temp = CountryModel()

    if id_in != 0:
        temp: CountryModel = session.query(CountryModel).filter(CountryModel.id == id_in).first()
    elif name != "":
        temp: CountryModel = session.query(CountryModel).filter(CountryModel.name == name).first()
    elif currency != "":
        temp: CountryModel = session.query(CountryModel).filter(CountryModel.currency == currency).first()

    return temp


def add_country(name: str, currency: str = "") -> bool:
    """
        add country with name and currency
        name is required
    :param name:name of country, name is required
    :param currency:currency of country
    :return:
        boolean flag that shows that its insert correctly or not
    """
    temp = CountryModel()
    temp.name = name
    temp.currency = currency
    return temp.insert()


def get_all_country() -> list[CountryModel]:
    """
        return all of a country's list in a list
    :return:
        return list of CountryModel: list[CountryModel]
    """
    return session.query(CountryModel).all()
