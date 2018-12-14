"""Utility functions"""

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


def test_run():
    # Define a date range
    dates = pd.date_range('2010-01-22', '2010-01-26')

    # Choose stock symbols to read
    symbols = ['GOOGL', 'IBM', 'GLD']

    # Get stock data
    df = get_data(symbols, dates)
    print(df)


if __name__ == "__main__":
    test_run()
