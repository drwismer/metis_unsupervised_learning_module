import pandas as pd
from pytrends.request import TrendReq
from pytrends import dailydata


def get_gtrends(keyword, start_year, start_month, end_year, end_month):
    """
    Return dataframe with daily Google Trends data for a given keyword and time period.
    """
    
    gtrends_df = dailydata.get_daily_data(keyword, start_year, start_month, end_year, end_month)

    gtrends_df = gtrends_df.drop(columns='isPartial')
    
    column_dict = {keyword + '_unscaled' : 'unscaled_interest',
                   keyword + '_monthly' : 'monthly_interest',
                   keyword : 'scaled_interest'
                  }

    gtrends_df = gtrends_df.rename(columns=column_dict)
    gtrends_df.reset_index(inplace=True)
    
    return gtrends_df