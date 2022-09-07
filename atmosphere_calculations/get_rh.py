import pandas as pd

class RHbyState:
    def __init__(self):
        path = "data/ATMOS_VOL"
        fname = 'rh.csv'
        self.rh_df = pd.read_csv("{}/{}".format(path, fname))

    def to_int(self, x):
        return float(x.replace("%", ""))

    def get_df(self):
        self.rh_df['RH'] = self.rh_df['RH'].apply(self.to_int)
        return self.rh_df

if __name__ == "__main__":
    obj = RHbyState()
    print(obj.get_df())