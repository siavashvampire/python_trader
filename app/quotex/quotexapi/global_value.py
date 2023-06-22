 
check_websocket_if_connect={}#None
# try fix ssl.SSLEOFError: EOF occurred in violation of protocol (_ssl.c:2361)
ssl_Mutex={}

#
 
#if false websocket can sent self.websocket.send(data)
#else can not sent self.websocket.send(data)



SSID={}#None

check_websocket_if_error={}#False
websocket_error_reason={}#None

balance_id={}#None
account_mode_isDemo={}#practice is 1, real is 0 (int)
check_auth_finish={}
balance={}

real_balance={}
practice_balance={}

client_callback=None
auth_send_count={}
req_mutex={}#True or object_id
req_id={}

def get_req_id(object_id):
    req_mutex[object_id].acquire()
    get_req_id=req_id[object_id]
    req_id[object_id]=req_id[object_id]+1
    req_mutex[object_id].release()

    return str(get_req_id)
def get_quotex_net(cookie_token,SESSION_HEADER):
    import requests
    import urllib.parse
    headers=SESSION_HEADER
    r=requests.head("https://quotex.com/",allow_redirects=True,headers=headers,cookies=cookie_token)
    return urllib.parse.urlparse(r.url).netloc


quotex_netloc=None
websocket_url=[
    "wss://api-asia.qxbroker.com:8095/socket.io/?EIO=3&transport=websocket",
    "wss://api-hk.qxbroker.com:8095/socket.io/?EIO=3&transport=websocket",
    "wss://api-fr.qxbroker.com:8095/socket.io/?EIO=3&transport=websocket",
    "wss://api-sg2.qxbroker.com:8095/socket.io/?EIO=3&transport=websocket",
    "wss://api-in.qxbroker.com:8095/socket.io/?EIO=3&transport=websocket",
    "wss://api-in2.qxbroker.com:8095/socket.io/?EIO=3&transport=websocket",
    
    "wss://api-msk.qxbroker.com:8095/socket.io/?EIO=3&transport=websocket",
    "wss://api-fin.qxbroker.com:8095/socket.io/?EIO=3&transport=websocket",
    "wss://api-l.qxbroker.com:8095/socket.io/?EIO=3&transport=websocket",
    "wss://api-c.qxbroker.com:8095/socket.io/?EIO=3&transport=websocket",
    "wss://api-sc.qxbroker.com:8095/socket.io/?EIO=3&transport=websocket",
    "wss://api-asia2.qxbroker.com:8095/socket.io/?EIO=3&transport=websocket",
    "wss://api-us2.qxbroker.com:8095/socket.io/?EIO=3&transport=websocket",
    "wss://api-us3.qxbroker.com:8095/socket.io/?EIO=3&transport=websocket",
    "wss://api-us4.qxbroker.com:8095/socket.io/?EIO=3&transport=websocket",
    "wss://api-latina2.qxbroker.com:8095/socket.io/?EIO=3&transport=websocket"
     ]