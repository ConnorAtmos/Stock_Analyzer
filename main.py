import datetime
import os
import time

import plotly.express as px

from toolbox import database
from toolbox import ticker_prices
from toolbox import ticker_retreival
from toolbox import ticker_price_analysis
from toolbox import ticker_plotter

storage_path = "/mnt/nvme1n1p1/"
database_path = os.path.join(storage_path, "database")

database.set_storage_path(database_path)
ticker_retreival.set_storage_path(database_path)
ticker_prices.set_storage_path(database_path)
ticker_price_analysis.set_storage_path(database_path)
ticker_plotter.set_storage_path(database_path)

days_to_refresh = 1


def main():

    ticker = "AMZN"
    print(f"Getting {ticker} historical data")
    start_time = time.time()
    trend = ticker_prices.get_ticker_historical_trend(ticker, cooldown=False, database_only=False)

    # Create columns variable that does not contain the Date and Volume column
    columns = trend.columns
    columns = columns.drop("Volume")

    trend_fig = ticker_plotter.get_figure(trend, columns, title=f"{ticker} Price")

    # Save the figure as a png
    trend_fig.write_image(f"{ticker}_trend.png")

    # Create a candlestick figure
    candlestick_fig = ticker_plotter.get_candlestick_figure(trend, title=f"{ticker} Candlestick")

    # Save the figure as a png
    candlestick_fig.write_image(f"{ticker}_candlestick.png")

    # Get velocity of prices
    velocity = ticker_price_analysis.diff(trend)
    velocity_fig = ticker_plotter.get_figure(velocity, columns, title=f"{ticker} Velocity")

    # Save the figure as a png
    velocity_fig.write_image(f"{ticker}_velocity.png")

    # Get acceleration of prices
    acceleration = ticker_price_analysis.diff(velocity)
    acceleration_fig = ticker_plotter.get_figure(acceleration, columns, title=f"{ticker} Acceleration")

    # Save the figure as a png
    acceleration_fig.write_image(f"{ticker}_acceleration.png")

    end_time = time.time()
    print(f"Time taken: {end_time - start_time}")



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
