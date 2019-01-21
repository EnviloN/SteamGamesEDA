import numpy as np
import pandas as pd
import datetime as dt

months = set(['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])

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

def supports_english(row):
    '''Function estimates if a game supports English language.'''
    if 'English' in row['SupportedLanguages']:
        return True
    else:
        return False

def count_languages(row,languages):
    '''Function counts all supported languages.'''
    cnt = 0
    for lang in languages:
        if lang in row['SupportedLanguages']:
            cnt += 1
    return cnt

def find_invalid_dates(df, format_str):
    '''Function picks up any invalid values in the ReleaseDate column.'''
    invalid = set()
    for date_str in df.ReleaseDate:
        try:
            dt.datetime.strptime(date_str, format_str)
        except ValueError:
            invalid.add(date_str)
    return invalid

def find_invalid_dates(df, format_str):
    '''Function picks up any invalid values in the ReleaseDate column.'''
    invalid = set()
    for date_str in df.ReleaseDate:
        try:
            dt.datetime.strptime(date_str, format_str)
        except ValueError:
            invalid.add(date_str)
    return invalid

def manual_dt_approx(date_str):
    '''Manual replacement of invalid release dates.'''
    date_str = date_str.replace("Dec 2016 - Early", "Jan")
    date_str = date_str.replace("Dec 2016 / Early", "Jan")
    date_str = date_str.replace("Q1", "Feb")
    date_str = date_str.replace("1st Quarter", "Feb")
    date_str = date_str.replace("Q2", "May")
    date_str = date_str.replace("Q 2", "May")
    date_str = date_str.replace("Q3", "Aug")
    date_str = date_str.replace("Q4", "Nov")
    date_str = date_str.replace("Christmas", "Dec 24th")
    date_str = date_str.replace("CHRISTMAS", "Dec 24th")
    date_str = date_str.replace("Clicking Begins Nov", "Nov")
    date_str = date_str.replace("Coming", "")
    date_str = date_str.replace("2016 (Early Access)", "2016")
    date_str = date_str.replace("End of", "Dec")
    date_str = date_str.replace("End", "Dec")
    date_str = date_str.replace("1st - ", "")
    date_str = date_str.replace("Nov.", "Nov ")
    date_str = date_str.replace("2016!", "2016")
    date_str = date_str.replace(" Early Access", "")
    date_str = date_str.replace("Nov (ish)", "Nov")
    date_str = date_str.replace("2016Nov", "Nov 2016")
    date_str = date_str.replace("EA Nov", "Nov")
    date_str = date_str.replace("Summer of", "Jul")
    date_str = date_str.replace("Sept", "Sep")
    date_str = date_str.replace("Nov  of", "Nov")
    date_str = date_str.replace("Late Summer -", "Sep")
    date_str = date_str.replace("Late Fall", "Nov")
    date_str = date_str.replace("Halloween", "October 31")
    date_str = date_str.replace("Holiday", "Jul")
    date_str = date_str.replace("Autumn", "Oct")
    date_str = date_str.replace("Late", "Dec")
    date_str = date_str.replace("Summer", "Jul")
    date_str = date_str.replace("MID", "Jul")
    date_str = date_str.replace("Mid-", "Jul ")
    date_str = date_str.replace("Spring", "Apr")
    date_str = date_str.replace("Fall", "Oct")
    date_str = date_str.replace("early", "Jan")
    date_str = date_str.replace("Early", "Jan")
    date_str = date_str.replace("The end of", "Dec")
    date_str = date_str.replace("Sepember", "Sep")
    date_str = date_str.replace(" November", "Nov")
    date_str = date_str.replace(" May", "May")
    
    return date_str

def replace_datetime(date_str, format_str):
    '''Function tries to apply one of known format strings to the date and change its format accordingly.'''
    format_strings = ["%b %Y", "%dth %B %Y", "%dst %B %Y", "%B %d %Y", "%x", "%m-%Y", "%m - %Y", "%d %B %Y", \
                     "%b - %Y", "%B - %Y", "%B %Y", "%B %dth %Y", "%b %dth %Y", "%dth of %B %Y", "%d.%m.%Y", \
                     "%Y %b", "%Y-%d-%m"]
    
    date_str = manual_dt_approx(date_str)
    original = date_str
    
    for dtFormat in format_strings:
        try:
            date_str = dt.datetime.strptime(date_str, dtFormat).strftime("%b %d %Y")
            if date_str != original: return date_str
        except ValueError:
            ...
    return date_str

def fix_invalid_date(date_str, format_str):
    '''Function checks if the date-time is valid and tries to fix it if not.'''
    fixed = date_str
    try:
        dt.datetime.strptime(date_str, format_str)
    except ValueError:
        fixed = replace_datetime(date_str, format_str)
    return fixed