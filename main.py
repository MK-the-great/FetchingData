import requests
import pandas as pd
import matplotlib.pyplot as plt

def get_api_key(filename='configure.txt'):
    with open(filename, 'r') as file:
        return file.readline().strip()

def get_data(stock_ticker):
    ALPHA_KEY = get_api_key()
    API_URL = ("https://www.alphavantage.co/query?function=TIME_"
               "SERIES_DAILY&symbol=" + stock_ticker + "&apikey=" + ALPHA_KEY)
    URL = requests.get(API_URL, verify=0)
    my_info = URL.json()
    return my_info

def access_stock(my_data):
    my_dataFrame = pd.DataFrame(my_data["Time Series (Daily)"])
    my_df = my_dataFrame.transpose()
    my_df = my_df.head()
    my_df.index = pd.to_datetime(my_df.index)
    return my_df


def plot_stock(my_df, stock_ticker):
    for column in ["1. open", '2. high', '3. low', '4. close', '5. volume']:
        plt.plot(my_df.index, my_df[column], label=column, linewidth=2)
    plt.title("Stocks for " + stock_ticker)
    plt.xlabel("Dates")
    plt.ylabel("Stock Prices")
    plt.legend()
    plt.show()

continue_search = True
while continue_search:
    try:
        stock_ticker = input("Enter a stock ticker: ")
        stock_data = get_data(stock_ticker)
        df = access_stock(stock_data)

        plot_stock(df, stock_ticker)

        user_decision = input("Do you want to check another stock? Enter 'Y' for yes and 'N' for no: ").lower()
        if user_decision == 'n':
            continue_search = False
        elif user_decision != 'y':
            print("Invalid input")
            continue_search = False

    except requests.exceptions.Timeout:
        print("The request timed out")
    except requests.exceptions.TooManyRedirects:
        print("Too many redirects.")
    except requests.exceptions.RequestException as error:
        print(f"An error occurred while getting data: {error}")
    except requests.exceptions.ConnectionError:
        print("Failed to establish a connection.")
    except KeyError:
        print("Invalid stock ticker")
    except ValueError as e:
        print(f"An error occurred: {e}")
