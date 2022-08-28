#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import csv
from constants import *
import numpy as np
from math import log, floor


# In[2]:


label_dict = {
   
    'GENDER' : {
                1.0: "Male",
                2.0: "Female",
                9.0: "Missing"
               },
    'RACE': {
        1.0: "White",
        2.0: "Black or African American",
        3.0: "American Indian or Alaskan Native",
        4.0: "Asian",
        5.0: "Other race",
        77.0: "Missing"
    },
    'POVERTY': {
        1.0: "Below Poverty Guideline",
        0.0: "Above Poverty Guideline",
        77.0: "Missing"
    }
}


# In[8]:


def merge_cols(x):
    return "{}/{} ({}%)".format(human_format(x['ASTHMA_y']), human_format(x['ASTHMA_x']), get_per(x['ASTHMA_y'], x['ASTHMA_x']))

def filter_df(df, col):
    tdf = df.groupby([col])['ASTHMA'].count().reset_index()
    tdf['LABEL'] = tdf[col].apply(label_dict.get(col).get)
    
    tdf_asthma = df[df['ASTHMA'] == 1].groupby([col])['ASTHMA'].count().reset_index()
    tdf_asthma['LABEL'] = tdf_asthma[col].apply(label_dict.get(col).get)
    
    tdf = tdf.merge(tdf_asthma, on="LABEL")
    tdf['ASTHMA'] = tdf.apply(merge_cols, axis = 1)
    return tdf.reset_index()

def get_value(df, value_col):
    if value_col == 'Missing':
        return df.loc[df['LABEL']==value_col, ['ASTHMA_x']].values[0][0]
    else:
        return df.loc[df['LABEL']==value_col, ['ASTHMA']].values[0][0]


def get_per(a, b):
    value = (a*100)/b
    return "{:.2f}".format(value)

def human_format(number):
    units = ['', 'K', 'M', 'G', 'T', 'P']
    k = 1000.0
    magnitude = int(floor(log(number, k)))
    return '%.2f%s' % (number / k**magnitude, units[magnitude])

def combine_row(year, total_row, zev_states, zev_row,  other_states, other_row, col):
    rows = []
    missing = human_format(get_value(total_row, 'Missing'))


    row1 = [year, "{} (missing n = {})".format(col, missing), zev_states, '', other_states,'', '']
    rows.append(row1)
    x = label_dict.get(col)
    sorted_labels = sorted(x.items(), key=lambda item: item[1])
    sorted_labels = [(i[0], i[1]) for i in sorted_labels if i[1]!='Missing']
    for i in sorted_labels:
        label = i[1]
        zev_value = get_value(zev_row, label)
        other_value = get_value(other_row, label)
        total_value = get_value(total_row, label)
        # zev_per = get_per(zev_value, total_value)
        # other_per = get_per(other_value, total_value)
        trow = ['', label, '', zev_value, '', other_value, total_value]
        rows.append(trow)
    return rows
    

def make_row(year, df, col):
    total_row = filter_df(df, col)
    zev_df = df[df['STATE'].isin(ZEV_STATES)]
    zev_row = filter_df(zev_df, col)
    other_df = df[~df['STATE'].isin(ZEV_STATES)]
    other_row = filter_df(other_df, col)
    
    zev_states = ", ".join(sorted(zev_df['State Name'].unique().tolist()))
    other_states = ", ".join(sorted(other_df['State Name'].unique().tolist()))
    
    rows = combine_row(year, total_row, zev_states, zev_row,  other_states, other_row, col)
    return rows

def merge_for_state_name(df):
    epa_region = pd.read_csv("data/states_and_counties.csv")
    epa_region = epa_region[['State Name','State Code']]
    epa_region = epa_region[epa_region['State Code'] != 'CC']
    epa_region['State Code'] = epa_region['State Code'].apply(int)
    epa_region = epa_region.drop_duplicates(['State Code'], keep='first')
    df = df.merge(epa_region, left_on="STATE", right_on="State Code", how='left')
    return df

def write_file(year, rows):
    fname = dir_path.format(year, "Table1_Demographics.csv")
    with open(fname, "w", newline='') as f:
        headers = ["Year", "Variables", "ZEV States","ZEV States", "Other States","Other States", "Total"]
        writer = csv.writer(f)
        writer.writerow(headers)
        for row in rows:
            writer.writerow(row)


# In[9]:


features = ['GENDER', "RACE", "POVERTY"]    
rows = []
years = list(range(2015, 2016))
dir_path = "odds_ratio_module/data/{}/{}"
for year in years:
    path = dir_path.format(year, "df_AFv2_EPA0_CHILD_old.csv")
    df = pd.read_csv(path)
    df = merge_for_state_name(df)
    race_dict = {7.0: 77.0, 99.0:77.0}
    df['RACE'] = df['RACE'].replace(race_dict)
    for feature in features:
        row = make_row(year, df, feature)
        rows.extend(row)
write_file(year, rows)


# In[ ]:




