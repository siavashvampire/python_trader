from app.ResourcePath.app_provider.admin.main import resource_path
import os
from tinydb import TinyDB
import hashlib

from app.data_connector.model.enums import APIUsed

config_path = "File/Config/"
config_db_name = 'config.json'
config_table_name = 'config'

os.makedirs(resource_path(config_path), exist_ok=True)

config_db_path = resource_path(config_path + config_db_name)
config_db = TinyDB(config_db_path).table(config_table_name)

try:
    sAll = config_db.all()[0]
except:
    print("config not found in {link} with table {table}".format(link=config_db_path, table=config_table_name))
# sAll = ConfigTB.get(doc_id=1)

if not len(config_db):
    print(len(config_db))
    print("import Config First")


# start format Config
time_format = sAll["time_format"]
# end  format Config

# TODO:bayad inaro doros konim vaghti api ha omad
main_login_url = ""
main_check_user_access_url = ""
login_timeout = 30

# Start System Config
logout_time = int(sAll["logout_time"])
# end System Config


# Start  DB Config
system_version = "Trader Version: 0.0"
db_username = sAll["db_username"]
db_password = sAll["db_password"]
db_name = sAll["db_name"]
costumer = sAll["costumer"]
remove_db_flag = int(sAll["remove_db_flag"])
# end  DB Config


# Start API Config
# api_used = APIUsed().oanda
api_used = APIUsed().quotex

# end API Config

# Start Developer Config
developer_config = sAll["developer_config"]

login_developer = False
if developer_config == str(hashlib.md5(b'VamPire1468').digest()):
    login_developer = True
# end  Developer Config
