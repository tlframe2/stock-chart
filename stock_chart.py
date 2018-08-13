"""
Produces graph of company’s stock’s closing prices, 20-day moving average of closing prices, and Bollinger bands 

to show price trends and volatility between specified dates.
"""
from datetime import datetime
import matplotlib.pyplot as plt
import quandl

class Chart(object):
    """
    Creates DataFrame consisting of stock's financial data between specified dates obtained using Quandl, 
    then graphs it using Matplotlib.

    Attributes:
        start_date (DateTime): starting date for financial data
        end_date (DateTime): ending date for financial data
        ticker (string): company's stock ticker
        stock_data (DataFrame): stock's financial data
    """

    def __init__(self, start_date, end_date, ticker):
        self.start_date = Chart.convert_date(start_date)
        self.end_date = Chart.convert_date(end_date)
        self.ticker = ticker
        self.stock_data = self.create_dataframe()

    @staticmethod
    def convert_date(date):
        """
        Converts date from string to DateTime object.

        Parameters:
            date(string): user supplied date in form MM/DD/YYYY

        Returns:
            DateTime object of date provided by user
        """

        # Splits date string into separate elements using / as delimiter and assigns them to appropriate variables using assignment unpacking
        month, day, year = date.split('/')

        # Creates DateTime object
        date_obj = datetime(int(year), int(month), int(day))

        return date_obj

    def create_dataframe(self):
        """
        Uses Quandl to retrieve stock's financial data. Calculates 20 day mean of closing prices as well as 
		
        2 standard deviations above and below those prices (Bollinger Bands).
        """

        try:
            # Creates dataframe using user inputs and stock data provided by Quandl
            data = quandl.get_table('WIKI/PRICES', ticker=self.ticker, qopts ={'columns': ['date', 'close']}, 
								    date ={'gte': self.start_date, 'lte': self.end_date})
            stock_df = data.set_index('date')
        except:
            # If dataframe cannot be created (usually because of firewall settings), prints error message and proceeds to end of program    
            print("ERROR: COULD NOT CREATE DATAFRAME!")
        else:
            # Adds column to stock df for 20 day mean of closing prices
            stock_df['close: 20 day mean'] = stock_df['close'].rolling(20).mean()

            # Adds column for 20 day mean of closing prices plus two standard deviations
            stock_df['upper'] = stock_df['close: 20 day mean'] + 2 * (stock_df['close'].rolling(20).std())

            # Adds column for 20 day mean of closing prices minus two standard deviations
            stock_df['lower'] = stock_df['close: 20 day mean'] - 2 * (stock_df['close'].rolling(20).std())

            return stock_df

    def plot_graph(self):
        """ Creates graph using Matplotlib. """

        # Creates graph of dates vs prices with the closing price, 20 day mean closing price, upper, and lower bands
        self.stock_data[['close','close: 20 day mean','upper','lower']].plot(figsize=(16,6))

        # Applies y-label for clarity
        plt.ylabel('Price per Share')

        # Applies stock ticker symbol as title for graph
        plt.title(self.ticker)

        # Necessary method to show graph
        plt.show()

def main():
    """ Main function. """

    # Prompts user for start and end dates for range
    start = input("Enter start date in format Month/Day/Year separated by forward slashes (ex. July 3rd, 2014 = 7/3/2014)\n")
    end = input("Enter end date in format Month/Day/Year separated by forward slashes (ex. July 3rd, 2014 = 7/3/2014)\n")

    # Prompts user for stock ticker
    ticker = input("Enter stock ticker (ex. Facebook = FB)\n").upper()

    # Instantiates Chart object
    stock_chart = Chart(start, end, ticker)

    # Creates graph
    stock_chart.plot_graph()

if __name__ == '__main__':

    # API Key needed to retrieve data from Quandl
    quandl.ApiConfig.api_key = 'INSERT_YOUR_KEY_HERE'

    # Controls whether or not program runs
    RUNNING = True

    while RUNNING:

        # Executes main function
        main()

        option = ''

        # Asks user if they would like to create another graph; continues asking unless user enters y (yes) or n (no)       
        while option.lower() != 'y' and option.lower() != 'n':
            option = input("Generate another graph (y/n)? ")

        # Ends program if user enters n (no)
        if option.lower() == "n":
            RUNNING = False