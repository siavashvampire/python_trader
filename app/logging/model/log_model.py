from sqlalchemy import Column, Integer, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship

from app.market_trading.api import get_trading
from core.database.Base import Base
from core.database.database import session
from datetime import datetime


class LogModel(Base):
    __tablename__ = 'log'

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    user_id = Column(ForeignKey("users.id"))
    trading_id = Column(ForeignKey("trading.id"))
    country_from = Column(ForeignKey("country.id"))
    country_to = Column(ForeignKey("country.id"))
    predict = Column(Boolean, default=0)
    insert_time = Column(DateTime, default=datetime.now)

    user_rel = relationship("UserDB", foreign_keys=[user_id])
    trading_rel = relationship("TradingModel", foreign_keys=[trading_id])
    country_from_rel = relationship("CountryModel", foreign_keys=[country_from])
    country_to_rel = relationship("CountryModel", foreign_keys=[country_to])

    def __init__(self, id: int = 0, user_id: int = 0, trading_id: int = 0, predict: int = 0) -> None:
        try:
            if id != 0:
                temp: LogModel = session.query(LogModel).filter(LogModel.id == id).first()
            else:
                raise

            self.id = temp.id
        except:
            trading = get_trading(trading_id)
            self.id = 0
            self.user_id = user_id
            self.trading_id = trading_id
            self.country_from = trading.country_from
            self.country_to = trading.country_to
            self.predict = predict

        Base.__init__(self)

    def __repr__(self):
        if self.country_from_rel is not None:
            return "<Log(%r, %r, %r, %r, %r)>" % (
                self.user_rel.first_name, self.country_from_rel.name, self.country_to_rel.name, self.predict, self.id)
        else:
            return "<Log(%r, %r, %r, %r, %r)>" % (
                self.user_id, self.country_from, self.country_to, self.predict, self.id)

    def insert(self) -> bool:
        try:
            session.add(self)
            session.commit()
            return True
        except:
            return False
