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

# start  Bale Config
# BaleToken           = '1326876710:66d645ae0c89cd745c8763de669e03c78bf3ab65' #developer

if developer:
    bale_token = '1516915829:443dc7da81a8cb716d19d8ceab0360203819ba62'  # New Bot
else:
    bale_token = '1002539037:1d81d4d5b08a9aef9211073e3c1e43f06b8f9d16'  # original

bale_base_url = "https://tapi.bale.ai/"
help_file_name = 'File/Help/BaleHelp'
help_pdf_timeout = 100

config_db.insert({"bale_token": str(bale_token)})
config_db.update({"bale_base_url": str(bale_base_url)})
config_db.update({"help_file_name": str(help_file_name)})
config_db.update({"help_pdf_timeout": str(help_pdf_timeout)})
# end  Bale Config

# start  format Config
time_format = '%Y-%m-%d %H:%M:%S'
send_time_format = '%y-%m-%d %H:%M:%S'
day_time_format = '%Y/%m/%d'
adminUnit = -3

config_db.update({"time_format": str(time_format)})
config_db.update({"send_time_format": str(send_time_format)})
config_db.update({"day_time_format": str(day_time_format)})
config_db.update({"adminUnit": adminUnit})
# end  format Config

# start  PLC Config
register_for_start_read = 2088
register_for_end_read = 2089
register_for_data = 4100
register_for_counter = 6099
register_for_test = 2098

if developer:
    disconnect_alarm_time = 5
else:
    disconnect_alarm_time = 5 * 60

plc_time_sleep_max = 1
plc_time_sleep_min = 0
plc_refresh_time = 5
plc_sleep_time_step_down = 0.1
plc_sleep_time_step_up = 0.01

time_between_read_from_each_device = 0.2

config_db.update({"register_for_start_read": str(register_for_start_read)})
config_db.update({"register_for_end_read": str(register_for_end_read)})
config_db.update({"register_for_data": str(register_for_data)})
config_db.update({"register_for_counter": str(register_for_counter)})
config_db.update({"register_for_test": str(register_for_test)})
config_db.update({"disconnect_alarm_time": str(disconnect_alarm_time)})
config_db.update({"plc_time_sleep_max": str(plc_time_sleep_max)})
config_db.update({"plc_time_sleep_min": str(plc_time_sleep_min)})
config_db.update({"plc_refresh_time": str(plc_refresh_time)})
config_db.update({"plc_sleep_time_step_down": str(plc_sleep_time_step_down)})
config_db.update({"plc_sleep_time_step_up": str(plc_sleep_time_step_up)})
config_db.update({"time_between_read_from_each_device": str(time_between_read_from_each_device)})
# end  PLC Config

# Start  Timeouts Config
bale_get_timeout = 80
login_timeout = 5
send_timeout = 200
check_timeout = 30
sensor_get_timeout = 10
switch_get_timeout = 10
device_get_timeout = 10
da_units_get_timeout = 10
phones_get_timeout = 10
user_timeout = 5
queue_sender_max_wait = 100
sleep_time_1 = 30
sleep_time_2 = 120
sleep_time_3 = 10
time_delay_main_loop = 15
cronjob_timeout = 500
shift_cache_time = 30

if developer:
    shift_check_time = 120
else:
    shift_check_time = 20 * 60

modbus_timeout = 3

config_db.update({"bale_get_timeout": str(bale_get_timeout)})
config_db.update({"login_timeout": str(login_timeout)})
config_db.update({"send_timeout": str(send_timeout)})
config_db.update({"check_timeout": str(check_timeout)})
config_db.update({"sensor_get_timeout": str(sensor_get_timeout)})
config_db.update({"switch_get_timeout": str(switch_get_timeout)})
config_db.update({"device_get_timeout": str(device_get_timeout)})
config_db.update({"da_units_get_timeout": str(da_units_get_timeout)})
config_db.update({"phones_get_timeout": str(phones_get_timeout)})
config_db.update({"user_timeout": str(user_timeout)})
config_db.update({"queue_sender_max_wait": str(queue_sender_max_wait)})
config_db.update({"sleep_time_1": str(sleep_time_1)})
config_db.update({"sleep_time_2": str(sleep_time_2)})
config_db.update({"sleep_time_3": str(sleep_time_3)})
config_db.update({"time_delay_main_loop": str(time_delay_main_loop)})
config_db.update({"cronjob_timeout": str(cronjob_timeout)})
config_db.update({"shift_cache_time": str(shift_cache_time)})
config_db.update({"shift_check_time": str(shift_check_time)})

config_db.update({"modbus_timeout": str(modbus_timeout)})
# end  Timeouts Config

# Start  System Config
logout_time = 3600
backup_time = 30
sensor_on_off_time = 10
merge_check_time = 30
merge_time = 12
update_time = 20*60
update_system_timeout = 20
update_system_sleep_time = 2*60

config_db.update({"logout_time": str(logout_time)})
config_db.update({"backup_time": str(backup_time)})
config_db.update({"sensor_on_off_time": str(sensor_on_off_time)})
config_db.update({"merge_check_time": str(merge_check_time)})
config_db.update({"merge_time": str(merge_time)})
config_db.update({"update_time": str(update_time)})
config_db.update({"update_system_timeout": str(update_system_timeout)})
config_db.update({"update_system_sleep_time": str(update_system_sleep_time)})
# end  System Config

# Start  CamSwitch Config
off_cam_switch_value = 13000
on_cam_switch_value = 26000

config_db.update({"off_cam_switch_value": str(off_cam_switch_value)})
config_db.update({"on_cam_switch_value": str(on_cam_switch_value)})
# end  CamSwitch Config


# Start  DB Config
if developer:
    db_username = 'Siavash'
    db_password = 'VamPire1468'
else:
    db_username = 'root'
    db_password = 'AAaa1234'

db_name = 'test'
costumer = 'Hafez Tiles'
remove_db_flag = 1

config_db.update({"db_username": str(db_username)})
config_db.update({"db_password": str(db_password)})
config_db.update({"db_name": str(db_name)})
config_db.update({"costumer": str(costumer)})
config_db.update({"remove_db_flag": str(remove_db_flag)})
# end  DB Config

# Start  SMS Config
sms_username = "HafezManufactor"
sms_password = "HafezAAaa1234"
sms_phone = "3000505"
phone_timeout = 10

config_db.update({"sms_username": str(sms_username)})
config_db.update({"sms_password": str(sms_password)})
config_db.update({"sms_phone": str(sms_phone)})
config_db.update({"phone_timeout": str(phone_timeout)})
# end  SMS Config

# Start  LocalDB Config
db_path = "File/DataBase/"
logging_db_name = 'logging_db.json'
phone_db_name = 'phone_property_db.json'
phone_table_name = 'phone'
sms_phone_db_name = 'phone_property_db.json'
sms_phone_table_name = 'phone'
backup_db_name = 'backup_property_db.json'
backup_table_name ='Backup'
last_log_db_name = 'last_log_db.json'
da_unit_db_name = 'da_units_property_db.json'
da_unit_table_name = 'db_units'
sender_table_name = 'data_archive'
log_db_name = 'data_log_db.json'
sensor_db_name = 'sensor_property_db.json'
sensor_table_name = 'sensor'
switch_db_name = 'sensor_property_db.json'
switch_table_name = 'switch'
device_db_name = 'electrical_device_property.json'
device_table_name = 'device'

