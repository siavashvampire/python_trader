import os
import sys


def resource_path(relative_path):
    base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
