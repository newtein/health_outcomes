import pandas as pd
import os
import csv

syear, eyear = 2008, 2019
wdata = []

epa_region = pd.read_csv("data/states_and_counties.csv")
epa_region = epa_region[['State Name', 'State Code', "EPA Region"]]
epa_region = epa_region[epa_region['State Code'] != 'CC']
epa_region['State Code'] = epa_region['State Code'].apply(int)
epa_region = epa_region.drop_duplicates(['State Code'], keep='first')
state_lookup = {i:j for i, j in zip(epa_region['State Code'], epa_region['State Name'])}

for year in range(syear, eyear+1):
    path = "odds_ratio_module/data/{}/df_AFv2_EPA0_CHILD.csv".format(year)
    if os.path.exists(path):
        df = pd.read_csv(path, usecols=['STATE'])
        unique_states = [state_lookup.get(i) for i in df['STATE'].unique().tolist() if i]
        print(year, unique_states)
        wdata.append([year, ", ".join(unique_states)])
        break

f = open("odds_ratio_module/participating_states_{}_{}.csv".format(syear, eyear), "w", newline='')
writer = csv.writer(f)
for row in wdata:
    writer.writerow(row)
f.close()