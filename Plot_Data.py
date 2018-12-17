"""Slice and plot"""

import os
import pandas as pd
import matplotlib.pyplot as plt
cwd = os.getcwd()






def symbol_to_path(symbol, base_dir=cwd):
    """Return CSV file path given ticker symbol."""
    return os.path.join(base_dir, "{}.csv".format(str(symbol)))


def get_data(symbols, dates):
    """Read stock data (adjusted close) for given symbols from CSV files."""
    df = pd.DataFrame(index=dates)
    if 'SPY' not in symbols:  # add SPY for reference, if absent
        symbols.insert(0, 'SPY')

    for symbol in symbols:
        filepath = symbol_to_path(symbol)
        if symbol == "SPY":
            df1 = pd.read_csv(filepath, usecols=['Date', "Adj Close"], parse_dates=True, index_col='Date',
                              na_values=["nan"])
            df1 = df1.iloc[::-1]

            df1 = df1.rename(columns={"Adj Close": symbol})

            df = df.join(df1, how='inner')

        else:
            df1 = pd.read_csv(filepath, usecols=['Date', "Adj Close"], parse_dates=True, index_col='Date',
                              na_values=["nan"])
            df1 = df1.iloc[::-1]

            df1 = df1.rename(columns={"Adj Close": symbol})
            df = df.join(df1)

    return df


def get_rolling_mean(values, window):
    """Return rolling mean of given values, using specified window size."""
    return pd.rolling_mean(values, window=window)


def get_rolling_std(values, window):
    """Return rolling standard deviation of given values, using specified window size."""
    return pd.rolling_std(values, window=window)


def get_bollinger_bands(rm, rstd):
    """Return upper and lower Bollinger Bands."""
    lower_band = rm - (2 * rstd)
    upper_band = rm + (2 * rstd)

    return upper_band, lower_band

def plot_selected(df, columns, start_index, end_index):

    selected_df = df[columns].ix[start_index:end_index]

    "Normalize Stock data for plotting(make everything start at 1)"
    selected_df = selected_df / selected_df.ix[0,:]

    """Plot the desired columns over index values in the given range."""
    plot_data(selected_df,title="Stock Prices")

def plot_data(df, title="Stock prices"):
    """Plot stock prices with a custom title and meaningful axis labels."""
    ax = df.plot(title=title, fontsize=12)
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    plt.show()


def plot_bollinger_bands(df):
    """Plot Bollinger bands graph"""

    rolling_mean = get_rolling_mean(df["SPY"],window=20)
    rolling_std = get_rolling_std(df["SPY"],window=20)
    upper_band, lower_band = get_bollinger_bands(rolling_mean, rolling_std)



    # Plot raw  values, rolling mean and Bollinger Bands
    ax = df['SPY'].plot(title="Bollinger Bands", label='SPY')
    rolling_mean.plot(label='Rolling mean', ax=ax)
    upper_band.plot(label='upper band', ax=ax)
    lower_band.plot(label='lower band', ax=ax)

    # Add axis labels and legend
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.legend(loc='upper left')
    plt.show()


def test_run():
    # Define a date range
    dates = pd.date_range('2010-01-01', '2010-12-31')

    # Choose stock symbols to read
    symbols = ['GOOGL', 'IBM', 'GLD']  # SPY will be added in get_data()

    # Get stock data
    df = get_data(symbols, dates)

    # Plot Bollinger Graph
    plot_bollinger_bands(df)

    # Slice and plot
    # plot_selected(df, ['SPY', 'IBM'], '2010-03-01', '2010-04-01')



if __name__ == "__main__":
    test_run()




