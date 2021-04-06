# delete_outliers
import sys
import pytest
import numpy as np

sys.path.append('./src/')

from houselib import delete_outliers,  add_new_features, read_ames_data, prepare_data, fill_lot_frontage


def test_delete_outliers():
    '''
    Test if all outliers were deleted and not deleted others
    '''
    df = read_ames_data('./data/AmesHousing.txt')
    df = prepare_data(df)
    df = fill_lot_frontage(df)
    df = add_new_features(df)
    df_exout = delete_outliers(df)

    above_3std_sp = df_exout.SalePrice[(df_exout.SalePrice > np.mean(df.SalePrice) + 3 * np.std(df.SalePrice))].count()
    under_3std_sp = df_exout.SalePrice[(df_exout.SalePrice < np.mean(df.SalePrice) - 3 * np.std(df.SalePrice))].count()
    above_3std_ga = df_exout.GrLivArea[(df_exout.GrLivArea > np.mean(df.GrLivArea) + 3 * np.std(df.GrLivArea))].count()
    under_3std_ga = df_exout.GrLivArea[(df_exout.GrLivArea < np.mean(df.GrLivArea) - 3 * np.std(df.GrLivArea))].count()
    above_3std_ba = df_exout.BaseLivArea[(df_exout.BaseLivArea > np.mean(df.BaseLivArea) + 3 * np.std(df.BaseLivArea))].count()
    under_3std_ba = df_exout.BaseLivArea[(df_exout.BaseLivArea < np.mean(df.BaseLivArea) - 3 * np.std(df.BaseLivArea))].count()
    outliers = [above_3std_sp, under_3std_sp,
                above_3std_ga, under_3std_ga,
                above_3std_ba, under_3std_ba]

    assert all(np.array(outliers) == 0)
    assert (df.shape[0] - df_exout.shape[0]) == 284
