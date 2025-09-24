# Import the necessary libraries
import yfinance as yf
import pandas as pd
import numpy as np
import time

def fetch_data(ticker_symbol, start_date, end_date):
    """
    Fetches historical stock data from Yahoo Finance.
    - ticker_symbol: The stock symbol we want data for (e.g., 'AAPL' for Apple).
    - start_date: The beginning date for the data in 'YYYY-MM-DD' format.
    - end_date: The ending date for the data.
    Returns a pandas DataFrame with the stock data.
    """
    print(f"Fetching data for {ticker_symbol} from {start_date} to {end_date}...")
    # yf.download() is the key function from the yfinance library.
    # It returns the data in a convenient pandas DataFrame structure.
    data = yf.download(ticker_symbol, start=start_date, end=end_date)
    print("Data fetched successfully!")
    return data

def calculate_indicators(data):
    """
    Calculates financial indicators on the stock data.
    - data: A pandas DataFrame containing the stock data.
    Returns the DataFrame with the new indicator columns added.
    """
    print("Calculating financial indicators...")
    
    # --- Calculate Simple Moving Average (SMA) ---
    # A 50-day SMA is the average of the closing price over the last 50 days.
    # .rolling(window=50) creates a 50-day sliding window over the 'Close' price column.
    # .mean() then calculates the average for each window. This is very efficient!
    data['SMA_50'] = data['Close'].rolling(window=50).mean()

    # --- Calculate Exponential Moving Average (EMA) ---
    # EMA gives more weight to recent prices.
    # .ewm() is pandas' function for exponential calculations.
    # com=21 is a way to specify the smoothing factor, roughly equivalent to a 22-day EMA.
    data['EMA_21'] = data['Close'].ewm(com=21).mean()

    # --- Calculate Volatility (Standard Deviation) ---
    # We measure volatility as the standard deviation of daily returns over a period (e.g., 50 days).
    # First, calculate the daily returns as the percentage change in the closing price.
    daily_returns = data['Close'].pct_change()
    # Then, calculate the rolling standard deviation of these returns.
    data['Volatility_50'] = daily_returns.rolling(window=50).std()

    print("Indicators calculated.")
    return data

def analyze_performance(data):
    """
    Performs a final analysis and prints the results.
    - data: The DataFrame with all data and indicators.
    """
    print("\n--- Analysis Complete ---")
    # .dropna() removes any rows with missing values (like the first 49 days for the 50-day SMA).
    # We do this so we only look at rows where all our calculations are valid.
    final_data = data.dropna()
    
    # Display the last 5 rows of our completed DataFrame to see the results.
    print("Displaying the last 5 days of data with indicators:")
    print(final_data.tail(5))


# --- MAIN EXECUTION BLOCK ---
# This is where the script starts running.
# The `if __name__ == "__main__":` line is a standard Python convention.
# It means "run the code below only when this file is executed directly."
if __name__ == "__main__":
    
    # Define the parameters for our analysis.
    # You can change these to analyze different stocks or time periods.
    ticker = 'NVDA'  # NVIDIA Corporation
    start = '2020-01-01'
    end = '2025-01-01'
    
    # --- Performance Benchmarking ---
    # Record the time before we start the main process.
    start_time = time.time()
    
    # Step 1: Fetch the data using our function.
    stock_data = fetch_data(ticker, start, end)
    
    # Check if data was successfully downloaded. If the DataFrame is empty, something went wrong.
    if not stock_data.empty:
        # Step 2: Calculate the indicators using our function.
        stock_data_with_indicators = calculate_indicators(stock_data)
        
        # Step 3: Run the final analysis and display results.
        analyze_performance(stock_data_with_indicators)
    else:
        print(f"Could not download data for {ticker}. Please check the symbol and date range.")

    # Record the time after the process is finished.
    end_time = time.time()
    
    # Calculate the total duration by subtracting the start time from the end time.
    duration = end_time - start_time
    
    # Print the performance result.
    # The ':.2f' formats the number to show only two decimal places.
    print(f"\nTotal execution time: {duration:.2f} seconds.")