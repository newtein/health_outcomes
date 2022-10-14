import pandas as pd

class TempbyState:
    def __init__(self):
        path = "data/ATMOS_VOL"
        fname = 'temp.csv'
        self.temp_df = pd.read_csv("{}/{}".format(path, fname))

    def to_int(self, x):
        return float(x.replace("%", ""))

    def get_df(self):
        return self.temp_df

if __name__ == "__main__":
    obj = TempbyState()
    print(obj.get_df())