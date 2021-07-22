from data.glassnode import GlassnodeClient
import pandas as pd

class GlassnodeRetrieve():
    def get_glassnode_data(self, start_date):
        """
        Use glassnode API to retrieve data for dictionary of indicators, and return a merged dataframe.
        """
        
        gn = GlassnodeClient()
        gn.set_api_key('1paIjI1fhjUKmH0fMu6OEpAR1ph')

        # Set API parameters and metric URLs
        api_param = {'url' : '',
                     'a' : 'BTC',
                     's' : start_date,
                     'i' : '24h'
                    }

        indicator_dict = {'nupl' : {'url' : 'https://api.glassnode.com/v1/metrics/indicators/net_unrealized_profit_loss'},
                          'stfd' : {'url' : 'https://api.glassnode.com/v1/metrics/indicators/stock_to_flow_deflection'},
                          'market_to_thermo' : {'url' : 'https://api.glassnode.com/v1/metrics/mining/marketcap_thermocap_ratio'},
                          'perc_supply_profit' : {'url' : 'https://api.glassnode.com/v1/metrics/supply/profit_relative'},
                          'puell' : {'url' : 'https://api.glassnode.com/v1/metrics/indicators/puell_multiple'},
                          'active_addresses' : {'url' : 'https://api.glassnode.com/v1/metrics/addresses/active_count'},
                          'new_addresses' : {'url' : 'https://api.glassnode.com/v1/metrics/addresses/new_non_zero_count'},
                          'transactions' : {'url' : 'https://api.glassnode.com/v1/metrics/transactions/count'},
                          'net_transfer_volume' : {'url' : 'https://api.glassnode.com/v1/metrics/transactions/transfers_volume_exchanges_net'},
                          'hash_rate' : {'url' : 'https://api.glassnode.com/v1/metrics/mining/hash_rate_mean'},
                          'mining_difficulty' : {'url' : 'https://api.glassnode.com/v1/metrics/mining/difficulty_latest'},
                          'transaction_fees' : {'url' : 'https://api.glassnode.com/v1/metrics/fees/volume_mean'}
                         }
        
        # Retrieve data
        for key in indicator_dict:
            api_param['url'] = indicator_dict[key]['url']
            indicator_dict[key]['data'] = gn.get(**api_param).to_frame(name=key)

        gn_data = pd.DataFrame({'t':[]})

        for key in indicator_dict:
            gn_data = pd.merge(gn_data,
                               indicator_dict[key]['data'],
                               how='outer',
                               left_on='t',
                               right_on='t',
                              )
        
        # For hash rate and mining difficulty, convert to trillions to fit into Postgres db
        gn_data['hash_rate'] = gn_data['hash_rate'] / 1000000000000
        gn_data['mining_difficulty'] = gn_data['mining_difficulty'] / 1000000000000

        return gn_data.rename(columns={'t' : 'date'})