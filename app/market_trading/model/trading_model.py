from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.candle.model.candle_model import CandleModel
from app.country.model.country_model import CountryModel
from core.database.Base import Base
from core.database.database import session


class TradingModel(Base):
    __tablename__ = 'trading'

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    country_from = Column(ForeignKey("country.id"))
    country_to = Column(ForeignKey("country.id"))
    candle = Column(ForeignKey("candle.id"))

    country_from_rel = relationship("CountryModel", foreign_keys=[country_from])
    country_to_rel = relationship("CountryModel", foreign_keys=[country_to])
    candle_rel = relationship("CandleModel", foreign_keys=[candle])

    def __init__(self, id: int = 0, country_from: int = 0, country_to: int = 0) -> None:
        try:
            if id != 0:
                temp: TradingModel = session.query(TradingModel).filter(TradingModel.id == id).first()
            else:
                raise

            self.id = temp.id
            self.country_from = temp.country_from
            self.country_to = temp.country_to
        except:
            self.id = 0
            self.country_from = country_from
            self.country_to = country_to

        Base.__init__(self)

    def __repr__(self):
        if self.country_from_rel is not None:
            return "<Trading(%r,%r, %r, %r)>" % (
            self.currency_disp(), self.country_from_rel.name, self.country_to_rel.name, self.id)
        else:
            return "<Trading(%r, %r, %r)>" % (self.country_from, self.country_to, self.id)

    def insert(self) -> bool:
        try:
            session.add(self)
            session.commit()
            return True
        except:
            return False

    def currency_disp(self, between: str = "/") -> str:
        return self.country_from_rel.currency + between + self.country_to_rel.currency
