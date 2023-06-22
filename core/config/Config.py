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

# Start  Bale Config
bale_token = sAll["bale_token"]
bale_base_url = sAll["bale_base_url"]
help_file_name = sAll["help_file_name"]
help_file_name = resource_path(help_file_name)
help_pdf_timeout = int(sAll["help_pdf_timeout"])
choose_of_bale = 1
choose_of_sms = 2
choose_of_whatsApp = 3
# end  Bale Config

# start  format Config
time_format = sAll["time_format"]
send_time_format = sAll["send_time_format"]
day_time_format = sAll["day_time_format"]
adminUnit = int(sAll["adminUnit"])
# end  format Config

# Start  PLC Config
register_for_start_read = int(sAll["register_for_start_read"])
register_for_end_read = int(sAll["register_for_end_read"])
register_for_data = int(sAll["register_for_data"])
register_for_counter = int(sAll["register_for_counter"])
register_for_test = int(sAll["register_for_test"])
disconnect_alarm_time = float(sAll["disconnect_alarm_time"])
plc_time_sleep_max = float(sAll["plc_time_sleep_max"])
plc_time_sleep_min = float(sAll["plc_time_sleep_min"])
plc_refresh_time = float(sAll["plc_refresh_time"])
plc_sleep_time_step_down = float(sAll["plc_sleep_time_step_down"])
plc_sleep_time_step_up = float(sAll["plc_sleep_time_step_up"])
time_between_read_from_each_device = float(sAll["time_between_read_from_each_device"])
# end  PLC Config

# Start  Timeouts Config
bale_get_timeout = int(sAll["bale_get_timeout"])
login_timeout = int(sAll["login_timeout"])
send_timeout = int(sAll["send_timeout"])
check_timeout = int(sAll["check_timeout"])
sensor_get_timeout = int(sAll["sensor_get_timeout"])
switch_get_timeout = int(sAll["switch_get_timeout"])
device_get_timeout = int(sAll["device_get_timeout"])
da_units_get_timeout = int(sAll["da_units_get_timeout"])
phones_get_timeout = int(sAll["phones_get_timeout"])
user_timeout = int(sAll["user_timeout"])
queue_sender_max_wait = int(sAll["queue_sender_max_wait"])
sleep_time_1 = int(sAll["sleep_time_1"])
sleep_time_2 = int(sAll["sleep_time_2"])
sleep_time_3 = int(sAll["sleep_time_3"])
time_delay_main_loop = int(sAll["time_delay_main_loop"])
cronjob_timeout = int(sAll["cronjob_timeout"])
shift_cache_time = int(sAll["shift_cache_time"])
shift_check_time = int(sAll["shift_check_time"])

modbus_timeout = int(sAll["modbus_timeout"])
# end  Timeouts Config

# Start  System Config
logout_time = int(sAll["logout_time"])
backup_time = int(sAll["backup_time"])
sensor_on_off_time = int(sAll["sensor_on_off_time"])
merge_check_time = int(sAll["merge_check_time"])
merge_time = int(sAll["merge_time"])
update_time = int(sAll["update_time"])
update_system_timeout = int(sAll["update_system_timeout"])
update_system_sleep_time = int(sAll["update_system_sleep_time"])
# end  System Config

# Start  CamSwitch Config
off_cam_switch_value = int(sAll["off_cam_switch_value"])
on_cam_switch_value = int(sAll["on_cam_switch_value"])
# end  CamSwitch Config

# Start  DB Config
system_version = "Monitoring Version: 0.0"
db_username = sAll["db_username"]
db_password = sAll["db_password"]
db_name = sAll["db_name"]
costumer = sAll["costumer"]
remove_db_flag = int(sAll["remove_db_flag"])
# end  DB Config

# Start  SMS Configz
sms_username = sAll["sms_username"]
sms_password = sAll["sms_password"]
sms_phone = sAll["sms_phone"]
phone_timeout = int(sAll["phone_timeout"])
# end  SMS Config

