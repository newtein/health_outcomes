import pandas as pd


class ReadCountyCensus:
    def __init__(self):
        path = "../data/CENSUS"
        fname = "cc-est2019-alldata.csv"
        self.df = pd.read_csv("{}/{}".format(path, fname),  encoding = "ISO-8859-1")

    def get_df(self):
        return self.df

if __name__ == "__main__":
    obj = ReadCountyCensus()
    print(obj.get_df())
