import os
from prepare_data_for_modeling_or import ModelingData
from prepare_data_for_modeling_child_or import ModelingDataChild
import statsmodels.api as sm
import numpy as np
from constants import *
from sklearn.metrics import accuracy_score
from config import CONFIG
import sys
import pandas as pd
from pymer4.models import Lmer
from pymer4.io import save_model, load_model
from sklmer import LmerRegressor


class OddsRatio:
    def __init__(self, state_code, pop_type='ADULT'):
        self.state_code = state_code
        self.pop_type = pop_type
        if self.pop_type == 'ADULT':
            # TODO
            # ADD statecode for adults
            self.data_obj = ModelingData()
        else:
            self.data_obj = ModelingDataChild(state_code=self.state_code)
        mdf = self.data_obj.get_data_with_epa_region()
        self.results = {}
        mdf = mdf[~mdf['_STATE'].isin(EXCLUDE_STATES)]
        self.df_carb = mdf[mdf['_STATE'].isin(ZEV_STATES)]
        self.df_noncarb = mdf[~mdf['_STATE'].isin(ZEV_STATES)]
        self.carb_regions = self.df_carb['EPA Region'].unique().tolist()
        self.noncarb_regions = self.df_noncarb['EPA Region'].unique().tolist()
        print(self.carb_regions)
        print(self.noncarb_regions)
        print(self.df_noncarb[self.df_noncarb['EPA Region'] == 2]['_STATE'].unique())
        self.mdf = mdf
        self.model_type = "logistic"

    def process(self, mdf):
        if self.pop_type == 'ADULT':
            sc = MODELING_COLUMNS
        else:
            sc = MODELING_COLUMNS_FOR_CHILD
        mdf = mdf[sc]
        mdf = mdf.dropna()
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
        # # print(df['GENDER'].unique())
        # df = df[df['GENDER'].isin([1.0, 2.0])]
        # gender_dict = {2.0: 0, 1.0: 1}
        # df['GENDER'] = df['GENDER'].replace(gender_dict)
        # race_dict = {1.0:1, 2.0:2, 3.0: 3, 4.0: 4, 5.0:0, 6.0:0, 7.0:5, 8.0: 0, 77.0:5, 99.0:5}
        # df['RACE'] = df['RACE'].replace(race_dict)
        # df = df.dropna()
        return df


    def create_df_for_mixed_models(self, df):
        years = [int(i) for i in CONFIG.get("analysis_years")]
        syear, eyear = min(years), max(years)
        year_dict = {year: index + 1 for index, year in enumerate(range(syear, eyear + 1))}
        df['year'] = df['year'].replace(year_dict)
        replace_columns = {"year": "YEAR", "_CPRACE": "RACE", "_STATE": "STATE",
                           "EPA Region": "EPA_REGION", "RCSGENDR": "GENDER",
                           "NONCARB": "ZEV_MANDATES"}
        df = df.rename(columns=replace_columns)
        df.drop(columns=["_CLLCPWT"], inplace=True)
        df = df.dropna()
        return df

    def create_logistic_model(self, tdf):
        # tdf = tdf[tdf['RCSGENDR'].isin([1.0, 2.0])]
        # gender_dict = {2.0: 0, 1.0: 1}
        # tdf['RCSGENDR'] = tdf['RCSGENDR'].replace(gender_dict)
        # race_dict = {1.0:1, 2.0:2, 3.0: 3, 4.0: 4, 5.0:0, 6.0:0, 7.0:5, 8.0: 0, 77.0:5, 99.0:5}
        # tdf['_CPRACE'] = tdf['_CPRACE'].replace(race_dict)
        # tdf = tdf.dropna()

        one_hot = ['_CPRACE', "RCSGENDR"]
        tdf = pd.get_dummies(tdf, columns=one_hot)
        X = tdf.drop(['ASTHMA'], axis=1)
        y = tdf['ASTHMA']
        result_df, accuracy = self.fit_logistic(X, y)
        return result_df, accuracy

    def create_mixed_model(self, df):
        # formula = "ASTHMA  ~ ZEV_MANDATES + GENDER + RACE + POVERTY + DENSITY + YEAR  + (1|STATE) + (1|EPA_REGION)"
        formula = "ASTHMA  ~ ZEV_MANDATES + GENDER + RACE + POVERTY + DENSITY + YEAR  + (1 | STATE)"
        # model = Lmer(formula, data=df, family='binomial')
        nm_estimator = LmerRegressor(
            formula,
            X_cols=df.columns,
            family = 'binomial',
            predict_rfx=True,
            fit_kwargs={
                "control": "optimizer='Nelder_Mead', optCtrl = list(FtolAbs=1e-8, XtolRel=1e-8)"
            },
        )
        print("Modeling begin: 2/2")
        result_df = nm_estimator.fit(data=df).get_params()
        # try:

        print("Modeling end: 1/2")
        return result_df, 100, nm_estimator

    def get_results(self):
        odds_ratio = {}
        accuracy_dict = {}
        epa_regions = CONFIG.get("epa_regions")
        t = [0] + epa_regions
        # for index, epa_region in enumerate(t):
        for epa_region in [0]:
            if epa_region == 0 or (epa_region in self.carb_regions and epa_region in self.noncarb_regions):
                if epa_region == 0:
                    tdf = self.mdf
                else:
                    tdf = self.mdf[self.mdf['EPA Region'] == epa_region]
                fw = "{}/{}.csv".format(DATA_ODDS_RATIO_MODULE, "EPA Region {} Odds Ratio {}".format(epa_region, self.pop_type))
                fw_df = "{}/df_{}.csv".format(DATA_ODDS_RATIO_MODULE, "AFv2_EPA0_{}".format(self.pop_type))
                model_name = "{}/model_{}.h5".format(DATA_ODDS_RATIO_MODULE, "epa_region_{}_{}_zev_{}".format(epa_region, self.pop_type, self.state_code))
                print("Modeling begin: 1/2")
                if self.model_type == 'logistic':
                    df_write = self.df_rename(tdf)
                    df_write.to_csv(fw_df, index=False)
                    tdf = self.process(tdf)
                    result_df, accuracy = self.create_logistic_model(tdf)
                elif self.model_type == 'mixed':
                    # df1 = tdf.query('ASTHMA == 1').sample(10)
                    # df2 = tdf.query('ASTHMA == 0').sample(10)
                    # tdf = df1.append(df2)
                    tdf = self.create_df_for_mixed_models(tdf)
                    tdf.to_csv(fw_df, index=False)
                    result_df, accuracy, model = self.create_mixed_model(tdf)
                    print("Modeling end: 2/2")
                    #save_model(model, model_name)
                accuracy_dict[epa_region] = accuracy
                odds_ratio[epa_region] = result_df
                try:
                    result_df.to_csv(fw)
                except:
                    print("In except")
                    with open(fw, "w", newline='') as file:
                        file.write(result_df)
                print("Written file {} for state {}".format(fw, self.state_code))
                # print("EPA Region {}".format(epa_region))
        # obj = plt_error_bar(odds_ratio)
        # obj.execute()
        return odds_ratio, accuracy_dict

    def fit_logistic(self, X, y):
        res = sm.Logit(y, X).fit()
        params = res.params
        conf = res.conf_int()
        conf['Odds Ratio'] = params
        conf.columns = ['5%', '95%', 'Odds Ratio']
        y_pred = res.predict(X).apply(lambda x: 0 if x<0.5 else 1).tolist()
        accuracy = accuracy_score(y, y_pred)
        return np.exp(conf), accuracy

if __name__ == "__main__":

    years = [int(i) for i in sys.argv[1:]]
    years_str = "_".join([str(i) for i in years])
    CONFIG.update({"analysis_years": years})
    DATA_ODDS_RATIO_MODULE = DATA_ODDS_RATIO_MODULE + "/{}".format(years_str)

    try:
        os.mkdir(DATA_ODDS_RATIO_MODULE)
    except:
        pass

    print(CONFIG.get("analysis_years"))
    for state_code in ZEV_STATES:
        obj = OddsRatio(state_code, pop_type='CHILD')
        obj.get_results()