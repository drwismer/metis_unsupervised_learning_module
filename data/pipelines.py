from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from bitcoin_metis.sql_model import *


class BitcoinPipeline:
    def __init__(self):
        """
        Initializes db connection and sessionmaker. Creates postgres table.
        """
        engine = bitcoin_metis.sql_model.db_connect()
        bitcoin_metis.sql_model.create_table(engine)
        self.Session = sessionmaker(bind=engine)