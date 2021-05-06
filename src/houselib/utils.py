import numpy as np
import pandas as pd
import pickle


def fix_seeds(seed=42):
    '''
    Fix random seed
    '''
    np.random.seed(seed)


def save_model(model, modelspath='./src/models'):
    '''
    Save ML model into path
    '''
    with open(f'{modelspath}/model.pkl', 'wb') as handle:
        pickle.dump(model, handle)


def load_model(path='../models/model.pkl'):
    '''
    Load ML model from path
    '''
    with open(path, 'rb') as model_file:
        model = pickle.load(model_file)

    return model


def get_df(prepared_data_path='../data/ames_prepared.csv'):
    '''
    Read prepared data
    Return: df_0609, df_2010, dataframes divided into 2006-2009 and 2010 parts
    '''
    df = pd.read_csv(prepared_data_path)
    df_0609 = df.loc[df['YrSold_2010'] != 1]
    df_2010 = df.loc[df['YrSold_2010'] == 1]

    return df_0609, df_2010
