import argparse
import sys
import pandas as pd
import pickle

from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler

sys.path.append('..')

from houselib.utils import load_model, get_df


parser = argparse.ArgumentParser()
parser.add_argument('-m', '--modelpath', type=str, default='../models/model.pkl', help='path to ml model for testing')
args = parser.parse_args()

model = load_model(args.modelpath)

df_0609, df_2010 = get_df('../../data/ames_prepared.csv')
y_lnSP_2010 = df_2010['LnSalePrice']
X_2010 = df_2010.drop(['SalePrice', 'LnSalePrice'], axis=1)

# Setting 2010 data as the test data
scaler = StandardScaler()
X_train = df_0609.drop(['SalePrice', 'LnSalePrice'], axis=1)
X_train = pd.DataFrame(scaler.fit_transform(X_train), columns=X_train.columns)
X_test = pd.DataFrame(scaler.transform(X_2010), columns=X_2010.columns)

predictions_test = model.predict(X_test)
print(f'R-squared on 2010 holdout data: {model.score(X_test, y_lnSP_2010)}')
print(f'MSE: {mean_squared_error(y_lnSP_2010, predictions_test)}')
print(f'RMSE: {(mean_squared_error(y_lnSP_2010, predictions_test))**0.5}')
