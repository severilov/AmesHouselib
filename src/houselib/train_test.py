import sys
import numpy as np
import pandas as pd
import pickle
import warnings
warnings.filterwarnings("ignore")

from sklearn.linear_model import LinearRegression, Ridge, RidgeCV
from sklearn.model_selection import KFold, train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler

from .utils import get_df, save_model, load_model


DATA_PATH = './data/processed/ames_prepared.csv'

def train_model(modeltype, datapath=DATA_PATH):
    print("Reading data...\n")
    df_0609, df_2010 = get_df(datapath)
    y_SP = df_0609['SalePrice']
    y_lnSP = df_0609['LnSalePrice']
    X = df_0609.drop(['SalePrice', 'LnSalePrice'], axis=1)

    X_train, X_test, y_train, y_test = train_test_split(X, y_lnSP, test_size=0.3, random_state=8)
    scaler = StandardScaler()
    X_train = pd.DataFrame(scaler.fit_transform(X_train), columns=X_train.columns)
    X_test = pd.DataFrame(scaler.transform(X_test), columns=X_test.columns)

    if modeltype == 'linreg':
        model = LinearRegression()
    elif modeltype == 'ridge':
        ridge_cv = RidgeCV(alphas=np.logspace(-4, 4, 10), cv=5)
        ridge_cv.fit(X_train, y_train)

        print('Best Ridge alpha:', ridge_cv.alpha_)

        model = Ridge(alpha=ridge_cv.alpha_)

    print("Fitting model...\n")
    model.fit(X_train, y_train)
    predictions_test = model.predict(X_test)

    # 5-fold cross-validation
    cv_scores = cross_val_score(model, X_train, y_train, cv=5)

    # Shuffled 5-fold cross validation scores
    kf = KFold(n_splits=5, shuffle=True, random_state=1)
    cv_scores_shuffled = cross_val_score(model, X_train, y_train, cv=kf)

    print(f'Mean cross validation score: {cv_scores.mean()}')
    print(f'Mean shuffled cross validation score: {cv_scores_shuffled.mean()}\n')

    print(f'R-squared on train: {model.score(X_train, y_train)}')
    print(f'R-squared on test: {model.score(X_test, y_test)}\n')

    print(f'MSE: {mean_squared_error(y_test, predictions_test)}')
    print(f'RMSE: {(mean_squared_error(y_test, predictions_test))**0.5}')

    save_model(model)


def calculate_results_for_test(modelpath, datapath):
    """
    Creates predictions on the features with the model and calculates residuals
    """
    model = load_model(modelpath)

    df_0609, df_2010 = get_df(datapath)
    y_lnSP_2010 = df_2010['LnSalePrice']
    X_2010 = df_2010.drop(['SalePrice', 'LnSalePrice'], axis=1)

    # Setting 2010 data as the test data
    scaler = StandardScaler()
    X_train = df_0609.drop(['SalePrice', 'LnSalePrice'], axis=1)
    X_train = pd.DataFrame(scaler.fit_transform(X_train), columns=X_train.columns)
    X_test = pd.DataFrame(scaler.transform(X_2010), columns=X_2010.columns)

    predictions_test = model.predict(X_test)

    results = pd.DataFrame({'Actual': y_lnSP_2010, 'Predicted': predictions_test})
    results['Residuals'] = abs(results['Actual']) - abs(results['Predicted'])

    return results


def test_model(modelpath, show_res=False, datapath=DATA_PATH):
    results = calculate_results_for_test(modelpath, datapath)
    true_labels = results['Actual']
    predicted_labels = results['Predicted']
    if show_res:
        print(f'R-squared on 2010 holdout data: {r2_score(true_labels, predicted_labels)}')
        print(f'MSE: {mean_squared_error(true_labels, predicted_labels)}')
        print(f'RMSE: {(mean_squared_error(true_labels, predicted_labels))**0.5}')
