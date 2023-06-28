import os, datetime, requests, time
import pandas as pd
from toolbox import database
from toolbox import ticker_prices


def set_storage_path(database_path: str, make_dir=False):
    """
    Params
    ------
    database_path: str
        Path to the database
    make_dir: bool
        If True, create the directory if it does not exist

    Returns
    -------
    None

    Notes
    -----
    This function is used to set the path to the database. The database is a

    Examples
    --------
    from toolbox import ticker_price_analysis
    ticker_price_analysis.set_storage_path('~/Desktop/database', make_dir=True)
    """

    if make_dir:
        if not os.path.exists(database_path):
            os.makedirs(database_path)

    database.set_storage_path(database_path)
    ticker_prices.set_storage_path(database_path)


def diff(df: pd.DataFrame):
    """
    Parameters
    ----------
    df: pd.DataFrame
        Dataframe with datetime index and columns of prices

    Returns
    -------
    diff_df: pd.DataFrame
        Dataframe with datetime index and columns of differences in prices

    Notes
    -----
    This function is used to get the difference between the price of each datetime

    Examples
    --------
    from toolbox import ticker_price_analysis
    import pandas as pd
    df = pd.DataFrame({'price': [1, 2, 3, 4, 5]}, index=pd.date_range('2020-01-01', periods=5, freq='1min'))
    velocity_df = ticker_price_analysis.diff(df)
    print(velocity_df)
    """

    diff_df = pd.DataFrame(columns=df.columns)

    # get the difference, by taking the difference between the closing price of each datetime
    # And dividing by the difference in time between each datetime, in minutes
    for column in df.columns:
        diff_df[column] = df[column].diff()

    return diff_df


def get_pct_change(df: pd.DataFrame):
    """
    Parameters
    ----------
    df: pd.DataFrame
        Dataframe with datetime index and columns of prices

    Returns
    -------
    pct_change_df: pd.DataFrame
        Dataframe with datetime index and columns of percent change in prices

    Notes
    -----
    This function is used to get the percent change between the price of each datetime

    Examples
    --------
    from toolbox import ticker_price_analysis
    import pandas as pd
    df = pd.DataFrame({'price': [1, 2, 3, 4, 5]}, index=pd.date_range('2020-01-01', periods=5, freq='1min'))
    pct_change_trend = ticker_price_analysis.get_pct_change(df)
    print(pct_change_trend)
    """

    # Create new df with same columns as df
    pct_change_df = pd.DataFrame(columns=df.columns)

    # get the difference, by taking the difference between the closing price of each datetime
    # And dividing by the difference in time between each datetime, in minutes
    for column in df.columns:
        pct_change_df[column] = df[column].diff() / df[column].shift(1) * 100

    return pct_change_df


def get_velocity(ticker: str, start_date=None, end_date=None, cooldown=True, database_only=False, interval="1d"):
    """
    Parameters
    ----------
    ticker: str
        Ticker symbol

    start_date: datetime.datetime
        Start date of the data

    end_date: datetime.datetime
        End date of the data

    cooldown: bool
        If True, wait 1 second between each request to the API

    database_only: bool
        If True, only use the database, do not make any requests to the API

    Returns
    -------
    velocity_df: pd.DataFrame
        Dataframe with datetime index and columns of velocity

    Notes
    -----
    This function is used to get the velocity of the ticker

    Examples
    --------
    from toolbox import ticker_price_analysis
    velocity_df = ticker_price_analysis.get_velocity('AAPL')
    print(velocity_df)
    """

    df = ticker_prices.get_ticker_historical_trend(ticker, start_date, end_date, cooldown=cooldown,
                                                   database_only=database_only, interval=interval)

    return diff(df)


def get_acceleration(ticker: str, start_date=None, end_date=None, cooldown=True, database_only=False, interval="1d"):
    """
    Parameters
    ----------
    ticker: str
        Ticker symbol

    start_date: datetime.datetime
        Start date of the data

    end_date: datetime.datetime
        End date of the data

    cooldown: bool
        If True, wait 1 second between each request to the API

    database_only: bool
        If True, only use the database, do not make any requests to the API

    Returns
    -------
    acceleration_df: pd.DataFrame
        Dataframe with datetime index and columns of acceleration

    Notes
    -----
    This function is used to get the acceleration of the ticker

    Examples
    --------
    from toolbox import ticker_price_analysis
    acceleration_df = ticker_price_analysis.get_acceleration('AAPL')
    print(acceleration_df)
    """

    df = ticker_prices.get_ticker_historical_trend(ticker, start_date, end_date, cooldown=cooldown,
                                                   database_only=database_only, interval=interval)

    return diff(diff(df))


