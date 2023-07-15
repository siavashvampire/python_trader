from app.ResourcePath.app_provider.admin.main import resource_path
import os
from tinydb import TinyDB
import hashlib

config_path = "../../File/Config/"
config_db_name = 'config.json'
config_table_name = 'config'

developer = 1

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

# Start  Developer Config
if developer:
    developer_config = hashlib.md5(b'VamPire1468').digest()
else:
    developer_config = ""

config_db.update({"developer_config": str(developer_config)})
# end  Developer Config

print("config Create Successfully")
