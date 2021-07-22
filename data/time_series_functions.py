import pandas as pd
import numpy as np
from scipy.stats import linregress

def streak_column(two_columns):
    """
    Accepts a 2 column df and returns a series that provides the streaks for which column A is greater than column B
    (positive integer) and where column B is greater than column A (negative integer).
    """
    two_columns['A>B'] = np.where(two_columns.iloc[:,0].isna() | two_columns.iloc[:,1].isna(),
                                  np.nan,
                                  two_columns.iloc[:,0] > two_columns.iloc[:,1]
                                 )
    two_columns['streak_start'] = two_columns['A>B'].ne(two_columns['A>B'].shift(1))
    two_columns['streak_id'] = two_columns['streak_start'].cumsum()
    two_columns['streak_counter'] = np.where(two_columns.iloc[:,0].isna() | two_columns.iloc[:,1].isna(),
                                             np.nan,
                                             (two_columns.groupby('streak_id').cumcount() + 1) * np.where(two_columns['A>B'] == True, 1, -1)
                                            )
    
    return two_columns['streak_counter']


def confluence_divergence(streaks, conf_div):
    """
    Accepts a 2 column df where each column represents the streaks of a single measure. Returns a series that represents
    confluence or divergence of the two columns. Divergence measures the length of a streak where signs are opposite in the
    two columns, whereas confluence measures the length of a streak where signs are the same. For confluence, the sign of 
    the returned series will be positive for streaks of increases and negative for streaks of decreases. For divergence, the
    sign of the returned series will always be based on whether the first column provided is increasing or decreasing.
    """
    if conf_div == 'conf':
        streaks.loc[(streaks.iloc[:,0] > 0) & (streaks.iloc[:,1] > 0), 'conf'] = streaks.iloc[:,0:2].min(axis=1)
        streaks.loc[(streaks.iloc[:,0] < 0) & (streaks.iloc[:,1] < 0), 'conf'] = streaks.iloc[:,0:2].max(axis=1)
        streaks.loc[(streaks.iloc[:,0] > 0) & (streaks.iloc[:,1] < 0), 'conf'] = 0
        streaks.loc[(streaks.iloc[:,0] < 0) & (streaks.iloc[:,1] > 0), 'conf'] = 0
        return streaks['conf']
    
    if conf_div == 'div':
        streaks.loc[(streaks.iloc[:,0] > 0) & (streaks.iloc[:,1] > 0), 'div'] = 0
        streaks.loc[(streaks.iloc[:,0] < 0) & (streaks.iloc[:,1] < 0), 'div'] = 0
        streaks['abs_1'] = streaks.iloc[:,0].abs()
        streaks['abs_2'] = streaks.iloc[:,1].abs()
        streaks.loc[(streaks.iloc[:,0] > 0) & (streaks.iloc[:,1] < 0), 'div'] = streaks.iloc[:,-2:].min(axis=1)
        streaks.loc[(streaks.iloc[:,0] < 0) & (streaks.iloc[:,1] > 0), 'div'] = streaks.iloc[:,-2:].min(axis=1) * -1
        return streaks['div']


def hist_magnitude(hist_series, periods):
    """
    Calculate MACD histogram magnitude in a new series. Compare current histogram value against prior X period average 
    in absolute value and apply sign of current histogram value.
    """
    df = hist_series.to_frame()
    df['hist_abs'] = df.iloc[:,0].abs()
    df['hist_abs_avg'] = df['hist_abs'].rolling(window=periods).mean()
    df['hist_magnitude'] = df.iloc[:,0] / df['hist_abs_avg']
    
    return df['hist_magnitude']

def get_slope(array):
    """
    Accept array, return slope of the regression line.
    """
    y = np.array(array)
    x = np.arange(len(y))
    slope, intercept, r_value, p_value, std_err = linregress(x,y)
    
    return slope

def add_regression_column(df, col_name, window):
    """
    Create rolling regression, rolling average, and normalized regression columns for a given column 
    in a df. Create percentile column for normalized regression. Return the df.
    """
    df[col_name + '_reg' + str(window)] = df[col_name].rolling(window=window, min_periods=window)\
                                                      .apply(get_slope, raw=False).reset_index(0, drop=True)
    
    df[col_name + '_avg' + str(window)] = abs(df[col_name].rolling(window=window, min_periods=window)
                                              .mean()
                                             )
    
    df[col_name + '_reg_norm' + str(window)] = (df[col_name + '_reg' + str(window)] / 
                                                df[col_name + '_avg' + str(window)]
                                               )
    
    df[col_name + '_reg_norm' + str(window) + '_perc'] = df[col_name + '_reg_norm' + str(window)].rank(pct = True)
    
    return df

def missing_dates_by_year(df, date_column, count_column):
    """
    Accept df with date column and return missing dates by year.
    """
    df = df.groupby(date_column)[[count_column]].count().reset_index()
    
    start_date = df[date_column].min()
    end_date = df[date_column].max()
    complete_datelist = pd.date_range(start=start_date,end=end_date).to_pydatetime().tolist()
    complete_datelist = [date.date() for date in complete_datelist]
    
    df_datelist = df[date_column].values
    
    missing_dates = [date for date in complete_datelist if date not in df_datelist]
    
    missing_df = pd.DataFrame({'missing_dates' : missing_dates})
    missing_df['year'] = missing_df.apply(lambda row: row['missing_dates'].year, axis=1)
    
    missing_df = missing_df.groupby('year').count().reset_index()
    
    return missing_dates, missing_df

def vs_previous_high(df, date_column, ath_column, window=None, function='max'):
    """
    Accept df and return new df with all-time high and percent of all-time high columns.
    """
    df.sort_values(date_column, inplace=True)
    
    if window:
        if function=='max':
            df[ath_column + '_high_prior_max_' + str(window)] = df[ath_column].rolling(window=window).max()
            df[ath_column + '_vs_high_prior_max_' + str(window)] = df[ath_column] / df[ath_column + '_high_prior_max_' + str(window)]
        if function=='median':
            df[ath_column + '_high_prior_median_' + str(window)] = df[ath_column].rolling(window=window).median()
            df[ath_column + '_vs_high_prior_median_' + str(window)] = df[ath_column] / df[ath_column + '_high_prior_median_' + str(window)]
    else:    
        if function=='max':
            df[ath_column + '_ath'] = df[ath_column].cummax()
            df[ath_column + '_vs_ath'] = df[ath_column] / df[ath_column + '_ath']
        if function=='median':
            df[ath_column + '_all_time_median'] = df[ath_column].expanding().median()
            df[ath_column + '_vs_all_time_median'] = df[ath_column] / df[ath_column + '_all_time_median']
    
    return df