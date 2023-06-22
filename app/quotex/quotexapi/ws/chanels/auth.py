from app.quotex.quotexapi.ws.chanels.base import Base
import app.quotex.quotexapi.constants as OP_code
import app.quotex.quotexapi.global_value as global_value
import json
class auth_mode(Base):
    def __call__(self,account_mode):
        session=global_value.SSID[self.api.object_id]
        if account_mode=="REAL":
            global_value.SSID[self.api.object_id]=session.replace("\"isDemo\":1","\"isDemo\":0")
        elif account_mode=="PRACTICE":
            global_value.SSID[self.api.object_id]=session.replace("\"isDemo\":0","\"isDemo\":1")
        self.send_websocket_request(global_value.SSID[self.api.object_id])
 