import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime, date
import pandas_market_calendars as mcal
def main():
    # Define the list of sector ETFs and VOO
    sector_etfs = ['XLY', 'XLP', 'XLE', 'XLF', 'XLV', 'XLI', 'XLB', 'XLRE', 'XLK', 'XLC', 'XLU']
    benchmark = 'VOO'

    # Ask the user to input the start and end dates
    #start_date_str = input("Enter the start date (YYYY-MM-DD): ")
    #end_date_str = input("Enter the end date (YYYY-MM-DD): ")

    # Convert string dates to datetime objects`
    start_date = date(2023,6,1)
    end_date = date(2023,6,11)
    

    # Get NYSE calendar
    nyse = mcal.get_calendar('NYSE')
    trading_days = nyse.schedule(start_date=start_date, end_date=end_date)
    trading_days = trading_days.index
    X=relativeStrength(start_date,end_date,metric='Corr')
    print(X.top_stocks)




class relativeStrength:
    def __init__(self,start_date, end_date,metric='Slope'):
        self.metric=metric
        self.start_date=start_date
        self.end_date=end_date
        # Define the list of sector ETFs and VOO
        self.sector_etfs = ['XLY', 'XLP', 'XLE', 'XLF', 'XLV', 'XLI', 'XLB', 'XLRE', 'XLK', 'XLC', 'XLU']
        self.benchmark = 'VOO'
        # Get NYSE calendar
        self.nyse = mcal.get_calendar('NYSE')
        self.trading_days = self.nyse.schedule(start_date=start_date, end_date=end_date)
        self.trading_days = self.trading_days.index
        self.top_3_etfs=self.getResults()
        self.top_stocks=self.getTopStocks()


# Calculate slopes for all sector ETFs
    @property
    def actual_start_date(self):
        return self.trading_days[0].date()

    @property
    def actual_end_date(self):
        return self.trading_days[-1].date()

    def getResults(self):
        results = []
        for etf in self.sector_etfs:
            metric = self.calculate_relative_etf_strength(etf, self.benchmark)
            results.append((etf, metric))
        # Sort results by slope in descending order and get top 3
        top_3_etfs = sorted(results, key=lambda x: x[1], reverse=True)[:3]
        return top_3_etfs
    def __str__(self):
# Print the top 3 sector ETFs
        print_string=""
        for etf, slope in self.top_3_etfs:
            print_string+=f"{etf}: Slope = {slope:.6f}"
        return print_string
        # Function to calculate relative strength and regression slope
    def calculate_relative_etf_strength(self, etf, benchmark):
        # Download data
        check=True
        try:
            etf_data = yf.download(etf, start=self.start_date, end=self.end_date)['Adj Close']
            benchmark_data = yf.download(benchmark, start=self.start_date, end=self.end_date)['Adj Close']
        except:
            print(etf)
        
        # Filter for trading days
        etf_data = etf_data[etf_data.index.isin(self.trading_days)]
        benchmark_data = benchmark_data[benchmark_data.index.isin(self.trading_days)]
        
        # Calculate relative strength
        relative_strength = etf_data / benchmark_data

        # Prepare data for regression

        X = np.arange(len(relative_strength)).reshape(-1, 1)
        y = relative_strength.values

        if check:
            print(relative_strength)
            pd.DataFrame({'X':list(X),'y':list(y)}).to_csv('CHECK.csv')
            check=False

        if self.metric=='Corr':
            # Calculate correlation coefficient
            correlation = np.corrcoef(X.flatten(), y)[0, 1]
            return correlation
        if self.metric=='Slope':
        # Perform linear regression
            try:
                model = LinearRegression()
                model.fit(X, y)
            except:
                print(etf)
            return model.coef_[0]
        else:
            try:
                model = LinearRegression()
                model.fit(X, y)
                correlation = np.corrcoef(X.flatten(), y)[0, 1]
                product=model.coef_[0]*abs(correlation)
            except:
                product=-float('inf')
                print(etf)
            return product



