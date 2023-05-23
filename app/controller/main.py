import pandas as pd
from pandas import DataFrame

from app.controller.learn_attitude import learn_attitude
from app.controller.learn_altitude import learn_altitude
from app.controller.learn_path import learn_path
from app.controller.play_altitude import play_altitude
from app.controller.play_attitude import play_attitude
from app.controller.play_path import play_path


class Controller:
    df_learn: DataFrame

    def __init__(self):
        self.file_path = 'controller.xlsx'
        self.df_learn = pd.read_excel(self.file_path, sheet_name="learn", engine='openpyxl')
        self.df_run = pd.read_excel(self.file_path, sheet_name="run", engine='openpyxl')
        self.writer = pd.ExcelWriter(self.file_path, engine='xlsxwriter')

        self.clear_file()

    def clear_file(self):
        self.df_learn["iter number"] = self.df_learn["iter number"].fillna(0)
        self.df_run["run"] = self.df_run["run"].fillna(0)
        self.df_learn.to_excel(self.writer, sheet_name="learn", index=False)
        self.df_run.to_excel(self.writer, sheet_name="run", index=False)

        self.writer.save()

    def run(self):
        apps = self.df_learn[self.df_learn["iter number"] > 0]
        for index, app in apps.iterrows():
            if "attitude" in app["environment name"]:
                learn_attitude(app["environment name"], app["iter number"])
            elif "altitude" in app["environment name"]:
                learn_altitude(app["environment name"], app["iter number"])
            elif "path_planning" in app["environment name"]:
                learn_path(app["environment name"], app["iter number"])

        apps = self.df_run[self.df_run["run"] > 0]
        for index, app in apps.iterrows():

            if "attitude" in app["environment name"]:
                play_attitude(app["environment name"])
            elif "altitude" in app["environment name"]:
                play_altitude(app["environment name"])
            elif "path_planning" in app["environment name"]:
                play_path(app["environment name"])
