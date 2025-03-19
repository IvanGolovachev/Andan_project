import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests
from xml.etree import ElementTree as ET
from datetime import datetime
import warnings
warnings.filterwarnings("ignore")


def stock_moex(date_from, ticker, timeframe):

  url = f"https://iss.moex.com/iss/engines/stock/markets/shares/securities/{ticker}/candles.json"
  params = {
      'from': date_from,
      'interval': timeframe,
      }
  response = requests.get(url, params=params)
  data = response.json()
  columns = data["candles"]["columns"]
  rows = data["candles"]["data"]
  df = pd.DataFrame(rows, columns=columns)

  df.columns = [f'open_{ticker}', f'close_{ticker}', f'high_{ticker}', f'low_{ticker}', f'value_{ticker}', f'volume_{ticker}', f'begin', f'end_{ticker}']
  df = df.set_index('begin')
  df = df.drop([f'value_{ticker}', f'volume_{ticker}', f'end_{ticker}'], axis=1)


  return df


def futures_moex(date_from, ticker, timeframe):

  url = f"https://iss.moex.com/iss/engines/futures/markets/forts/securities/{ticker}/candles.json"

  params = {
      'from': date_from,
      'interval': timeframe,
      }
  response = requests.get(url, params=params)
  response.raise_for_status()
  data = response.json()
  columns = data["candles"]["columns"]
  rows = data["candles"]["data"]
  df = pd.DataFrame(rows, columns=columns)

  df.columns = [f'open_{ticker}', f'close_{ticker}', f'high_{ticker}', f'low_{ticker}', f'value_{ticker}', f'volume_{ticker}', f'begin', f'end_{ticker}']
  df = df.set_index('begin')
  df = df.drop([f'value_{ticker}', f'volume_{ticker}', f'end_{ticker}'], axis=1)

  return df


def parser_moex(data, stock_ticker, futures_ticker, timeframe):
    stock_df = stock_moex(data, stock_ticker, timeframe)
    futures_df = futures_moex(data, futures_ticker, timeframe)

    df = pd.merge(stock_df, futures_df, how='inner', on='begin')
    

    return df