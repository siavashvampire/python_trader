from sqlalchemy import Column, String, Integer, BigInteger, DateTime, Boolean

from core.database.Base import Base
from core.database.database import session
from datetime import datetime


class UserDB(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True, autoincrement=True, unique=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    admin_check_flag = Column(Boolean, default=0)
    insert_time = Column(DateTime, default=datetime.now)

    def __init__(self, id: int = 0, first_name: str = "", last_name: str = "") -> None:
        try:
            temp: UserDB = session.query(UserDB).filter(UserDB.id == id).first()
            self.id = temp.id
            self.first_name = temp.first_name
            self.last_name = temp.last_name
            self.admin_check_flag = temp.admin_check_flag
        except:
            self.id = id
            self.first_name = first_name
            self.last_name = last_name
            self.admin_check_flag = 0

        Base.__init__(self)

    def insert_user(self) -> bool:
        temp: UserDB = session.query(UserDB).filter(UserDB.id == self.id).first()
        if temp is not None:
            return False
        try:
            session.add(self)
            session.commit()
            return True
        except:
            return False

    def check_exist_user(self) -> bool:
        temp: UserDB = session.query(UserDB).filter(UserDB.id == self.id).first()
        if temp is not None:
            return True
        return False

    def check_admin(self) -> bool:
        return self.first_name == 'trading_bot' and self.last_name == 'AvidMech'

    def __repr__(self):
        return "<User(%r, %r)>" % (self.first_name, self.id)
