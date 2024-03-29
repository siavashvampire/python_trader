from app.ResourcePath.app_provider.admin.main import resource_path
import os
from tinydb import TinyDB

from app.data_connector.model.enums import APIUsed
from core.config.Config import fernet

config_path = "../../File/Config/"
config_db_name = 'config.json'
config_table_name = 'config'

developer = False

os.makedirs(resource_path(config_path), exist_ok=True)

config_db_path = resource_path(config_path + config_db_name)
config_db = TinyDB(config_db_path)
config_db.drop_tables()
config_db = TinyDB(config_db_path).table(config_table_name)

# start format Config
time_format = '%Y-%m-%d %H:%M:%S'

config_db.insert({"time_format": str(time_format)})
# end  format Config

# Start System Config
logout_time = 3600

config_db.update({"logout_time": str(logout_time)})
# end System Config


# Start  DB Config
if developer:
    db_username = 'Siavash'
    db_password = 'VamPire1468'
else:
    db_username = 'root'
    db_password = 'AAaa1234'

db_name = 'test'
costumer = 'avidMech'
remove_db_flag = 1

config_db.update({"db_username": str(db_username)})
config_db.update({"db_password": str(db_password)})
config_db.update({"db_name": str(db_name)})
config_db.update({"costumer": str(costumer)})
config_db.update({"remove_db_flag": str(remove_db_flag)})
# end  DB Config

# Start connector api Config
if developer:
    user_name_quotex = b"avidmechco@gmail.com"
    password_quotex = b"titometi2"
else:
    user_name_quotex = b"eng.tit0@yahoo.com"
    password_quotex = b"titometi2"

api_used = APIUsed().quotex
user_name_quotex = fernet.encrypt(user_name_quotex)
password_quotex = fernet.encrypt(password_quotex)

config_db.update({"api_used": api_used})
config_db.update({"user_name_quotex": user_name_quotex.decode('utf-8')})
config_db.update({"password_quotex": password_quotex.decode('utf-8')})

# end connector api Config


# start telegram config
if developer:
    token_telegram = b"5911882360:AAFQABCYQXObbISk4BGe4DE-_Vtxn39uQ1I"
else:
    token_telegram = b"6328974072:AAEPZhYsr1nZVAYHWUbGUrFIhHJyVvfFvkk"

token_telegram = fernet.encrypt(token_telegram)
config_db.update({"token_telegram": token_telegram.decode('utf-8')})

run_telegram_flag = True
config_db.update({'run_telegram_flag': run_telegram_flag})

bot_admin_id = [99981475]
config_db.update({'bot_admin_id': bot_admin_id})

telegram_channel_id = -1001835626804
config_db.update({'telegram_channel_id': telegram_channel_id})
# end telegram config


# Start  Developer Config
if developer:
    developer_config = fernet.encrypt(b"VamPire1468").decode('utf-8')
else:
    developer_config = ""
    developer_config = fernet.encrypt(b"VamPire1468").decode('utf-8')

config_db.update({"developer_config": str(developer_config)})


# end  Developer Config

print("config Create Successfully")
