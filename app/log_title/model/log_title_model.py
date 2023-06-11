from sqlalchemy import Column, String, Integer

from core.database.Base import Base
from core.database.database import session


class LogTitleModel(Base):
    __tablename__ = 'log_title'

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String(50))

    def __init__(self, id: int = 0, name: str = "") -> None:
        try:
            if id != 0:
                temp: LogTitleModel = session.query(LogTitleModel).filter(LogTitleModel.id == id).first()
            elif name != "":
                temp: LogTitleModel = session.query(LogTitleModel).filter(LogTitleModel.name == name).first()
            else:
                raise

            self.id = temp.id
            self.name = temp.name
        except:
            self.id = 0
            self.name = ""

        Base.__init__(self)

    def __repr__(self):
        return "<LogTitle(%r, %r)>" % (self.name,  self.id)

    def insert(self) -> bool:
        try:
            session.add(self)
            session.commit()
            return True
        except:
            return False