def get_jerk(ticker: str, start_date=None, end_date=None, cooldown=True, database_only=False, interval="1d"):
    """
    Parameters
    ----------
    ticker: str
        Ticker symbol

    start_date: datetime.datetime
        Start date of the data

    end_date: datetime.datetime
        End date of the data

    cooldown: bool
        If True, wait 1 second between each request to the API

    database_only: bool
        If True, only use the database, do not make any requests to the API

    Returns
    -------
    jerk_df: pd.DataFrame
        Dataframe with datetime index and columns of jerk

    Notes
    -----
    This function is used to get the jerk of the ticker

    Examples
    --------
    from toolbox import ticker_price_analysis
    jerk_df = ticker_price_analysis.get_jerk('AAPL')
    print(jerk_df)
    """

    df = ticker_prices.get_ticker_historical_trend(ticker, start_date, end_date, cooldown=cooldown,
                                                   database_only=database_only, interval=interval)

    return diff(diff(diff(df)))

def get_pct_change_velocity(ticker: str, start_date=None, end_date=None, cooldown=True, database_only=False, interval="1d"):
    """
    Parameters
    ----------
    ticker: str
        Ticker symbol

    start_date: datetime.datetime
        Start date of the data

    end_date: datetime.datetime
        End date of the data

    cooldown: bool
        If True, wait 1 second between each request to the API

    database_only: bool
        If True, only use the database, do not make any requests to the API

    Returns
    -------
    pct_change_velocity_df: pd.DataFrame
        Dataframe with datetime index and columns of percent change velocity

    Notes
    -----
    This function is used to get the percent change velocity of the ticker

    Examples
    --------
    from toolbox import ticker_price_analysis
    pct_change_velocity_df = ticker_price_analysis.get_pct_change_velocity('AAPL')
    print(pct_change_velocity_df)
    """

    df = ticker_prices.get_ticker_historical_trend(ticker, start_date, end_date, cooldown=cooldown,
                                                   database_only=database_only, interval=interval)

    return get_pct_change(diff(df))


def get_pct_change_acceleration(ticker: str, start_date=None, end_date=None, cooldown=True, database_only=False, interval="1d"):
    """
    Parameters
    ----------
    ticker: str
        Ticker symbol
    start_date: datetime.datetime
        Start date of the data
    end_date: datetime.datetime
        End date of the data
    cooldown: bool
        If True, wait 1 second between each request to the API
    database_only: bool
        If True, only use the database, do not make any requests to the API

    Returns
    -------
    pct_change_acceleration_df: pd.DataFrame
        Dataframe with datetime index and columns of percent change acceleration

    Notes
    -----
    This function is used to get the percent change acceleration of the ticker

    Examples
    --------
    from toolbox import ticker_price_analysis
    pct_change_acceleration_df = ticker_price_analysis.get_pct_change_acceleration('AAPL')
    print(pct_change_acceleration_df)
    """

    df = ticker_prices.get_ticker_historical_trend(ticker, start_date, end_date, cooldown=cooldown,
                                                   database_only=database_only, interval=interval)

    return get_pct_change(diff(diff(df)))


def get_pct_change_jerk(ticker: str, start_date=None, end_date=None, cooldown=True, database_only=False, interval="1d"):
    """
    Parameters
    ----------
    ticker: str
        Ticker symbol
    start_date: datetime.datetime
        Start date of the data
    end_date: datetime.datetime
        End date of the data
    cooldown: bool
        If True, wait 1 second between each request to the API
    database_only: bool
        If True, only use the database, do not make any requests to the API

    Returns
    -------
    pct_change_jerk_df: pd.DataFrame
        Dataframe with datetime index and columns of percent change jerk

    Notes
    -----
    This function is used to get the percent change jerk of the ticker

    Examples
    --------
    from toolbox import ticker_price_analysis
    pct_change_jerk_df = ticker_price_analysis.get_pct_change_jerk('AAPL')
    print(pct_change_jerk_df)
    """

    df = ticker_prices.get_ticker_historical_trend(ticker, start_date, end_date, cooldown=cooldown,
                                                   database_only=database_only, interval=interval)

    return get_pct_change(diff(diff(diff(df))))