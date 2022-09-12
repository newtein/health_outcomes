import pandas as pd


class ReadLUR:
    def __init__(self):
        path = "../data/lur_no2"
        fname = "uwc16625203218040380eebdf79369d5d84edb6dba8eb6c1.csv"
        self.df = pd.read_csv("{}/{}".format(path, fname))

    def get_df(self):
        return self.df


if __name__ == "__main__":
    obj = ReadLUR()
    print(obj.get_df())
