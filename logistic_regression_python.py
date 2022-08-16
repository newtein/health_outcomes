import pandas as pd
import statsmodels.api as sm
import numpy as np
from sklearn.metrics import accuracy_score


def fit_logistic(X, y):
    res = sm.Logit(y, X).fit()
    params = res.params
    conf = res.conf_int()
    conf['Odds Ratio'] = params
    conf.columns = ['5%', '95%', 'Odds Ratio']
    y_pred = res.predict(X).apply(lambda x: 0 if x < 0.5 else 1).tolist()
    accuracy = accuracy_score(y, y_pred)
    return np.exp(conf), accuracy


if __name__ == "__main__":
    fname = "df_OriginalEPA Region 0 Odds Ratio CHILD.csv"
    wfname = "python_stats_model.txt"
    fdf = pd.read_csv(fname)
    wdf = pd.DataFrame()
    for year in range(1, 6):
        df = fdf[fdf['YEAR'] == year]
        print(year)
        # keeps = ["ASTHMA", "ZEV_MANDATES",  "RACE", "POVERTY", "DENSITY"]
        keeps = ["ASTHMA", "ZEV_MANDATES", "GENDER", "DENSITY", "RACE", "POVERTY"]
        #keeps = ["ASTHMA", "ZEV_MANDATES", "POVERTY", "DENSITY", "GENDER"]
        df = df[keeps]
        one_hot = [ 'RACE', "GENDER"]
        df = pd.get_dummies(df, columns=one_hot)
        X = df.drop(['ASTHMA'], axis=1)
        y = df['ASTHMA']
        result_df, accuracy = fit_logistic(X, y)
        wdf = wdf.append(result_df)
        print(result_df)
    wdf.to_csv(wfname)
