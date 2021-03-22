def functional_numeric(x):
    '''
    Creating a new numeric ordinal variable for 'Functional'
    '''
    if 'Typ' in x:
        return 8
    elif 'Min1' in x:
        return 7
    elif 'Min2' in x:
        return 6
    elif 'Mod' in x:
        return 5
    elif 'Maj1' in x:
        return 4
    elif 'Maj2' in x:
        return 3
    elif 'Sev' in x:
        return 2
    else:
        return 1


def extercond_numeric(x):
    '''
    Creating a new numeric ordinal variable for external conditon or 'ExterCond'
    '''
    if 'Ex' in x:
        return 5
    elif 'Gd' in x:
        return 4
    elif 'TA' in x:
        return 3
    elif 'Fa' in x:
        return 2
    else:
        return 1


def exterqual_numeric(x):
    '''
    Creating a new numeric ordinal variable for external quality or 'ExterQual'
    '''
    if 'Ex' in x:
        return 5
    elif 'Gd' in x:
        return 4
    elif 'TA' in x:
        return 3
    elif 'Fa' in x:
        return 2
    else:
        return 1


def add_neighborhood_loc(x):
    '''
    Function to make numbers from neighborhood categorial feature
    '''
    if 'MeadowV' in x or 'Edwards' in x or 'Sawyer' in x or 'Landmrk' in x or 'SWISU' in x or 'BrDale' in x or 'IDOTRR' in x:
        return 1
    elif 'NAmes' in x or 'Mitchel' in x or 'BrkSide' in x or 'NPkVill' in x or 'OldTown' in x or 'ClearCr' in x or 'Gilbert' in x:
        return 2
    elif 'SawyerW' in x or 'NWAmes' in x or 'Crawfor' in x or 'CollgCr' in x or 'Blueste' in x or 'GrnHill' in x or 'Blmngtn' in x:
        return 3
    else:
        return 4


def add_location_feature(df_exout):
    '''
    Add location feature to df
    Return: df, dataframe with new feature
    '''
    df_exout['Functional_Num'] = df_exout.Functional.map(functional_numeric)
    df_exout['ExterCond_Num'] = df_exout.ExterCond.map(extercond_numeric)
    df_exout['ExterQual_Num'] = df_exout.ExterQual.map(exterqual_numeric)
    df_exout['Location'] = ((df_exout['OverallQual']/df_exout['OverallQual'].mean())
                            + (df_exout['OverallCond']/df_exout['OverallCond'].mean())
                            + (df_exout['ExterQual_Num']/df_exout['ExterQual_Num'].mean())
                            + (df_exout['ExterCond_Num']/df_exout['ExterCond_Num'].mean())
                            + (df_exout['Functional_Num']/df_exout['Functional_Num'].mean()))
    df_exout['Location'] = df_exout.Neighborhood.map(add_neighborhood_loc)

    return df_exout
