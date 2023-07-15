from tinydb import TinyDB, Query



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

