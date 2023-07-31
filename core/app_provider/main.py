import os


def file_exist(file_name_in: str, main_path: str = "File/trade_data/"):
    """
        check file exists or not
    :param file_name_in: file path
    :param main_path: main path
    :return:
    True when it exists,
    False when it doesn't exist
    """
    files = os.listdir(main_path)
    for file in files:
        if file_name_in == file:
            return True

    return False
