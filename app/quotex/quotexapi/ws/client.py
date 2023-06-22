import json
import logging
import websocket
import app.quotex.quotexapi.constants as OP_code
import app.quotex.quotexapi.global_value as global_value
import collections
#websocket.enableTrace(True)
import time
class WebsocketClient(object):

    def __init__(self, api):

        self.api = api
        self.status=""
        self.message_clos="""451-["s_orders/close",{"_placeholder":true,"num":0}]"""
        self.message_cancel="""451-["s_orders/cancel",{"_placeholder":true,"num":0}]"""
        cookie_token=self.api.websocket_cookie
       

        self.wss = websocket.WebSocketApp(
            self.api.wss_url, on_message=self.on_message,
            on_error=self.on_error, on_close=self.on_close,
            on_open=self.on_open,header=self.api.header,cookie=cookie_token)

    def on_message(self, wss,raw_message):

        global_value.ssl_Mutex[self.api.object_id].acquire()
        logger = logging.getLogger(__name__)
        logger.debug(raw_message)
        #raw_message = json.loads(str(raw_message))
        if self.api.client_callback!= None:
            self.api.client_callback(raw_message)
        #特殊處理
        if raw_message=="40" and global_value.check_auth_finish[id(wss)]==False:
            logger.debug(global_value.SSID[self.api.object_id])
            wss.send(global_value.SSID[self.api.object_id])
            global_value.auth_send_count[self.api.object_id]=global_value.auth_send_count[self.api.object_id]+1
           
        #print(raw_message)
        if isinstance(raw_message,str):
            if  "451-" in raw_message:
                self.api._temp_status=str(raw_message)
        try:
            if self.api._temp_status=="""451-["settings/list",{"_placeholder":true,"num":0}]""":
                #print(json.loads(raw_message[1:]))
                
                self.api.settings_list=json.loads(raw_message[4:])
                self.api._temp_status=""
            elif self.api._temp_status=="""451-["history/list/v2",{"_placeholder":true,"num":0}]""":
                tt=json.loads(raw_message[1:])
                 
                self.api.candle_v2_data[tt["asset"]]=tt["history"]
                self.api._temp_status=""
        except:
            pass
            

        if raw_message=="""42["s_authorization"]""":
            global_value.check_websocket_if_connect[id(wss)] = 1
            global_value.check_auth_finish[id(wss)]=True
            pass
        
        try:
            
            ok_json=json.loads(raw_message[1:])
            try:
                if "signals" in ok_json:
                    for i in ok_json["signals"]:
                        self.api.signal_data[i[0]][i[2]]["dir"]=i[1][0]["signal"]
                        self.api.signal_data[i[0]][i[2]]["duration"]=i[1][0]["timeFrame"]
                         
                         
            except:
                pass
            try:
                if len(ok_json[0])==27:
                    self.api.updateAssets_data=ok_json
            except:
                pass    

            try:
                if len(ok_json[0])==4:
                     
                    ans={}
                    ans["time"]=ok_json[0][1]
                    ans["price"]=ok_json[0][2]
                    
                    self.api.realtime_price[ok_json[0][0]].append(ans)

                   
            except:
                pass  

            """
            b'\x04[["AUDCAD_otc",1625299325.048,0.87461]]'
            """

            if "index" in ok_json:
                self.api.getcandle_data[ok_json["index"]]=ok_json
             
            if "balance" in ok_json:
               
                if ok_json["isDemo"]==0:
                    global_value.real_balance[id(wss)]=ok_json["balance"]
                elif ok_json["isDemo"]==1:
                     
                    global_value.practice_balance[id(wss)]=ok_json["balance"]
             
            if "liveBalance" in ok_json and "demoBalance" in ok_json:
                global_value.practice_balance[id(wss)]=ok_json["demoBalance"]
                global_value.real_balance[id(wss)]=ok_json["liveBalance"]
            if "requestId" in ok_json:
                self.api.request_data[str(ok_json["requestId"])]=ok_json
            #if "ticket" in ok_json and "amount" in ok_json:
            #    self.api.check_win_refund_data[ok_json["ticket"]]=ok_json
            
             
            if self.status==self.message_clos:
                try:
                    for info in ok_json["deals"]:
                        if "id" in info and "profit" in info:
                            if info["closePrice"]!=0:
                                self.api.check_win_close_data[info["id"]]=info
                except:
                    pass
                self.status=""
            elif self.status==self.message_cancel:
                pass
                self.api.check_win_refund_data[ok_json["ticket"]]=ok_json
                self.status=""

        except:
            pass

        #input status change
        if raw_message==self.message_clos or raw_message==self.message_cancel:
            self.status=raw_message
            pass
        
        global_value.ssl_Mutex[self.api.object_id].release()
    @staticmethod
    def on_error(wss, error):
        """Method to process websocket errors."""
        logger = logging.getLogger(__name__)
        logger.error(error)
        global_value.websocket_error_reason[id(wss)] = str(error)
        global_value.check_websocket_if_error[id(wss)] = True

    @staticmethod
    def on_open(wss):
        """Method to process websocket open."""
        logger = logging.getLogger(__name__)
        logger.debug("Websocket client connected.")
        
         
         
    @staticmethod
    def on_close(wss,close_status_code,close_msg):
        """Method to process websocket close."""
        logger = logging.getLogger(__name__)
        logger.debug("Websocket connection closed.")
        global_value.check_websocket_if_connect[id(wss)] = 0
