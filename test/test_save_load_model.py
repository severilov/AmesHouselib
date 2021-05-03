# load_model, save_model
import os
import pytest
import pandas as pd

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from houselib import save_model, load_model, get_df


test_load_paths = ['./src/models/model.pkl']

@pytest.mark.parametrize('path', test_load_paths)
def test_load_model(path):
    '''
    Check if function load model
    '''
    assert os.path.isfile(path) == True
    model = load_model(path)
    assert model is not None


test_save_paths = ['./src/models']

@pytest.mark.parametrize('path', test_save_paths)
def test_save_model(path):
    '''
    Check if function saved model correctly
    '''
    df_0609, df_2010 = get_df('./data/processed/ames_prepared.csv')
    y_lnSP = df_0609['LnSalePrice']
    X = df_0609.drop(['SalePrice', 'LnSalePrice'], axis=1)

    X_train, X_test, y_train, y_test = train_test_split(X, y_lnSP, test_size=0.3, random_state=8)
    scaler = StandardScaler()
    X_train = pd.DataFrame(scaler.fit_transform(X_train), columns=X_train.columns)

    model = LinearRegression()
    model.fit(X_train, y_train)

    save_model(model, modelspath=path)
    assert os.path.isfile(f'{path}/model.pkl') == True
    model = load_model(f'{path}/model.pkl')
    assert model is not None
