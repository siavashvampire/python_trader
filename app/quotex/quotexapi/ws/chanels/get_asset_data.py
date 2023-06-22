from app.quotex.quotexapi.ws.chanels.base import Base
import datetime
import app.quotex.quotexapi.constants as OP_code
class get_asset_data(Base):
    def __call__(self,req_id):
        data=[{"t":2,"e":98,"uuid":req_id,"d":[70,73,72]}]
        self.send_websocket_request(data)