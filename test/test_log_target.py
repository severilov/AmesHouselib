# log_target
import sys
import pytest
import numpy as np

sys.path.append('./src/')

from houselib import log_target, delete_outliers,  add_new_features, read_ames_data, prepare_data, fill_lot_frontage


def test_log_target():
    '''
    Test if function add log variable to df and add it correctly
    '''
    df = read_ames_data('./data/AmesHousing.txt')
    df = prepare_data(df)
    df = fill_lot_frontage(df)
    df = add_new_features(df)
    df = delete_outliers(df)
    df = log_target(df)
    assert 'LnSalePrice' in df.keys() and 'LnPriceSF' in df.keys()
    assert all(df['LnSalePrice'] == np.log(df.SalePrice))
    assert all(df['LnPriceSF'] == np.log(df.PriceSF))
