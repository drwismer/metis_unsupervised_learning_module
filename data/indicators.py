import jesse.indicators as ta
import pandas as pd
from datetime import datetime
from datetime import timedelta
import numpy as np
from data.time_series_functions import *


def candles_to_ichimoku(candles):
    """
    Accept candles data. Return Ichimoku Cloud pandas table.
    """
    
    # Specify Ichimoku Settings
    conv = 20
    base = 60
    lag = 120
    displace = 30

    # Build array of cloud metrics, add column names, add date and closing price columns
    cloud_array = []
    dates = []
    closing_prices = []

    for i in range(len(candles) - (lag + displace)):
        cloud_array.append(ta.ichimoku_cloud_seq(candles=candles[:(lag + displace + i)], 
                                  conversion_line_period=conv, 
                                  base_line_period=base,
                                  lagging_line_period=lag,
                                  displacement=displace
                                 )
                          )
        dates.append((datetime.fromtimestamp(candles[lag + displace + i][0] / 1000)).date())
        closing_prices.append(candles[lag + displace + i][2])

    cloud_columns = {0 : 'tenkan',
                     1 : 'kijun',
                     2 : 'span_a',
                     3 : 'span_b',
                     4 : 'lagging_span',
                     5 : 'future_span_a',
                     6 : 'future_span_b'
                   }
    cloud_df = pd.DataFrame(list(map(np.ravel, cloud_array))).rename(columns=cloud_columns)
    cloud_df['date'] = dates
    cloud_df['closing_price'] = closing_prices
    
    # Calculate additional Ichimoku Cloud related columns
    cloud_df['t_over_k'] = cloud_df['tenkan'] / cloud_df['kijun']
    cloud_df['t_over_k_streak'] = streak_column(cloud_df[['tenkan', 'kijun']].copy())
    cloud_df['price_over_t'] = cloud_df['closing_price'] / cloud_df['tenkan']
    cloud_df['price_over_t_streak'] = streak_column(cloud_df[['closing_price', 'tenkan']].copy())
    cloud_df['price_over_k'] = cloud_df['closing_price'] / cloud_df['kijun']
    cloud_df['price_over_k_streak'] = streak_column(cloud_df[['closing_price', 'kijun']].copy())
    cloud_df['price_over_cloud_top'] = cloud_df['closing_price'] / cloud_df[['span_a', 'span_b']].max(axis=1) 
    cloud_df['price_over_cloud_bottom'] = cloud_df['closing_price'] / cloud_df[['span_a', 'span_b']].min(axis=1)
    cloud_df['cloud_over_price'] = abs(cloud_df['span_a'] - cloud_df['span_b']) / cloud_df['closing_price']
    cloud_df['span_a_over_b'] = cloud_df['span_a'] / cloud_df['span_b']
    cloud_df['future_cloud_over_price'] = abs(cloud_df['future_span_a'] - cloud_df['future_span_b']) / cloud_df['closing_price']
    cloud_df['future_span_a_over_b'] = cloud_df['future_span_a'] / cloud_df['future_span_b']
    
    return cloud_df


def candles_to_volume(candles):
    """
    Accept candles data. Return Volume related pandas table.
    """
    
    # Create df from candle data
    volume_df = pd.DataFrame()
    volume_df['date'] = [datetime.fromtimestamp(row[0] / 1000).date() for row in candles]
    volume_df['volume'] = [row[5] for row in candles]
    volume_df['closing_price'] = [row[2] for row in candles]

    # Calculate other volume columns and price volume movement columns
    volume_df['volume_12_day_avg'] = volume_df.iloc[:,1].rolling(window=12).mean()
    volume_df['volume_26_day_avg'] = volume_df.iloc[:,1].rolling(window=26).mean()
    volume_df['volume_12_over_26_streak'] = streak_column(volume_df[['volume_12_day_avg', 'volume_26_day_avg']].copy())
    volume_df['price_streak'] = streak_column(pd.concat([volume_df['closing_price'].copy(),volume_df['closing_price'].shift(1).copy()], axis=1))
    volume_df['volume_streak'] = streak_column(pd.concat([volume_df['volume'].copy(),volume_df['volume'].shift(1).copy()], axis=1))
    volume_df['price_volume_confluence'] = confluence_divergence(volume_df[['price_streak', 'volume_streak']].copy(), 'conf')
    volume_df['price_volume_divergence'] = confluence_divergence(volume_df[['price_streak', 'volume_streak']].copy(), 'div')
    
    return volume_df
    

