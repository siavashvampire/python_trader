from app.quotex.quotexapi.ws.chanels.base import Base
import app.quotex.quotexapi.constants as OP_code
import app.quotex.quotexapi.global_value as global_value
import json
class Ping_To_Server(Base):
    def __call__(self):
        self.send_websocket_request("""42["tick"]""")
class Ping_To_Server_2(Base):
    def __call__(self):
        self.send_websocket_request("""2""")