#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import pandas as pd


# In[4]:


syear, eyear = 2010, 2019
path = "odds_ratio_module/data/"


# In[10]:


data = []
for year in range(syear, eyear+1):
    for state_code in range(1, 57):
        filename = "{}/{}/odds_ratio_CHILD_{}.0.csv".format(path, year, state_code)
        if os.path.exists(filename):
            tdf = pd.read_csv(filename, index_col=0)
            odds = tdf.loc["NONCARB", "Odds Ratio"]
            row = [year, state_code, odds]
            data.append(row)
columns = ['year', 'state_code', 'aOR']
df = pd.DataFrame(columns=columns, data=data)
df.to_csv("odds_ratio_module/statewise_aOR.csv".format(path), index=False)


# In[ ]:




