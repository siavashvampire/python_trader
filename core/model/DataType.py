bale_data = {"id": None, "name": None}
bale_app_name = 'contacts/phones/new'

switch_activity_data = {"Switch_id": None, "active": None, "time": None}
switch_activity_app = 'LineMonitoring'
switch_activity_class = 'line_monitoring'
switch_activity_method = 'camSwitchActivity'

sensor_new_log_data = {"Sensor_id": None, "AbsTime": None, "counter": None, "Tile_Kind": None, "Motor_Speed": None,
                       "start_time": None}
sensor_new_log_app = 'LineMonitoring'
sensor_new_log_class = 'line_monitoring'
sensor_new_log_method = 'newLog'

sensor_activity_data = {"Sensor_id": None, "active": None, "Tile_Kind": None, "time": None}
sensor_activity_app = 'LineMonitoring'
sensor_activity_class = 'line_monitoring'
sensor_activity_method = 'sensorActivity'

update_app_data = {"LineMonitoring": None, "ElectricalSubstation": None}

Device_new_log_data = {"substation_id": None,
                       "unitId": None,
                       "Start_time": None,
                       "Current_A": None,
                       "Current_B": None,
                       "Current_C": None,
                       "Current_N": None,
                       "Current_G": None,
                       "Current_Avg": None,
                       "Voltage_A_B": None,
                       "Voltage_B_C": None,
                       "Voltage_C_A": None,
                       "Voltage_L_L_Avg": None,
                       "Voltage_A_N": None,
                       "Voltage_B_N": None,
                       "Voltage_C_N": None,
                       "Voltage_L_N_Avg": None,
                       "Active_Power_A": None,
                       "Active_Power_B": None,
                       "Active_Power_C": None,
                       "Active_Power_Total": None,
                       "Reactive_Power_A": None,
                       "Reactive_Power_B": None,
                       "Reactive_Power_C": None,
                       "Reactive_Power_Total": None,
                       "Apparent_Power_A": None,
                       "Apparent_Power_B": None,
                       "Apparent_Power_C": None,
                       "Apparent_Power_Total": None,
                       "Power_Factor_A": None,
                       "Power_Factor_B": None,
                       "Power_Factor_C": None,
                       "Power_Factor_Total": None,
                       "Displacement_Power_Factor_A": None,
                       "Displacement_Power_Factor_B": None,
                       "Displacement_Power_Factor_C": None,
                       "Displacement_Power_Factor_Total": None,
                       "Frequency": None,
                       "Active_Energy_Delivered": None,
                       "Active_Energy_Received": None,
                       "Active_Energy_Delivered_Pos_Received": None,
                       "Active_Energy_Delivered_Neg_Received": None,
                       "Reactive_Energy_Delivered": None,
                       "Reactive_Energy_Received": None,
                       "Reactive_Energy_Delivered_Pos_Received": None,
                       "Reactive_Energy_Delivered_Neg_Received": None,
                       "Apparent_Energy_Delivered": None,
                       "Apparent_Energy_Received": None,
                       "Apparent_Energy_Delivered_Pos_Received": None,
                       "Apparent_Energy_Delivered_Neg_Received": None,
                       "Active_Power_Last_Demand": None,
                       "Active_Power_Present_Demand": None,
                       "Active_Power_Predicted_Demand": None,
                       "Active_Power_Peak_Demand": None,
                       "Active_Power_PK_DT_Demand": None,
                       "Reactive_Power_Last_Demand": None,
                       "Reactive_Power_Present_Demand": None,
                       "Reactive_Power_Predicted_Demand": None,
                       "Reactive_Power_Peak_Demand": None,
                       "Reactive_Power_PK_DT_Demand": None,
                       "Apparent_Power_Last_Demand": None,
                       "Apparent_Power_Present_Demand": None,
                       "Apparent_Power_Predicted_Demand": None,
                       "Apparent_Power_Peak_Demand": None,
                       "Apparent_Power_PK_DT_Demand": None,
                       "Current_Avg_Last_Demand": None,
                       "Current_Avg_Present_Demand": None,
                       "Current_Avg_Predicted_Demand": None,
                       "Current_Avg_Peak_Demand": None,
                       "Current_Avg_PK_DT_Demand": None,
                       }

Device_new_log_app = 'ElectricalSubstation'
Device_new_log_class = 'electrical'
Device_new_log_method = 'newLog'

user_add_data = {"fname": None, "lname": None, "email": None, "phone": None, "password": None, "groupId": "6",
                 "verified": "1"}