config_db.update({"db_path": str(db_path)})
config_db.update({"logging_db_name": str(logging_db_name)})
config_db.update({"phone_db_name": str(phone_db_name)})
config_db.update({"phone_table_name": str(phone_table_name)})
config_db.update({"sms_phone_db_name": str(sms_phone_db_name)})
config_db.update({"sms_phone_table_name": str(sms_phone_table_name)})
config_db.update({"backup_db_name": str(backup_db_name)})
config_db.update({"backup_table_name": str(backup_table_name)})
config_db.update({"last_log_db_name": str(last_log_db_name)})
config_db.update({"da_unit_db_name": str(da_unit_db_name)})
config_db.update({"da_unit_table_name": str(da_unit_table_name)})
config_db.update({"sender_table_name": str(sender_table_name)})
config_db.update({"log_db_name": str(log_db_name)})
config_db.update({"sensor_db_name": str(sensor_db_name)})
config_db.update({"sensor_table_name": str(sensor_table_name)})
config_db.update({"switch_db_name": str(switch_db_name)})
config_db.update({"switch_table_name": str(switch_table_name)})
config_db.update({"device_db_name": str(device_db_name)})
config_db.update({"device_table_name": str(device_table_name)})
# end  LocalDB Config

# Start  URL Config
if developer:
    main_url = "http://localhost/Hafez/"
else:
    main_url = "http://localhost/"

get_sensor_url = "api/line_monitoring_update/sensor"
get_switch_url = "api/line_monitoring_update/cam_switch"
get_device_url = "api/electrical_update/device"
get_da_unit_url = "api/DAUnits_update/DAUnits"
get_phones_url = "api/contacts_update/Phones"
get_sms_phones_url = "api/contacts_update/Phones"
get_admin_day_url = "api/get/adminDayCounter"
get_is_day_update_url = "api/get/isDayUpdated"
get_counter_url = "api/get/Counter"
get_activity_url = "api/get/sensorActivity"
update_system_url = "api/update"
login_url = "api/user/login"
check_user_access_url = "api/checkAccess/index/"
get_check_url = "api/get/Check"
add_user_url = "api/user/generateUser"
default_log_url = "api/multi_call"
export_url = "api/export/"
cronjob_merge_url = "api/cronjob/mergeData"
cronjob_update_shift_url = "api/cronjob/updateShift"
cronjob_update_day_url = "api/cronjob/updateDay"
sms_phone_send_url = "https://ippanel.com/class/sms/webservice/send_url.php"
send_list_flag = 1
count_for_send_list = 50
boundary_for_payload = "----80085"

config_db.update({"main_url": str(main_url)})
config_db.update({"get_sensor_url": str(get_sensor_url)})
config_db.update({"get_switch_url": str(get_switch_url)})
config_db.update({"get_device_url": str(get_device_url)})
config_db.update({"get_da_unit_url": str(get_da_unit_url)})
config_db.update({"get_phones_url": str(get_phones_url)})
config_db.update({"get_sms_phones_url": str(get_sms_phones_url)})
config_db.update({"get_admin_day_url": str(get_admin_day_url)})
config_db.update({"get_is_day_update_url": str(get_is_day_update_url)})
config_db.update({"get_counter_url": str(get_counter_url)})
config_db.update({"get_activity_url": str(get_activity_url)})
config_db.update({"update_system_url": str(update_system_url)})
config_db.update({"login_url": str(login_url)})
config_db.update({"check_user_access_url": str(check_user_access_url)})
config_db.update({"get_check_url": str(get_check_url)})
config_db.update({"add_user_url": str(add_user_url)})
config_db.update({"default_log_url": str(default_log_url)})
config_db.update({"export_url": str(export_url)})
config_db.update({"cronjob_merge_url": str(cronjob_merge_url)})
config_db.update({"cronjob_update_shift_url": str(cronjob_update_shift_url)})
config_db.update({"cronjob_update_day_url": str(cronjob_update_day_url)})
config_db.update({"sms_phone_send_url": str(sms_phone_send_url)})
config_db.update({"send_list_flag": str(send_list_flag)})
config_db.update({"count_for_send_list": str(count_for_send_list)})
config_db.update({"boundary_for_payload": str(boundary_for_payload)})
# end  URL Config

# Start  Developer Config
if developer:
    developer_config = hashlib.md5(b'VamPire1468').digest()
else:
    developer_config = ""

config_db.update({"developer_config": str(developer_config)})
# end  Developer Config

print("config Create Successfully")
