import os
import sys
import warnings

from PyQt5.QtWidgets import QApplication


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


path = resource_path("")
path = path.replace(path[2], "/")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    from core.app_provider.admin.main import Main

    warnings.filterwarnings("ignore", category=DeprecationWarning)
    warnings.filterwarnings("ignore")
    main = Main()
    sys.exit(app.exec_())