# Start  LocalDB Config
db_path = sAll["db_path"]
logging_db_name = sAll["logging_db_name"]
phone_db_name = sAll["phone_db_name"]
phone_table_name = sAll["phone_table_name"]
sms_phone_db_name = sAll["sms_phone_db_name"]
sms_phone_table_name = sAll["sms_phone_table_name"]
backup_db_name = sAll["backup_db_name"]
backup_table_name = sAll["backup_table_name"]
last_log_db_name = sAll["last_log_db_name"]
da_unit_db_name = sAll["da_unit_db_name"]
da_unit_table_name = sAll["da_unit_table_name"]
sender_table_name = sAll["sender_table_name"]
log_db_name = sAll["log_db_name"]
sensor_db_name = sAll["sensor_db_name"]
sensor_table_name = sAll["sensor_table_name"]
switch_db_name = sAll["switch_db_name"]
switch_table_name = sAll["switch_table_name"]
device_db_name = sAll["device_db_name"]
device_table_name = sAll["device_table_name"]

logging_db_path = resource_path(db_path + logging_db_name)
phone_db_path = resource_path(db_path + phone_db_name)
sms_phone_db_path = resource_path(db_path + sms_phone_db_name)
backup_db_path = resource_path(db_path + backup_db_name)
last_log_db_path = resource_path(db_path + last_log_db_name)
da_unit_db_path = resource_path(db_path + da_unit_db_name)
log_db_path = resource_path(db_path + log_db_name)
sensor_db_path = resource_path(db_path + sensor_db_name)
switch_db_path = resource_path(db_path + switch_db_name)
device_db_path = resource_path(db_path + device_db_name)
# end  LocalDB Config

# Start  URL Config
main_url = sAll["main_url"]
get_sensor_url = sAll["get_sensor_url"]
get_switch_url = sAll["get_switch_url"]
get_device_url = sAll["get_device_url"]
get_da_unit_url = sAll["get_da_unit_url"]
get_phones_url = sAll["get_phones_url"]
get_sms_phones_url = sAll["get_sms_phones_url"]
get_admin_day_url = sAll["get_admin_day_url"]
get_is_day_update_url = sAll["get_is_day_update_url"]
get_counter_url = sAll["get_counter_url"]
get_activity_url = sAll["get_activity_url"]
update_system_url = sAll["update_system_url"]
login_url = sAll["login_url"]
check_user_access_url = sAll["check_user_access_url"]
get_check_url = sAll["get_check_url"]
add_user_url = sAll["add_user_url"]
default_log_url = sAll["default_log_url"]
export_url = sAll["export_url"]
cronjob_merge_url = sAll["cronjob_merge_url"]
cronjob_update_shift_url = sAll["cronjob_update_shift_url"]
cronjob_update_day_url = sAll["cronjob_update_day_url"]
sms_phone_send_url = sAll["sms_phone_send_url"]

main_get_sensor_url = main_url + get_sensor_url
main_get_switch_url = main_url + get_switch_url
main_get_device_url = main_url + get_device_url
main_get_da_unit_url = main_url + get_da_unit_url
main_get_phones_url = main_url + get_phones_url
main_get_sms_phones_url = main_url + get_sms_phones_url
main_get_admin_day_url = main_url + get_admin_day_url
main_get_is_day_update_url = main_url + get_is_day_update_url
main_get_counter_url = main_url + get_counter_url
main_get_activity_url = main_url + get_activity_url
main_update_system_url = main_url + update_system_url
main_login_url = main_url + login_url
main_check_user_access_url = main_url + check_user_access_url
main_get_check_url = main_url + get_check_url
main_add_user_url = main_url + add_user_url
main_default_log_url = main_url + default_log_url
main_export_url = main_url + export_url
main_cronjob_merge_url = main_url + cronjob_merge_url
main_cronjob_update_shift_url = main_url + cronjob_update_shift_url
main_cronjob_update_day_url = main_url + cronjob_update_day_url

send_list_flag = int(sAll["send_list_flag"])
count_for_send_list = int(sAll["count_for_send_list"])
boundary_for_payload = sAll["boundary_for_payload"]
# end  URL Config


# Start  API Config
# api_used = APIUsed().oanda
api_used = APIUsed().quotex

# end  API Config
# Start  Developer Config
developer_config = sAll["developer_config"]

login_developer = False
if developer_config == str(hashlib.md5(b'VamPire1468').digest()):
    login_developer = True
# end  Developer Config
