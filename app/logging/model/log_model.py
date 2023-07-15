from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy import insert

# from app.market_trading.api import get_trading
from core.database.Base import Base
from core.database.database import session, engine
from datetime import datetime

table_name = 'log'


class LogModel(Base):
    """
        log model that save logs in database
    """
    __tablename__ = table_name

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    user_id = Column(ForeignKey("users.id"))
    trading_id = Column(ForeignKey("trading.id"))
    title = Column(ForeignKey("log_title.id"))
    text = Column(String(1000))
    insert_time = Column(DateTime, default=datetime.now)

    user_rel = relationship("UserModel", foreign_keys=[user_id])
    trading_rel = relationship("TradingModel", foreign_keys=[trading_id])
    title_rel = relationship("LogTitleModel", foreign_keys=[title])

    def __init__(self, id: int = 0, user_id: int = 0, trading_id: int = 0, title: int = 0, text: str = "") -> None:
        try:
            if id != 0:
                temp: LogModel = session.query(LogModel).filter(LogModel.id == id).first()
            else:
                raise

            self.id = temp.id
        except:
            self.id = 0
            self.user_id = user_id
            self.trading_id = trading_id
            self.title = title
            self.text = text

        Base.__init__(self)

    def __repr__(self):
        if self.user_rel is not None:
            return "<Log(%r, %r, %r, %r)>" % (
                self.user_rel.first_name, self.trading_rel.currency_disp(), self.title_rel.name, self.text)
        else:
            return "<Log(%r, %r, %r, %r,%r)>" % (
                self.user_id, self.trading_id, self.title, self.text, self.id)

    def insert(self) -> bool:
        """
            Insert log to a database
        :return:
            True if insert correctly
            False if insert goes wrong
        """
        try:
            engine.dispose()
            stmt = insert(LogModel).values(user_id=self.user_id, trading_id=self.trading_id, title=self.title,
                                           text=self.text)
            with engine.connect() as conn:
                conn.execute(stmt)
                conn.commit()
            # session.add(self)
            # session.commit()
            return True
        except:
            return False
