import argparse
import sys
import pandas as pd
import numpy as np
import pickle
import warnings
warnings.filterwarnings("ignore")

from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression, Ridge, RidgeCV
from sklearn.model_selection import KFold, train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler

sys.path.append('..')

from houselib.utils import fix_seeds, save_model, get_df


fix_seeds()

parser = argparse.ArgumentParser()
parser.add_argument('-m', '--model', type=str, default='linreg', help='ml model to use in training')
args = parser.parse_args()

df_0609, df_2010 = get_df('../../data/ames_prepared.csv')
y_SP = df_0609['SalePrice']
y_lnSP = df_0609['LnSalePrice']
X = df_0609.drop(['SalePrice', 'LnSalePrice'], axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y_lnSP, test_size=0.3, random_state=8)
scaler = StandardScaler()
X_train = pd.DataFrame(scaler.fit_transform(X_train), columns=X_train.columns)
X_test = pd.DataFrame(scaler.transform(X_test), columns=X_test.columns)

if args.model == 'linreg':
    model = LinearRegression()
elif args.model == 'ridge':
    ridge_cv = RidgeCV(alphas=np.logspace(-4, 4, 10), cv=5)
    ridge_cv.fit(X_train, y_train)

    print('Best Ridge alpha:', ridge_cv.alpha_)

    model = Ridge(alpha=ridge_cv.alpha_)

model.fit(X_train, y_train)
predictions_test = model.predict(X_test)

# 5-fold cross-validation
cv_scores = cross_val_score(model, X_train, y_train, cv=5)

# Shuffled 5-fold cross validation scores
kf = KFold(n_splits=5, shuffle=True, random_state=1)
cv_scores_shuffled = cross_val_score(model, X_train, y_train, cv=kf)

#print('Cross validation scores:', cv_scores)
#print('Shuffled cross validation score:', cv_scores_shuffled)
print(f'Mean cross validation score: {cv_scores.mean()}')
print(f'Mean shuffled cross validation score: {cv_scores_shuffled.mean()}\n')

print(f'R-squared on train: {model.score(X_train, y_train)}')
print(f'R-squared on test: {model.score(X_test, y_test)}\n')

print(f'MSE: {mean_squared_error(y_test, predictions_test)}')
print(f'RMSE: {(mean_squared_error(y_test, predictions_test))**0.5}')

save_model(model)
