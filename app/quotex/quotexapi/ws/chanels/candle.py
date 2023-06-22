

"""
42["loadHistoryPeriod",{"asset":"USDCAD","index":162513874160,"time":1625138122.445,"offset":1000,"period":5}]
"""
 
 
import collections
from app.quotex.quotexapi.ws.chanels.base import Base
import app.quotex.quotexapi.constants as OP_code
import app.quotex.quotexapi.global_value as global_value
import json
 
class loadHistoryPeriod(Base):
    def __call__(self,asset,time,offset,period,index):
        data=["history/load",{"asset":asset,"index":index,"time":time,"offset":offset,"period":period}]
        self.send_websocket_request("42"+str(data))
 
 
"""
42["history/load",{"asset":"AUDCAD_otc","index":162714805545,"time":1627147540.944,"offset":3000,"period":10}]
 
"""

 
class changeSymbol(Base):
    def __call__(self,asset,size,period=0):
        self.api.realtime_price[asset]=collections.deque([],size)
        data=["instruments/update",{"asset":asset,"period":period}]
        self.send_websocket_request("42"+str(data))
 
 
"""
42["unsubfor","EURRUB_otc"]
"""

class unsubfor(Base):
    def __call__(self,asset):
        data=["subfor",asset]
        self.send_websocket_request("42"+str(data))
 
 