import pandas as pd


class ReadSAS:
    def __init__(self):
        pass

    def get_df(self, filename):
        return pd.read_sas(filename)