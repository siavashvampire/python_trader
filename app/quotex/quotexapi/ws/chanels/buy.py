 
 
from app.quotex.quotexapi.ws.chanels.base import Base
import app.quotex.quotexapi.constants as OP_code
import app.quotex.quotexapi.global_value as global_value
import json
class buy_binary(Base):
    def __call__(self,asset,amount,dir,duration,req_id,option_type=1):
        session=global_value.SSID[self.api.object_id]
        """
        42["orders/open",{"asset":"CADJPY_otc","amount":1,"time":60,"action":"put","isDemo":1,"requestId":1627137205,"optionType":100}]
        """
        data=[]
        data.append("orders/open")
        openorder={}
        #openorder["session"]=json.loads(session[2:])[1]["session"].replace("\"","\\\"")
        openorder["asset"]=asset
        openorder["amount"]=amount
        openorder["action"]=dir
        openorder["requestId"]=req_id
        openorder["isDemo"]=global_value.account_mode_isDemo[self.api.object_id]
        openorder["time"]=duration#sec
        openorder["optionType"]=option_type
        data.append(openorder)
        self.send_websocket_request("42"+str(data))
 
class cancelOrder(Base):
    def __call__(self,ticket):
        data=["orders/cancel",{"ticket":str(ticket)}]
        self.send_websocket_request("42"+str(data))
 