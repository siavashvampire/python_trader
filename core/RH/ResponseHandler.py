from tinydb import TinyDB, Query

from core.config.Config import phone_db_path, phone_table_name


def get_rh(r, status_code, db_path, table_name):
    if status_code == 0:
        print(r)
    elif status_code == 404:
        print("Non Existing URL Path")
        print(r)
    elif status_code == 400:
        print("DB Error")
        print(r)
    elif status_code == 500:
        print("internal Code Error")
        print(r)
    elif status_code == 200:
        try:
            db = TinyDB(db_path)
            db.drop_table(table_name)
            db.close()
            db = TinyDB(db_path).table(table_name)
            for i in r:
                # db.upsert(i, prop.id == i["id"])

                db.insert(i)

        except Exception as e:
            print("bad Response in get_rh")

    else:
        print("Non Handling Error in RH")
        print(status_code)


def PhoneNumberResponseHandler(Name, phone_id):
    insertflag = False
    PhoneProp = Query()
    PhoneDB = TinyDB(phone_db_path).table(phone_table_name)
    sea = PhoneDB.search(PhoneProp.id == phone_id)
    if (sea == []):
        PhoneDB.insert({'Name': str(Name), 'id': phone_id, 'SendONOFF': 1, 'Access': 0, 'Units': [0], 'phase': [0]})
        insertflag = True
    else:
        PhoneDB.update({'Name': str(Name)}, PhoneProp.id == phone_id)
        insertflag = False
    return insertflag


def CounterResponseHandler(r, status):
    if r == True:
        massage = "داده ای تاکنون ثبت نشده است"
    else:
        massage = ""
        if not status:
            print(r)
        else:
            for i in r:
                massage += CounterResponseText.format(Name=i["Sensor_name"], Phase=i["phase"], counter=i["counter"],
                                                      Tile=i["tile_name"])
    return massage


def GetActivityeHandler(r, status):
    if r == True:
        massage = "داده ای تاکنون ثبت نشده است"
        return (massage)
    massage = ""

    if not status:
        print(r)
    else:
        try:
            for i in r:
                if int(i["Active"]):
                    Activetext = " فعال "
                else:
                    Activetext = "غیر فعال "
                massage += ActivityResponseText.format(Name=i["Name"], Phase=i["Phase"], Active=Activetext,
                                                       unit=i["unit"])
            return massage

        except Exception as e:
            print("bad Response in SensorActivity")

    massage = "خطایی رخ داده است"
    return massage


def send_data_rh(r, status):
    error = []
    good = False
    should_update = False
    index = []
    if status is True:
        good = True
        should_update = r["need_update"]
        result: list = r["result"]
        temp_index = 0
        for i in result:
            if "result" in i and i["result"]:
                index.append(temp_index)
            else:
                print(i)
                Logging.sender_log("sender", str(i))
                error.append(temp_index)

            temp_index += 1

    else:
        Logging.sender_log("sender", str(status) + str(r))
        index = []
        error = []
    return good, index, error, should_update
