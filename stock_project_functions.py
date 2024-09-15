import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

def plot_hue_column(df,column='Action',plot_one=False,plot_three=False):
    
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
    # Convert all dates to UTC, then remove timezone information
    df['Date'] = pd.to_datetime(df['Date'], utc=True).dt.tz_localize(None)
    
    # Sort the dataframe
    df = df.sort_values(by='Date')

    if plot_three:
        for ticker in ['XLB','XLK','XLY']:
            data = df[df['Ticker'] == ticker]
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.scatterplot(x='Date', y='Close', data=data, hue=column, ax=ax)
            ax.set_title(f'Close Price for {ticker}\nTarget Label: {column}')
            ax.set_xlabel('Date')
            ax.set_ylabel('Close Price')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()
        return None
    
    # Now plot for each ticker
    for ticker in sector_stocks.keys():
        data = df[df['Ticker'] == ticker]
        if not data.empty:  # Check if there's data for this ticker
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.scatterplot(x='Date', y='Close', data=data, hue=column, ax=ax)
            ax.set_title(f'Close Price for {ticker}\nTarget Label: {column}')
            ax.set_xlabel('Date')
            ax.set_ylabel('Close Price')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()
        if plot_one:
            break
def get_train_test(joined,ticker_dummies=True):

    if ticker_dummies:
        joined=pd.get_dummies(joined,columns=['Ticker'])

        features = [col for col in joined.columns if 'lag' in col] + ['Month']+[col for col in joined if 'Ticker' in col]
    else:
        features = [col for col in joined.columns if 'lag' in col] + ['Month']

    joined.sort_values(by='Date', inplace=True)
    joined=joined.dropna(subset=features)
    # Define the split point (e.g., 70% for training)
    split_point = int(len(joined) * 0.7)

    # Split the data into training and testing sets
    train = joined.iloc[:split_point]
    test = joined.iloc[split_point:]
    return train, test,features

def ge_best_model_():
    