def candles_to_macd(candles):
    """
    Accept candles data. Return MACD related pandas table.
    """
    # Specify MACD Settings
    fast = 12
    slow = 26
    signal = 9
    
    # Build array of MACD metrics, add column names, add date column
    macd_array = []
    dates = []

    for i in range(slow + signal - 1, len(candles)):
        macd_array.append(ta.macd(candles[:i],
                                  fast_period=fast, 
                                  slow_period=slow,
                                  signal_period=signal
                                 )
                          )
        dates.append((datetime.fromtimestamp(candles[i][0] / 1000)).date())
    
    macd_columns = {0 : 'macd',
                    1 : 'signal',
                    2 : 'histogram',
                   }

    macd_df = pd.DataFrame(list(map(np.ravel, macd_array))).rename(columns=macd_columns)
    macd_df['date'] = dates

    # Drop first 100 rows (calculation is inaccurate)
    macd_df = macd_df.iloc[100:]
    
    # Calculate other MACD related columns
    macd_df['macd_over_signal'] = macd_df['macd'] / macd_df['signal']
    macd_df['macd_over_signal_streak'] = streak_column(macd_df[['macd', 'signal']].copy())
    macd_df['histogram_streak'] = streak_column(pd.concat([macd_df['histogram'].copy(),macd_df['histogram'].shift(1).copy()], axis=1))
    macd_df['hist_magnitude'] = hist_magnitude(macd_df['histogram'], 26)
    
    return macd_df


def candles_to_bbands(candles):
    # Specify Bollinger Bonds settings
    period = 20
    std_dev = 2

    # Build array of Bollinger Bands information plus dates and prices from candles data
    bbands_array = []
    dates = []
    closing_prices = []

    for i in range(period, len(candles)):
        bbands_array.append(ta.bollinger_bands(candles[:i],
                                               period=period
                                              )
                           )
        dates.append((datetime.fromtimestamp(candles[i][0] / 1000)).date())
        closing_prices.append(candles[i][2])

    bbands_columns = {0 : 'upper',
                      1 : 'middle',
                      2 : 'lower'
                     }

    bbands_df = pd.DataFrame(list(map(np.ravel, bbands_array))).rename(columns=bbands_columns)
    bbands_df['date'] = dates
    bbands_df['closing_price'] = closing_prices

    # Calculate other Bollinger Bands related columns
    bbands_df['band_size'] = bbands_df['upper'] - bbands_df['lower']
    bbands_df['band_size_streak'] = streak_column(pd.concat([bbands_df['band_size'].copy(),bbands_df['band_size'].shift(1).copy()], axis=1))
    bbands_df['band_size_vs_closing_price'] = bbands_df['band_size'] / bbands_df['closing_price']

    def conditions(row):
        # Determine the position of closing price relative to the Bollinger Bands
        if row['closing_price'] > row['upper']:
            return 1 + (row['closing_price'] - row['upper']) / row['band_size']
        elif row['closing_price'] < row['lower']:
            return 1 - (row['lower'] - row['closing_price']) / row['band_size']
        else:
            return (row['closing_price'] - row['lower']) / row['band_size']

    bbands_df['closing_price_band_position'] = bbands_df.apply(conditions, axis=1)
    
    return bbands_df


def candles_to_rsi(candles):
    """
    Accept candles data. Return RSI related pandas table.
    """
    # Specify RSI settings
    period = 14
    oversold = 70.0
    undersold = 30.0

    # Build array of RSI information and dates from candles data
    rsi_array = []
    dates = []
    closing_prices = []

    for i in range(period, len(candles)):
        rsi_array.append(ta.rsi(candles[:i],
                                period=period
                               )
                        )
        dates.append((datetime.fromtimestamp(candles[i][0] / 1000)).date())

    rsi_df = pd.DataFrame(list(map(np.ravel, rsi_array))).rename(columns={0 : 'rsi'})
    rsi_df['date'] = dates



    # Calculate other RSI related columns
    rsi_df['rsi_streak'] = streak_column(pd.concat([rsi_df['rsi'].copy(), rsi_df['rsi'].shift(1).copy()], axis=1))

    # Calculate days over and undersold and drop oversold/undersold constant columns
    rsi_df['oversold'] = oversold
    rsi_df['undersold'] = undersold
    rsi_df['periods_oversold'] = streak_column(rsi_df[['rsi', 'oversold']].copy())
    rsi_df['periods_undersold'] = streak_column(rsi_df[['undersold', 'rsi']].copy())

    rsi_df['over_under_streak'] = 0
    rsi_df['over_under_streak'][rsi_df['periods_oversold'] > 0] = rsi_df['periods_oversold']
    rsi_df['over_under_streak'][rsi_df['periods_undersold'] > 0] = rsi_df['periods_undersold'] * -1

    rsi_df = rsi_df.drop(columns=['oversold', 'undersold', 'periods_oversold', 'periods_undersold'])

    # Drop first 100 rows (calculation is inaccurate)
    rsi_df = rsi_df.iloc[100:]
    
    return rsi_df
