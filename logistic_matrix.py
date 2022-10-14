import os
from prepare_data_for_modeling_or import ModelingData
from prepare_data_for_odds_matrix import ModelingDataChild
import statsmodels.api as sm
import numpy as np
import constants
from constants import *
from sklearn.metrics import accuracy_score
from config import CONFIG
import sys
import pandas as pd
from imblearn.over_sampling import SMOTE
#from pymer4.models import Lmer
#from pymer4.io import save_model, load_model
#from sklmer import LmerRegressor

import warnings
warnings.filterwarnings("ignore")

class OddsRatio:
    def __init__(self, pop_type='ADULT', state_code = None, write_file=True, identifier='', other_filters={},
                 use_smote=False, measurement_type='no2'):
        self.write_file = False
        self.state_code = state_code
        self.identifier = identifier
        self.pop_type = pop_type
        self.other_filters = other_filters
        self.use_smote = use_smote
        self.measurement_type = measurement_type

        years = CONFIG.get("analysis_years")
        years_str = "_".join([str(i) for i in years])
        self.DATA_ODDS_RATIO_MODULE = constants.DATA_ODDS_RATIO_MODULE + "/{}".format(years_str)
        try:
            os.mkdir(self.DATA_ODDS_RATIO_MODULE)
        except:
            pass

        if self.pop_type == 'ADULT':
            self.data_obj = ModelingData()
        else:
            self.data_obj = ModelingDataChild(state_code=state_code, other_filters=self.other_filters,
                                              measurement_type=self.measurement_type)
        mdf = self.data_obj.get_data_with_epa_region()
        self.results = {}
        mdf = mdf[~mdf['_STATE'].isin(EXCLUDE_STATES)]
        self.mdf = mdf
        self.model_type = "logistic"

    def process(self, mdf):
        if self.pop_type == 'ADULT':
            sc = MODELING_COLUMNS
        else:
            sc = MODELING_COLUMNS_FOR_CHILD
        mdf = mdf[sc]
        # mdf = mdf.dropna()
        return mdf

    def  df_rename(self, df):
        years = [int(i) for i in CONFIG.get("analysis_years")]
        syear, eyear = min(years), max(years)
        year_dict = {year: index + 1 for index, year in enumerate(range(syear, eyear + 1))}
        df['year'] = df['year'].replace(year_dict)
        replace_columns = {"year": "YEAR", "_CPRACE": "RACE", "_STATE": "STATE",
                           "EPA Region": "EPA_REGION", "RCSGENDR": "GENDER",
                           "NONCARB": "ZEV_MANDATES"}
        df = df.rename(columns=replace_columns)
        df.drop(columns=["_CLLCPWT"], inplace=True)
        return df

    def create_logistic_model(self, tdf):
        one_hot = ['_CPRACE', "RCSGENDR", "POVERTY"]
        tdf = pd.get_dummies(tdf, columns=one_hot)
        X = tdf.drop(['ASTHMA'], axis=1)
        y = tdf['ASTHMA']
        go_forward = True if len(set(tdf['NONCARB'].unique().tolist())) == 2 else False
        if go_forward:
            try:
                result_df, accuracy = self.fit_logistic(X.astype(float), y)
                return result_df, accuracy
            except Exception as e:
                print("ERROR!!", e)
                print(X.isna().sum())
                return pd.DataFrame(), np.nan
        else:
            print("State {} not participated in this year".format(self.state_code))
            return pd.DataFrame(), np.nan

    def get_primary_exposure(self, df):
        df['NONCARB'] = df['_STATE'].apply(self.if_state)
        return df

    def if_state(self, x):
        if x == self.state_code:
            return 1
        return 0

    def get_results(self):
        odds_ratio = {}
        accuracy_dict = {}
        epa_region = 0
        state_codes = self.mdf['_STATE'].unique().tolist()
        for state_code in state_codes:
            self.state_code = state_code
            self.identifier = state_code
            tdf = self.mdf
            tdf = self.get_primary_exposure(tdf)
            fw = "{}/{}.csv".format(self.DATA_ODDS_RATIO_MODULE, "odds_ratio_{}_{}_{}".format(self.pop_type, self.identifier, self.measurement_type))
            fw_df = "{}/df_{}.csv".format(self.DATA_ODDS_RATIO_MODULE, "AFv2_EPA0_{}".format(self.pop_type))
            print("Modeling begin: 1/2")
            if self.write_file:
                df_write = self.df_rename(tdf)
                df_write.to_csv(fw_df, index=False)
            tdf = self.process(tdf)
            result_df, accuracy = self.create_logistic_model(tdf)

            accuracy_dict[epa_region] = accuracy
            odds_ratio[epa_region] = result_df
            try:
                result_df.to_csv(fw)
            except:
                print("In except")
                with open(fw, "w", newline='') as file:
                    file.write(result_df)
            print("Written file {}".format(fw))
        return odds_ratio, accuracy_dict

    def fit_logistic(self, X, y):
        if self.use_smote:
            smote = SMOTE(random_state=32)
            X, y = smote.fit_resample(X, y)
        res = sm.Logit(y, X).fit()
        params = res.params
        conf = res.conf_int()
        conf['Odds Ratio'] = params
        conf.columns = ['5%', '95%', 'Odds Ratio']
        y_pred = res.predict(X).apply(lambda x: 0 if x<0.5 else 1).tolist()
        accuracy = accuracy_score(y, y_pred)
        print("Accuracy", accuracy)
        return np.exp(conf), accuracy

if __name__ == "__main__":
    measurement_type = sys.argv[1]
    years = [int(i) for i in sys.argv[2:]]
    CONFIG.update({"analysis_years": years})


    print(CONFIG.get("analysis_years"))
    obj = OddsRatio(pop_type='CHILD', measurement_type=measurement_type)
    obj.get_results()