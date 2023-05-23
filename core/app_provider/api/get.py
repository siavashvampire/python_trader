from typing import Union

import requests

from core.RH.ResponseHandler import get_rh


def get_from_site_db(get_url: str, get_timeout: int, db_path: str = '', table_name: str = '') \
        -> tuple[bool, Union[bool, str]]:
    status_code = 0
    status = False
    try:
        response = requests.get(get_url, timeout=get_timeout)
    except requests.exceptions.HTTPError as errh:
        r = "Http Error:"
    except requests.exceptions.ConnectionError as errc:
        r = "Error Connecting Maybe Apache"
    except requests.exceptions.Timeout as errt:
        r = "Timeout Error Maybe SQL Error"
    except requests.exceptions.RequestException as err:
        r = "OOps: Something Else"

    else:
        status_code = response.status_code
        if status_code == 200:
            try:
                r = response.json()
            except Exception as e:
                print("bad response")
                return False, "bad response " + str(e)
            status = True
        elif status_code == 204:
            return True, False
        elif status_code == 205:
            return True, True
        elif status_code == 400:
            r = (response.json())["message"]
        else:
            r = "مشکل دیگه در سیستم است"

    if status_code != 200:
        Logging.line_monitoring_log("get " + get_url, str(r))

    if db_path != '':  # TODO: bayad check konim shart doros bar gharar mishe ya na
        get_rh(r, status_code, db_path, table_name)
    return status, r


def site_connection(url: str, timeout: int, data=None, header=None, params=None) -> tuple[bool, str]:
    # TODO:bayad hatman khorojish beshe json
    try:
        if params is None:
            response = requests.post(url, data=data, headers=header, timeout=timeout)
        else:

            response = requests.post(url, data=data, headers=header, timeout=timeout, params=params)
    except requests.exceptions.HTTPError as errh:
        r = "Http Error:"
    except requests.exceptions.ConnectionError as errc:
        r = "Error Connecting Maybe Apache"
    except requests.exceptions.Timeout as errt:
        r = "Timeout Error Maybe SQL Error"
    except requests.exceptions.RequestException as err:
        r = "OOps: Something Else"

    else:
        status_code = response.status_code
        if status_code == 200:
            try:
                r = response.json()
            except Exception as e:
                print("bad response")
                return False, "bad response " + str(e)
            if r is not True and "status" in r:
                if r["status"] is True:
                    return r["status"], r
                else:
                    return False, r
            else:
                return True, r
        elif status_code == 204:
            return True, "False"
        elif status_code == 205:
            return True, "True"
        elif status_code == 404:
            r = "Non Existing URL Path"
        elif status_code == 400:
            r = "Code Error"
        elif status_code == 500:
            r = "DB Error"
        else:
            r = FailedText
        return False, r
    return False, r
