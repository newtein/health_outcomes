from config import CONFIG
from get_sas_df import ReadSAS
from constants import *
import pandas as pd
import os


class ReadACBS:
    def __init__(self, year, of='ADULT'):
        self.year = year
        self.of = of
        self.keyword = "ACBS"
        self.filename = self.get_filename()
        print(self.filename)

    def get_filename(self):
        return "data/{}/{}/{}/{}".format(self.keyword, self.year, self.of, CONFIG.get(self.keyword).get(self.year)
                                         .get(self.of))

    def get_df(self, all=False):
        return ReadSAS().get_df(self.filename)


if __name__ == "__main__":
    obj = ReadACBS('2017')
    print(obj.get_df().head(2))