"""

Uses the polygon io API to see stock prices of a given stock over a given period of time

"""


import requests
import matplotlib.pylab as plt
import matplotlib.dates as mdates
from datetime import datetime
import os

token_folder = r"PATHTOTOKENFOLDER"
token_file = r"polygon_io_token.txt"

with open(os.path.join(token_folder, token_file), "r") as token:
    API_KEY = token.read()

print(API_KEY)

stock = input("Stock: ")

timespan_unit = input("""
Timespan Unit - 
(second, minute, hour, day, week, month, quarter, year): """)

numOf = int(input("Number of: "))

fromDate = input("Date From (YYYY-MM-DD): ")
toDate = input("Date To (YYYY-MM-DD): ")

r = requests.get(f"https://api.polygon.io/v2/aggs/ticker/{stock}/range/{numOf}/{timespan_unit}/{fromDate}/{toDate}?adjusted=true&sort=asc&apiKey={API_KEY}")

print(r.status_code)
if r.status_code == 200:
    print("Connection Verified")
    data = r.json()

    # Dictionary to store date: close price
    date_close_dict = {}

    # Accessing values in results
    for result in data['results']:
        timestamp = result['t']
        close_price = result['c']

        # Convert timestamp to date string
        date_str = datetime.utcfromtimestamp(timestamp / 1000).strftime('%Y-%m-%d')

        # Store in dictionary
        date_close_dict[date_str] = close_price

    # Print the dictionary
    print(date_close_dict)

    dates = list(date_close_dict.keys())
    close_prices = list(date_close_dict.values())

    # Convert date strings to datetime objects for plotting
    dates = [datetime.strptime(date, '%Y-%m-%d') for date in dates]

    # Plotting
    fig, ax = plt.subplots()
    ax.plot(dates, close_prices, label='Close Price')

    # Formatting the x-axis to reduce labels
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.xticks(rotation=45)

    # Additional formatting
    plt.xlabel('Date')
    plt.ylabel('Close Price USD')
    plt.title(f'{stock} Close Prices Over Time')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

else:
    print("Issue Connecting")
