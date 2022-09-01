from constants import *
from config import CONFIG
import numpy as np
from get_trap_incidences import TRAPIncidences
import pandas as pd
import math


class AdjustWeightsForOR:
    def __init__(self, df, pop_type):
        self.df= df
        self.pop_type = pop_type
        self.trap_data = TRAPIncidences(of=self.pop_type).read_v2()
        print(self.df.columns)
        print(self.trap_data.columns)

    def resale_weights(self, weight_col):
        state_weight_df = self.df.groupby(['_STATE'])['year'].apply(set).apply(len).reset_index()
        state_weight_df['SWEIGHT'] = state_weight_df['year']
        self.df = self.df.merge(state_weight_df[['_STATE', 'SWEIGHT']], on='_STATE', how='left')
        self.df[weight_col] = self.df[weight_col] / self.df['SWEIGHT']
        self.df['TRAP_ASTHMA'] = self.df[weight_col] * self.df['AF']
        self.df['POP_W'] = self.df[weight_col]

    def execute(self):
        print("weighting begin")
        print("Pop type", self.pop_type)
        self.df = self.df.merge(self.trap_data, left_on='State Name', right_on='State', how='left')
        trap_global = CONFIG.get("TRAP_GLOBAL").get("value")
        self.years = CONFIG.get("analysis_years")
        self.df['AF'] = self.df['AF'].fillna(trap_global)
        self.df['AF'] = self.df['AF'].astype(float)
        if self.pop_type == 'ADULT':
            weight_col = '_LLCPWT2'
        else:
            weight_col = '_CLLCPWT'
        self.resale_weights(weight_col)
        self.df = self.df[~pd.isna(self.df['TRAP_ASTHMA'])]
        # self.df['TRAP_ASTHMA'] = self.df['TRAP_ASTHMA'] / self.df['TRAP_ASTHMA'].min()

        t = []
        print(self.df.shape)
        trap_asthma_w = self.df['TRAP_ASTHMA'].apply(math.ceil).tolist()
        pop_w = self.df['POP_W'].apply(math.ceil).tolist()
        """Try this approach"""
        # new_df = self.df.loc[np.repeat(self.df.index.values, weights)]
        """
        Dropping for lesser memory
        """
        self.df = self.df.drop(['State Name', 'State', 'AF', 'TRAP_ASTHMA', 'POP_W'], axis=1).reset_index()

        columns = self.df.columns
        for index, row in self.df.iterrows():
            weight = trap_asthma_w[index]
            pop_weight = pop_w[index]
            asthma_flag = int(row['ASTHMA'])
            row_t = []
            if asthma_flag:
                """
                Adjust based on AF, otherwise adjust the original numbers
                """
                for j in range(weight):
                    row_t.append(row.tolist())
                for j in range(pop_weight-weight):
                    row['ASTHMA'] = 0
                    row_t.append(row.tolist())
            else:
                for j in range(pop_weight):
                    row_t.append(row.tolist())
            t.extend(row_t)
            if index%100000==0:
                print(index)
        print("weighting ended 1/3")
        del trap_asthma_w
        del pop_w

        print("weighting ended 2/3")
        if self.pop_type == 'ADULT':
            dtype = {'NONCARB': np.int8, '_AGEG5YR': np.int8, 'SEX': np.int8, '_RACE_G1': np.int8, 'POVERTY':np.bool, 'DENSITY': np.int8,
             '_EDUCAG': np.int8, '_BMI5CAT': np.int8, 'ASTHMA': np.bool, '_LLCPWT2': np.float16, '_STATE': np.int8,
             'EPA Region': np.int8}
            new_df = pd.DataFrame(columns=columns, data=t)
        else:
            new_df = pd.DataFrame(columns=columns, data=t)

        # new_df = new_df.append(t, ignore_index=True)
        #new_df.to_csv("temp.csv", index=False)
        print("weighting ended 3/3")
        return new_df
