from config import CONFIG
import pandas as pd


class GetAgeSex:
    def __init__(self, year):
        self.year = year
        self.keyword = "CENSUS"

    def if_child(self, x):
        if x < 18:
            return 1
        else:
            return 0

    def read_file(self):
        fname = "data/{}/{}".format(self.keyword, CONFIG.get(self.keyword).get("age_sex"))
        df = pd.read_csv(fname)
        year_col = "POPEST{}_CIV".format(self.year)
        columns = ["STATE", "SEX", "AGE"] + [year_col]
        df = df[columns]
        df['CHILD'] = df['AGE'].apply(self.if_child)
        df = df[df['AGE'] != 999]
        pop_estimate_by_age_sex = df.groupby(['STATE', "SEX", "CHILD"]).agg({year_col: 'sum'}).reset_index()
        return pop_estimate_by_age_sex

    def read_file_by_age(self):
        fname = "data/{}/{}".format(self.keyword, CONFIG.get(self.keyword).get("age_sex"))
        df = pd.read_csv(fname)
        year_col = "POPEST{}_CIV".format(self.year)
        columns = ["STATE", "SEX", "AGE"] + [year_col]
        df = df[columns]
        df['CHILD'] = df['AGE'].apply(self.if_child)
        df = df[(df['AGE'] != 999) & (df['SEX'] == 0)]
        pop_estimate_by_age = df.groupby(['STATE', "SEX", "CHILD"]).agg({year_col: 'sum'}).reset_index()
        return pop_estimate_by_age

    def read_by_state(self, state_code):
        """
        SEX
            0: both sex
            1: male
            2: female
        CHILD
            1 < 18 years
        """
        df = self.read_file()
        a = df[df['STATE']==state_code]
        child_num = a[(a['SEX'] == 0) & (a['CHILD']==1)]['POPEST2017_CIV'].tolist()[0]
        adult_num = a[(a['SEX'] == 0) & (a['CHILD']==0)]['POPEST2017_CIV'].tolist()[0]
        return {"STATE": state_code, "ADULTS": adult_num, "CHILDREN": child_num, "YEAR": self.year}


if __name__ == "__main__":
    obj = GetAgeSex('2017')
    print(obj.read_by_state(1))