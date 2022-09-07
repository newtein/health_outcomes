from config import CONFIG
from get_sas_df import ReadSAS
from constants import *
import pandas as pd
import os


class ReadACBS:
    def __init__(self, year, of='ADULT'):
        self.year = str(year)
        self.of = of
        self.keyword = "ACBS"
        self.filename = self.get_filename()
        print(self.filename)

    def get_filename(self):
        return "data/{}/{}/{}/{}".format(self.keyword, self.year, self.of, CONFIG.get(self.keyword).get(self.year)
                                         .get(self.of))

    def get_df(self, all=False):
        df = ReadSAS().get_df(self.filename)
        if self.year in ['2008', '2009', '2010']:
            df['CLLCPWT_F'] = df['CHILDWT_F']
        if self.year == '2011':
            df['CLLCPWT_F'] = df['CLANDWT_F']
        try:
            """
            Handling inconsistencies in the files
            """
            df['_STATE'] = df['_state']
        except:
            pass
        try:
            df['SEQNO'] = df['seqno']

        except:
            pass
        return df


if __name__ == "__main__":
    obj = ReadACBS('2009', of='CHILD')
    print(obj.get_df().head(2))