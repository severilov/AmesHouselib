# add_new_features
import sys

sys.path.append('./src/')

from houselib import add_new_features, add_location_feature, read_ames_data, prepare_data, fill_lot_frontage


def test_add_new_features():
    '''
    Test if all needed features were added
    '''
    df = read_ames_data('./data/raw/AmesHousing.txt')
    df = prepare_data(df)
    df = fill_lot_frontage(df)
    df = add_new_features(df)
    assert 'Age' in df.keys()
    assert 'BaseLivArea' in df.keys()
    assert any('YrSold' in s for s in df.keys())
    assert any('Zoning' in s for s in df.keys())
    assert 'Zone_ordinal' in df.keys()


def test_add_location_feature():
    '''
    Test if location needed feature was added
    '''
    df = read_ames_data('./data/raw/AmesHousing.txt')
    df = prepare_data(df)
    df = fill_lot_frontage(df)
    df = add_new_features(df)
    df = add_location_feature(df)
    assert 'Location' in df.keys()
