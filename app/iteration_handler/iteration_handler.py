import os
import shutil

import numpy as np


class IterationHandler:
    iter: int
    max_iter: int
    name: str
    count_file_name: str
    flag_file_name: str
    file_name: str

    def __init__(self, name: str, max_iter: int = np.inf) -> None:
        self.name = name
        os.makedirs("./iterations", exist_ok=True)
        self.file_name = f"./iterations/iteration_{name}.txt"
        self.flag_file_name = f"./iterations/flag_{name}.txt"
        self.count_file_name = f"./iterations/count_{name}.txt"
        self.max_iter = max_iter
        self.iter = 0

    def read_iter(self) -> int:
        try:
            with open(self.file_name) as f:
                temp = int(f.readline())
                self.iter = temp
                return temp
        except FileNotFoundError:
            with open(self.file_name, "w") as f:
                f.write("0")
                self.iter = 0
                return 0

    def read_count(self) -> int:
        try:
            with open(self.count_file_name) as f:
                return int(f.readline())
        except FileNotFoundError:
            with open(self.count_file_name, "w") as f:
                f.write("0")
                return 0

    def read_flag(self) -> bool:
        if self.iter > self.max_iter:
            return False
        try:
            with open(self.flag_file_name) as f:
                data = int(f.readline())
                if data == 0:
                    return False
                return True
        except FileNotFoundError:
            with open(self.flag_file_name, "w") as f:
                f.write("1")
                return True

    def write_flag(self, iter_in: bool) -> bool:
        with open(self.flag_file_name, "w") as f:
            if iter_in:
                data = "1"
            else:
                data = "0"

            f.write(data)
            return True

    def write_iter(self, iter_in: int) -> bool:
        with open(self.file_name, "w") as f:
            f.write(str(iter_in))
            self.iter = iter_in
            return True

    def write_count(self, iter_in: int) -> bool:
        with open(self.count_file_name, "w") as f:
            f.write(str(iter_in))
            return True

    def set_max_iter(self, max_iter_in: int):
        self.max_iter = max_iter_in

    def clear(self, models_flag: bool = True) -> bool:
        try:
            os.remove(self.file_name)
        except:
            pass
        try:
            os.remove(self.flag_file_name)
        except:
            pass
        try:
            os.remove(self.count_file_name)
        except:
            pass
        shutil.rmtree(f"./logs/{self.name}", ignore_errors=True)
        shutil.rmtree(f"./models/{self.name}", ignore_errors=True)
        shutil.rmtree(f"./learn_result/{self.name}", ignore_errors=True)
        return True
