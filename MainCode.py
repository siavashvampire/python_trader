import asyncio
import os
import sys

import warnings

from core.database.database import create_db


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


path = resource_path("")
path = path.replace(path[2], "/")

if __name__ == '__main__':
    # from PyQt5.QtWidgets import QApplication

    # app = QApplication(sys.argv)
    # from core.app_provider.admin.main import Main

    warnings.filterwarnings("ignore", category=DeprecationWarning)
    warnings.filterwarnings("ignore")

    create_db()

    from app.telegram_bot.main import telegram_app

    # asyncio.run(telegram_app.run_all())
    # main = Main()
    print("miad inja khar ahmagh22")


    # sys.exit(app.exec_())
