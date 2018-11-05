import numpy as np
import pandas as pd

def delete_duplicates(df):
    '''Function filters out duplicate games from the dataset.'''

    # create a mask of all duplicates and find games that have these duplicates
    duplicate_mask = df.duplicated(subset=['ResponseName'], keep=False) 
    duplicates = df[duplicate_mask]
    duplicit_games = list(duplicates.ResponseName.unique())

    # for each game estimate which duplicate we want to keep and update the mask
    for game in duplicit_games:
        sample = df[df.ResponseName == game].index.values # all duplicates of the games
        
        # find the best one
        max_id = sample[0]
        max_coef = valid_coef(df,max_id)
        for i in sample:
            current_coef = valid_coef(df,i)
            if max_coef < current_coef:
                max_coef = current_coef
                max_id = i
        
        duplicate_mask[max_id] = False # we'll keep this one

    df.drop(df[duplicate_mask].index, axis=0, inplace=True) # drop all other duplicates
    return df

def valid_coef(df, i):
    '''Function estimates the entry's validity.'''
    # Only this columns should be affected
    columns = ['SteamSpyOwners', 'SteamSpyOwnersVariance', 'SteamSpyPlayersEstimate', 'SteamSpyPlayersVariance']
    return df.iloc[i][columns].sum() # sum up the values