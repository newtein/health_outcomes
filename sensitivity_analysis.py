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
    fname = "df_ZDEPA Region 0 Odds Ratio CHILD.csv"
    wfname = "python_SA_gender.txt"
    fdf = pd.read_csv(fname)
    wdf = pd.DataFrame()
    for year in range(1, 6):
        df = fdf[fdf['YEAR'] == year]
        col1 = "GENDER"
        col2 = "RACE"
        one_hot = [col1, col2]
        keeps = ["ASTHMA", "ZEV_MANDATES", "POVERTY", "DENSITY", col1, col2]
        df = df[keeps]
        df = pd.get_dummies(df, columns=one_hot)
        filter_cols = ["{}_{}".format(col1, i) for i in range(1,4)]
        for filter_col in filter_cols:
            print(year, filter_col)
            df = df[df[filter_col] == 1]
            drop_cols = ['ASTHMA'] + [i for i in filter_cols if i != filter_col]
            X = df.drop(drop_cols, axis=1)
            y = df['ASTHMA']
            result_df, accuracy = fit_logistic(X, y)
            wdf = wdf.append(result_df)
            print(result_df)
    wdf.to_csv(wfname)
