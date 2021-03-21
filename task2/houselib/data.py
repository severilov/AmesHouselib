import re
import csv
import numpy as np
import pandas as pd


# Identify the numeric data columns from the data description document
cols = ['MSSubClass', 'LotFrontage', 'LotArea', 'OverallQual', 'OverallCond', 'YearBuilt', 'YearRemod/Add',
        'MasVnrArea', 'BsmtFinSF1', 'BsmtFinSF2', 'BsmtUnfSF', 'TotalBsmtSF', '1stFlrSF', '2ndFlrSF',
        'LowQualFinSF', 'GrLivArea', 'BsmtFullBath', 'BsmtHalfBath', 'FullBath', 'HalfBath', 'BedroomAbvGr',
        'KitchenAbvGr', 'TotRmsAbvGrd', 'Fireplaces', 'GarageYrBlt', 'GarageCars', 'GarageArea', 'WoodDeckSF',
        'OpenPorchSF', 'EnclosedPorch', '3SsnPorch', 'ScreenPorch', 'PoolArea', 'MiscVal', 'MoSold', 'YrSold',
        'SalePrice']


def read_ames_data(datapath='../data/AmesHousing.txt'):
    with open(datapath) as f:
        reader = csv.reader(f, delimiter="\t")
        raw_data = list(reader)

    headings = [re.sub(r'\s+', '', item) for item in raw_data[0]]
    df = pd.DataFrame(raw_data[1:], columns=headings)

    return df


def prepare_data(df):
    df.drop(['Order'], axis=1, inplace=True)

    # DataFRame is full of 'NA' pr blank entries that need to be turned to proper NAN
    df = df.replace(['NA', ''], np.NaN)

    df[cols] = df[cols].astype('float')

    # Dropping those variables with less than 300 non-null values
    df.drop(['Alley', 'PoolQC', 'MiscFeature'], axis=1, inplace=True)

    # Delete all data with MSZoning = commercial, agriculture and industrial as these are not residential units
    df = df[(df.MSZoning != 'C (all)') & (df.MSZoning != 'I (all)') & (df.MSZoning != 'A (agr)')]

    # Transforming the 'CentralAir' discrete variable to numeric
    df['CentralAirNum'] = df.apply(lambda x: 1 if (x['CentralAir'] == 'Y') else 0, axis=1)
    return df


def fill_lot_frontage(df):
    # Examine the 'Lots' grouping.
    df_lots = df[['LotFrontage', 'LotArea', 'LotConfig', 'LotShape']]

    # Generate 'Lots' group where there are null 'LotFrontage' values
    df_LotFrontage_NA = df_lots.loc[(df['LotFrontage'].isnull())]

    # A reasonable assumption is that LotFrontage is linked to LotConfig and LotShape, and
    # the other 'Lot' variables have all observations
    # So I will replace all NA in 'LotFrontage'
    # with its mean based on the corresponding 'LotShape', which is indexed at 3
    df_LotFrontage_NA['LotFrontage'] = df_LotFrontage_NA.apply(lambda x: 74.7688 if (x[3] == 'IR1')
                                                               else x[0], axis=1)
    df_LotFrontage_NA['LotFrontage'] = df_LotFrontage_NA.apply(lambda x: 67.4375 if (x[3] == 'IR2')
                                                               else x[0], axis=1)
    df_LotFrontage_NA['LotFrontage'] = df_LotFrontage_NA.apply(lambda x: 117.6364 if (x[3] == 'IR3')
                                                               else x[0], axis=1)
    df_LotFrontage_NA['LotFrontage'] = df_LotFrontage_NA.apply(lambda x: 66.8214 if (x[3] == 'Reg')
                                                               else x[0], axis=1)

    # Filling the 'LotFrontage' null values with the LotFront_fills series in the given order of the data
    df.loc[df.LotFrontage.isnull(), 'LotFrontage'] = df_LotFrontage_NA.LotFrontage

    return df


def delete_outliers(df):
    # 3 std above the mean
    df_exout = df[(df.SalePrice < np.mean(df.SalePrice) + 3*np.std(df.SalePrice))]
    df_exout = df_exout[(df_exout.GrLivArea < np.mean(df.GrLivArea) + 3*np.std(df.GrLivArea))]
    df_exout = df_exout[(df_exout.BaseLivArea < np.mean(df.BaseLivArea) + 3*np.std(df.BaseLivArea))]

    # non-commercial transactions
    df_exout = df_exout[(df_exout.SaleCondition != 'Abnorml')]
    df_exout = df_exout[(df_exout.SaleCondition != 'Family')]

    # add price per square foot feature
    df_exout['PriceSF'] = df_exout.SalePrice / df_exout.GrLivArea

    return df_exout


def add_zoning(x):
    if 'RM' in x:
        return 1
    elif 'RH' in x:
        return 2
    elif 'RL' in x:
        return 3
    else:
        return 4


def add_new_features(df):
    # Adding structure age variable depending if there was a major remodeling
    df['Age'] = df.apply(lambda x: x['YrSold']-x['YearBuilt'] if (x['YearBuilt']<x['YearRemod/Add'])
                                                           else (x['YrSold']-x['YearRemod/Add']), axis=1)

    # Create a total "finished" basement square footage variable
    df['BaseLivArea'] = df.TotalBsmtSF - df.BsmtUnfSF

    # 'SoldPrice' and 'PriceSF' in 2009 and 2010 are lower than those in 2007 because of the crysis
    df['YrSold'] = df['YrSold'].astype(np.int64)
    df = pd.get_dummies(df, columns=['YrSold'])

    # variable of zoning, corresponding to the mean values from 'MSZoning'
    df['Zoning'] = df.MSZoning.map(add_zoning)
    df['Zone_ordinal'] = df['Zoning']
    df = pd.get_dummies(df, columns=['Zoning'])

    return df


def log_target(df):
    '''
    log transformation of targets
    '''
    df['LnSalePrice'] = np.log(df.SalePrice)
    df['LnPriceSF'] = np.log(df.PriceSF)
    return df
