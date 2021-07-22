from sqlalchemy import create_engine, Column, Integer, String, Float, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL

DeclarativeBase = declarative_base()

DATABASE = {
    'drivername': 'postgres',
    'host': 'localhost',
    'port': '5432',
    'username': 'davidwismer',
    'password': 'D3c3pticon9',
    'database': 'bitcoin'
}

def db_connect():
    """
    Performs db connection using db settings in settings.py module. Returns sqlalchemy engine instance.
    """
    return create_engine(URL(**DATABASE))


def create_table(engine):
    DeclarativeBase.metadata.create_all(engine)


class GlassnodeTable(DeclarativeBase):
    __tablename__ = 'glassnode'
    
    id = Column(Integer, primary_key=True)
    date = Column('date', String, nullable=True, unique=True)  # MAKE THIS DATE TYPE
    nupl = Column('nupl', Float, nullable=True)
    stfd = Column('stfd', Float, nullable=True)
    market_to_thermo =Column('market_to_thermo', Float, nullable=True) 
    perc_supply_profit = Column('perc_supply_profit', Float, nullable=True)
    puell = Column('puell', Float, nullable=True)
    active_addresses = Column('active_addresses', Float, nullable=True)
    new_addresses = Column('new_addresses', Float, nullable=True)
    transactions = Column('transactions', Float, nullable=True)
    net_transfer_volume = Column('net_transfer_volume', Float, nullable=True)
    hash_rate = Column('hash_rate', Float, nullable=True)
    mining_difficulty = Column('mining_difficulty', Float, nullable=True)
    transaction_fees = Column('transaction_fees', Float, nullable=True)


class IchimokuTable(DeclarativeBase):
    __tablename__ = 'ichimoku'
    
    id = Column(Integer, primary_key=True)
    date = Column('date', Date, nullable=True, unique=True)
    closing_price = Column('closing_price', Float, nullable=True)
    tenkan = Column('tenkan', Float, nullable=True)
    kijun = Column('kijun', Float, nullable=True)
    span_a = Column('span_a', Float, nullable=True)
    span_b = Column('span_b', Float, nullable=True)
    lagging_span = Column('lagging_span', Float, nullable=True)
    future_span_a = Column('future_span_a', Float, nullable=True)
    future_span_b = Column('future_span_b', Float, nullable=True)
    t_over_k = Column('t_over_k', Float, nullable=True)
    t_over_k_streak = Column('t_over_k_streak', Float, nullable=True)
    price_over_t = Column('price_over_t', Float, nullable=True)
    price_over_t_streak = Column('price_over_t_streak', Float, nullable=True)
    price_over_k = Column('price_over_k', Float, nullable=True)
    price_over_k_streak = Column('price_over_k_streak', Float, nullable=True)
    price_over_cloud_top = Column('price_over_cloud_top', Float, nullable=True)
    price_over_cloud_bottom = Column('price_over_cloud_bottom', Float, nullable=True)
    cloud_over_price = Column('cloud_over_price', Float, nullable=True)
    span_a_over_b = Column('span_a_over_b', Float, nullable=True)
    future_cloud_over_price = Column('future_cloud_over_price', Float, nullable=True)
    future_span_a_over_b = Column('future_span_a_over_b', Float, nullable=True)

class VolumeTable(DeclarativeBase):
    __tablename__ = 'volume'
    
    id = Column(Integer, primary_key=True)
    date = Column('date', Date, nullable=True, unique=True)
    volume = Column('volume', Float, nullable=True)
    closing_price = Column('closing_price', Float, nullable=True)
    volume_12_day_avg = Column('volume_12_day_avg', Float, nullable=True)
    volume_26_day_avg = Column('volume_26_day_avg', Float, nullable=True)
    price_streak = Column('price_streak', Float, nullable=True)
    volume_streak = Column('volume_streak', Float, nullable=True)
    price_volume_confluence = Column('price_volume_confluence', Float, nullable=True)
    price_volume_divergence = Column('price_volume_divergence', Float, nullable=True)
     
class MACDTable(DeclarativeBase):
    __tablename__ = 'macd'
    
    id = Column(Integer, primary_key=True)
    date = Column('date', Date, nullable=True, unique=True)
    macd = Column('macd', Float, nullable=True)
    signal = Column('signal', Float, nullable=True)
    histogram = Column('histogram', Float, nullable=True)
    macd_over_signal = Column('macd_over_signal', Float, nullable=True)
    macd_over_signal_streak = Column('macd_over_signal_streak', Float, nullable=True)
    histogram_streak = Column('histogram_streak', Float, nullable=True)
    hist_magnitude = Column('hist_magnitude', Float, nullable=True)

class RSITable(DeclarativeBase):
    __tablename__ = 'rsi'
    
    id = Column(Integer, primary_key=True)
    date = Column('date', Date, nullable=True, unique=True)
    rsi = Column('rsi', Float, nullable=True)
    rsi_streak = Column('rsi_streak', Float, nullable=True)
    over_under_streak = Column('over_under_streak', Float, nullable=True)

class BollingerBandsTable(DeclarativeBase):
    __tablename__ = 'bbands'
    
    id = Column(Integer, primary_key=True)
    date = Column('date', Date, nullable=True, unique=True)
    upper = Column('upper', Float, nullable=True)
    middle = Column('middle', Float, nullable=True)
    lower = Column('lower', Float, nullable=True)
    band_size = Column('band_size', Float, nullable=True)
    band_size_vs_closing_price = Column('band_size_vs_closing_price', Float, nullable=True)
    band_size_streak = Column('band_size_streak', Float, nullable=True)
    closing_price_band_position = Column('closing_price_band_position', Float, nullable=True)


class PostTable(DeclarativeBase):
    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key=True)
    date = Column('date', Date, nullable=True, unique=True)
    title = Column('title', String, nullable=True)
    num_comments = Column('num_comments', Integer, nullable=True)
    url = Column('url', String, nullable=True)

class CommentTable(DeclarativeBase):
    __tablename__ = 'comments'
    
    id = Column(Integer, primary_key=True)
    date = Column('date', Date, nullable=True, unique=True)
    timestamp = Column('timestamp', Float, nullable=True)
    author = Column('author', Integer, nullable=True)
    body = Column('body', String, nullable=True)
    upvotes = Column('upvotes', Integer, nullable=True)
    stickied = Column('stickied', Boolean, nullable=True)

class GtrendsTable(DeclarativeBase):
    __tablename__ = 'gtrends'
    
    id = Column(Integer, primary_key=True)
    date = Column('date', Date, nullable=True, unique=True)
    unscaled_interest = Column('unscaled_interest', Integer, nullable=True)
    monthly_interest = Column('monthly_interest', Float, nullable=True)
    scale = Column('scale', Float, nullable=True)
    scaled_interest = Column('scaled_interest', Float, nullable=True)