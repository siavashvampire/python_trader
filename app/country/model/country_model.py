from sqlalchemy import Column, String, Integer

from core.database.Base import Base
from core.database.database import session


class CountryModel(Base):
    __tablename__ = 'country'

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String(50))
    short_name = Column(String(50))
    flag_unicode = Column(String(50))
    currency = Column(String(50))

    def __init__(self, id: int = 0, name: str = "") -> None:
        try:
            if id != 0:
                temp: CountryModel = session.query(CountryModel).filter(CountryModel.id == id).first()
            elif name != "":
                temp: CountryModel = session.query(CountryModel).filter(CountryModel.name == name).first()
            else:
                raise

            self.id = temp.id
            self.name = temp.name
            self.short_name = temp.short_name
            self.flag_unicode = temp.flag_unicode
            self.currency = temp.currency
        except:
            self.id = 0
            self.name = ""
            self.short_name = ""
            self.flag_unicode = ""
            self.currency = ""

        Base.__init__(self)

    def __repr__(self):
        return "<Country(%r, %r, %r)>" % (self.name, self.currency, self.id)

    def insert(self) -> bool:
        try:
            session.add(self)
            session.commit()
            return True
        except:
            return False
