import os
import sys

import warnings
from threading import Thread

from core.database.database import create_db


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


path = resource_path("")
path = path.replace(path[2], "/")


def main_thread():
    from PyQt5.QtWidgets import QApplication
    from core.app_provider.admin.main import Main

    app = QApplication(sys.argv)

    main = Main()

    sys.exit(app.exec_())


if __name__ == '__main__':
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    warnings.filterwarnings("ignore")

    create_db()

    from app.telegram_bot.main import telegram_app

    thread = Thread(target=main_thread)
    thread.start()

    telegram_app.run_all()
