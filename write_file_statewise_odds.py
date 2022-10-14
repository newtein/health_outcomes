#!/usr/bin/env python
# coding: utf-8

# In[16]:


import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import pandas as pd
from constants import *
import math
import statsmodels.api as sm
import numpy as np
from imblearn.over_sampling import SMOTE
from collections import OrderedDict
import sys

# In[2]:


use_smote = True
years = sys.argv[1:]


# In[20]:


def create_dataset(row, selected_state):
    state_code = row['state_code']
    population = math.ceil(row['population'])
    pr, ir = row['PR'], row['IR']
    af = row['SAF']
    total_asthma_due_to_trap = math.ceil(row['AC'])
    total_non_asthma = math.ceil(population * (1-pr)) 
#     print(state_code, total_asthma_due_to_trap, total_non_asthma)
    primary_risk = [1]*total_asthma_due_to_trap + [0]*total_non_asthma
    primary_exposure = 1 if state_code == selected_state else 0
    data = {
        "x": primary_exposure,
        "y": primary_risk
    }
    tdf = pd.DataFrame(columns = ["x", "y"], data=data)
    return tdf

def logit_(X, y):
    try:
        res = sm.Logit(y, X).fit()
        params = res.params
        conf = res.conf_int()
        return np.exp(params)["x"]
    except:
        return 9999

def cal_odds(selected_state, state_df):
    y, X = state_df['y'], state_df[['x']]
    #odds_1 = logit_(X, y)
    odds_1 = ""
    if use_smote:
        smote = SMOTE(random_state=32)
        X_res, y_res = smote.fit_resample(X, y)
    odds_2 = logit_(X_res, y_res)
    print(selected_state, odds_1, odds_2)
    return selected_state, odds_1, odds_2
    
headers = ["state_code", "ZEV Mandates", "population", "at_risk", "total_incidence", "incidence_trap", "PR", "IR", "AF", "OddsRatio", "OddsRatio2"]
write_wrapper = OrderedDict()


for year in years:
    write_rows = []
    path = "odds_ratio_module/data/{}/PR_IR_AF.csv".format(year)
    df = pd.read_csv(path)
    write_row = []
    for selected_state in df['state_code'].unique():
        zev_status = 1 if selected_state in ZEV_STATES else 0
        print("For state", selected_state)
        state_df = pd.DataFrame()
        for index, row in df.iterrows():
            tdf = create_dataset(row, selected_state)
            state_df = state_df.append(tdf)
        _, odds_1, odds_2 = cal_odds(selected_state, state_df)
        row = df[df['state_code'] == selected_state]
        write_row = [selected_state, zev_status, math.ceil(row['population']), math.ceil(row['at_risk']),
                     math.ceil(row['incidence_cases']), math.ceil(row['AC']), row['PR'], row['IR'], row['SAF'], odds_1, odds_2]
        write_rows.append(write_row)     
        #if int(selected_state) == 1:
        #    break
    write_df = pd.DataFrame(columns=headers, data = write_rows)
    write_wrapper[year] = write_df

writer = pd.ExcelWriter("odds_ratio_module/statewise_or_{}_{}.xlsx".format(years[0], years[-1]))
for year in write_wrapper:
    write_df = write_wrapper.get(year)
    write_df.to_excel(writer, sheet_name="{}".format(year), index=False)
writer.close()


# In[28]:





# In[ ]:





# In[ ]:




