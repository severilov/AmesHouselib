# get_df, read_ames_data
import pytest

from houselib import get_df, read_ames_data


@pytest.mark.parametrize('path', ['./data/raw/AmesHousing.txt'])
def test_read_ames_data(path):
    '''
    Test if function read data correctly
    '''
    df = read_ames_data(path)
    assert df is not None
    assert df.shape == (2930, 82)


@pytest.mark.parametrize('path', ['./data/processed/ames_prepared.csv'])
def test_get_df(path):
    '''
    Test if function read prepared data correctly
    '''
    df_0609, df_2010 = get_df(path)
    assert df_0609 is not None and df_2010 is not None
    assert df_0609.shape == (206, 27)
    assert df_2010.shape == (27, 27)
