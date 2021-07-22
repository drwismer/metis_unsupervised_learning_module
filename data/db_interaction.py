from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from data.sql_model import *
import pandas as pd

class DatabaseInteraction:
    def __init__(self):
        """
        Initializes db connection and sessionmaker. Creates postgres table.
        """
        self.engine = db_connect()
        create_table(self.engine)
        self.Session = sessionmaker(bind=self.engine)
    
    
    def df_to_db(self, table_name, data, pd_if_exists='replace'):
        """
        Load pandas df to the postgres database. Replaces old data.
        """
        #session = self.Session()
        data.to_sql(table_name, con=self.engine, if_exists=pd_if_exists, index=False)

    
    def query_latest(self, table_name, column_name):
        """
        Return latest date from given table column.
        """
        latest = self.engine.execute('SELECT ' + column_name
                                     + ' FROM ' + table_name
                                     + ' ORDER BY ' + column_name + ' DESC'
                                     + ' LIMIT 1'
                                    )
        
        return latest.fetchone()[column_name]
    
    
    def query_all_data(self, table_name):
        """
        Return an entire db table query for a given table.
        """
        query = self.engine.execute('SELECT * '
                                    + 'FROM ' + table_name
                                   )
        return query
    
    def query_candles(self, table_name, exchange, coin, start, end):
        """
        Get db candle data give date, coin, and exchange parameters.
        """
        query = self.engine.execute('SELECT * '
                                    + 'FROM ' + table_name + ' '
                                    + 'WHERE timestamp >= ' + str(start) + ' '
                                    + 'AND timestamp <= ' + str(end) + ' '
                                    + 'AND exchange = \'' + exchange + '\' '
                                    + 'AND symbol = \'' + coin + '\''
                                   )
        print(query)
        return query
    
    
    def query_to_df(self, query):
        """
        Convert query to df.
        """
        df = pd.DataFrame(query.fetchall())
        df.columns = query.keys()
        return df
