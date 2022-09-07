import pandas as pd
from constants import *
import numpy as np


class TRAPIncidences:
    def __init__(self, of='CHILD'):
        self.of = of

    def read(self):
        df = pd.read_excel(TRAP_INCIDENCE, engine='openpyxl')
        # if self.of == 'CHILD':
        #     return df[['State', 'AF']]
        # else:
        #     df['AF'] = np.nan
        #     return df[['State', 'AF']]
        return df[['State', 'AF']]

    def read_v2(self):
        # columns = ['State Code', 'year', 'concentration', 'concentration_5', 'concentration_95', 'AF', 'AF_5', 'AF_95']
        columns = ['State Code', 'year', 'concentration','AF']
        df = pd.read_csv(TRAP_INCIDENCE_v2)
        return df[columns]
