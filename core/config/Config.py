from app.ResourcePath.app_provider.admin.main import resource_path
import os
from tinydb import TinyDB

from app.data_connector.model.enums import APIUsed

from cryptography.fernet import Fernet

config_path = "File/Config/"
config_db_name = 'config.json'
config_table_name = 'config'

key = b'VxssvDaFQUAvJ-zQi7k3jm0HAhDzHvB4Cn_jUalWmNM='
fernet = Fernet(key)

if __name__ in ['__main__', 'core.config.Config']:
    os.makedirs(resource_path(config_path), exist_ok=True)

    config_db_path = resource_path(config_path + config_db_name)
    config_db = TinyDB(config_db_path).table(config_table_name)

    try:
        sAll = config_db.all()[0]
    except:
        sAll = {}
        print("config not found in {link} with table {table}".format(link=config_db_path, table=config_table_name))
    # sAll = ConfigTB.get(doc_id=1)

    if not len(config_db):
        print(len(config_db))
        print("import Config First")
    else:
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
        system_version = "Trader Version: 0.1"
        db_username = sAll["db_username"]
        db_password = sAll["db_password"]
        db_name = sAll["db_name"]
        costumer = sAll["costumer"]
        remove_db_flag = int(sAll["remove_db_flag"])
        # end  DB Config


        # Start API Config
        api_used = sAll["api_used"]

        user_name_quotex = fernet.decrypt(sAll["user_name_quotex"].encode("ascii")).decode('utf-8')
        password_quotex = fernet.decrypt(sAll["password_quotex"].encode("ascii")).decode('utf-8')
        # end API Config

        # Start Developer Config
        developer_config = sAll["developer_config"]

        # login_developer = False
        # if fernet.decrypt(developer_config) == b'VamPire1468':
        #     login_developer = True
        # end  Developer Config