# Function to get approximate constituents of an ETF
    def get_etf_constituents(self, etf):
        sector_stocks = {
            'XLY': ['AMZN', 'TSLA', 'HD', 'MCD', 'NKE', 'BKNG', 'LOW', 'TJX', 'SBUX', 'CMG'],
            'XLP': ['PG', 'PEP', 'KO', 'COST', 'WMT', 'PM', 'MDLZ', 'CL', 'MO', 'TGT'],
            'XLE': ['XOM', 'CVX', 'COP', 'SLB', 'EOG', 'MPC', 'PSX', 'WMB', 'VLO', 'OKE'],
            'XLF': ['BRK-B', 'JPM', 'BAC', 'WFC', 'GS', 'V', 'MA', 'BAC', 'WFC', 'GS', 'SPGI', 'AXP', 'PGR'],
            'XLV': ['UNH', 'JNJ', 'LLY', 'PFE', 'ABT', 'MRK', 'ABBV', 'TMO', 'AMGN', 'DHR', 'PFE'],
            'XLI': ['UNP', 'HON', 'UPS', 'CAT', 'GE', 'UBER', 'HON', 'RTX', 'ETN', 'BA', 'UPS', 'LMT'],
            'XLB': ['LIN', 'FCX', 'APD', 'ECL', 'NEM', 'SHW', 'NUE', 'CTVA', 'DOW', 'DD'],
            'XLRE': ['PLD', 'AMT', 'CCI', 'EQIX', 'PSA', 'WELL', 'SPG', 'DLR', 'O', 'EXR'],
            'XLK': ['AAPL', 'MSFT', 'NVDA', 'AVGO', 'AMD', 'CRM', 'ADBE', 'ORCL', 'QCOM', 'AMAT'],
            'XLC': ['META', 'GOOGL', 'NFLX', 'CMCSA', 'T', 'VZ', 'EA', 'TMUS', 'DIS'],
            'XLU': ['NEE', 'DUK', 'SO', 'D', 'AEP', 'CEG', 'SRE', 'PCG', 'PEG', 'EXC']
        }
        return sector_stocks.get(etf, [])

# Function to calculate relative strength and regression slope for stocks within an ETF
    def calculate_stock_relative_strength(self, stock, etf):
        # Download data
        stock_data = yf.download(stock, start=self.start_date, end=self.end_date)['Adj Close']
        etf_data = yf.download(etf, start=self.start_date, end=self.end_date)['Adj Close']
        
        # Filter for trading days
        stock_data = stock_data[stock_data.index.isin(self.trading_days)]
        etf_data = etf_data[etf_data.index.isin(self.trading_days)]
        
        # Calculate relative strength
        relative_strength = stock_data / etf_data

        try:
        # Prepare data for regression
            X = np.arange(len(relative_strength)).reshape(-1, 1)
            y = relative_strength.values
        except:
            print(stock,etf)

        if self.metric=='Corr':
            # Calculate correlation coefficient
            correlation = np.corrcoef(X.flatten(), y)[0, 1]
            return correlation
        if self.metric=='Slope':
        # Perform linear regression
            model = LinearRegression()
            model.fit(X, y)
            return model.coef_[0]
        else:
            try:
                model = LinearRegression()
                model.fit(X, y)
                correlation = np.corrcoef(X.flatten(), y)[0, 1]
                product=model.coef_[0]*abs(correlation)
            except:
                product=-float('inf')
                print(etf)
            return product

    def getTopStocks(self):
    # For each of the top 3 sector ETFs, find the top 3 stocks by relative strength slope
        final_stocks={}
        is_positive={}
        for etf, _ in self.top_3_etfs:
            print(f"\nAnalyzing stocks for {etf}:")
            # Get the approximate constituents of the ETF
            constituents = self.get_etf_constituents(etf)
            print(f"Constituents: {constituents}")
            final_stocks[etf]=[]
            stock_results = []

            for stock in constituents:
                try:
                    Metric= self.calculate_stock_relative_strength(stock, etf)
                    if Metric>0:
                        metric_sign=True
                    else:
                        metric_sign=False
                    stock_results.append((stock, Metric,metric_sign))
                    print(f"Calculated {self.metric} for {stock}: {Metric:.6f}")
                except Exception as e:
                    print(f"Error calculating slope for {stock} in {etf}: {str(e)}")
            
            if stock_results:
                # Sort results by slope in descending order and get top 3
                top_3_stocks = sorted(stock_results, key=lambda x: x[1], reverse=True)[:3]
                
                # Print the top 3 stocks for each sector ETF
                print(f"\nTop 3 stocks in {etf} by relative strength slope:")
                for stock, metric,metric_sign in top_3_stocks:
                    print(f"{stock}: {self.metric} = {metric:.6f}")
                    final_stocks[etf].append((stock,metric_sign))

            else:
                print(f"No valid results for stocks in {etf}")
        return final_stocks
if __name__=='__main__':
    main()
