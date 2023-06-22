from app.quotex.quotexapi.ws.chanels.base import Base
import datetime
import app.quotex.quotexapi.constants as OP_code
import time
import json
class Settings(Base): 
    def __call__(self,isFastOption=True):
       #{"name":"subscribeMessage","msg":{"name":"candle-generated","params":{"routingFilters":{"active_id":1,"size":1}}}}
        #data="""[{"t":2,"e":4,"uuid":"gg","d":[{"p":"EURUSD","tf":60}]}]"""
        true=True
        false=False
       
        while self.api.settings_list=={}:
            pass
 
        _tmp=self.api.settings_list[0]
        _tmp_dict=json.loads(_tmp["settings"])
        
        #_tmp_dict["isFastOption"]=False
        data=["settings/store",{"chartId":"graph","settings":_tmp_dict}]
        self.send_websocket_request("42"+str(data))

        