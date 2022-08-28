import pandas as pd
import numpy as np
from config import CONFIG


class POVERTY:
    def __init__(self, df):
        self.df = df

    def count_adults(self, x):
        landline = x['NUMADULT']
        cell = x['HHADULT']
        if not pd.isna(landline):
            return landline
        return cell

    def add_adults_and_children(self, x):
        children = x['CHILDREN']
        adults = x['ADULTS']
        if not pd.isna(children) and not pd.isna(adults):
            if adults not in [77, 99] and children not in [99]:
                if children == 88:
                    children = 0
                return adults + children
            elif adults not in [77, 99]:
                return adults
        elif (not pd.isna(adults)) and (adults not in [77, 99]):
            return adults
        return np.nan

    def calculate_poverty_guideline_flag(self, x):
        if x['_STATE'] == 2:
            poverty_table = CONFIG.get("POVERTY").get("HOUSEHOLD_DATA").get("AK")
        elif x['_STATE'] == 15:
            poverty_table = CONFIG.get("POVERTY").get("HOUSEHOLD_DATA").get("HW")
        else:
            poverty_table = CONFIG.get("POVERTY").get("HOUSEHOLD_DATA").get("DATA")
        household = x['HOUSEHOLD']
        if not pd.isna(household):
            if household > 8:
                poverty_guideline = poverty_table.get("8") + (poverty_table.get("+8") * (household - 8))
            else:
                poverty_guideline = poverty_table.get(str(int(household)))
            return poverty_guideline
        return np.nan

    def get_poverty_flag(self, x):
        income_table = CONFIG.get("POVERTY").get("INCOME_INDEX").get("DATA")
        reported_income = x['INCOME2']
        if pd.isna(reported_income) or (reported_income in [77, 99]):
            return 77
        income = income_table.get(str(int(reported_income)))
        if income <= x['POVERTY_GUIDE']:
            return 1
        return 0

    def process(self):
        mdf = self.df
        mdf['ADULTS'] = mdf.apply(self.count_adults, axis=1)
        mdf['HOUSEHOLD'] = mdf.apply(self.add_adults_and_children, axis=1)
        mdf['POVERTY_GUIDE'] = mdf.apply(self.calculate_poverty_guideline_flag, axis=1)
        mdf['POVERTY'] = mdf.apply(self.get_poverty_flag, axis=1)
        return mdf