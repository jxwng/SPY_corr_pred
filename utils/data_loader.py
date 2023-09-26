import yfinance as yf
from joblib import Memory

MEMORY = Memory(location='~/.cache', verbose=1)


@MEMORY.cache
def load_px(stocks, start_date, end_date):
    """
    download historical prices of equities
    :return:
    """
    df = yf.download(stocks, start=start_date, end=end_date).xs('Adj Close', axis=1)
    return df


@MEMORY.cache
def load_ret(stocks, start_date, end_date):
    px = load_px(stocks, start_date, end_date)
    return px.pct_change()


def load_corr(stocks, start_date, end_date, window=60):
    ret = load_ret(stocks, start_date, end_date)
    corr = ret.rolling(window=window, min_periods=window).corr(ret['SPY']).tail()
    return corr


if __name__ == '__main__':
    univ = ['AMZN', 'GME', 'GOOG', 'JPM', 'SPY', 'XOM']
    corr = load_corr(stocks=univ, start_date='2023-01-01', end_date='2023-09-01')
    print(corr.tail())
