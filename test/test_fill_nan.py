# fill_lot_frontage
import sys

sys.path.append('./src/')

from houselib import fill_lot_frontage, read_ames_data, prepare_data


def test_fill_lot_frontage():
    '''
    Check if NaN values has gone
    '''
    df = read_ames_data('./data/raw/AmesHousing.txt')
    df = prepare_data(df)
    df = fill_lot_frontage(df)
    assert df.LotFrontage.isnull().sum() == 0
