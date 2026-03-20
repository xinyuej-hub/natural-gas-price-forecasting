# Natural Gas Price Forecasting

This project estimates natural gas prices for user-input dates based on historical monthly price data.

## Overview
The script:
- loads and prepares monthly natural gas price data,
- visualizes the time series,
- models trend and seasonality using Holt-Winters Exponential Smoothing,
- forecasts prices for the next 12 months,
- and estimates a price for any valid input date.

## Method
For dates within the historical and forecast range, the script uses time-based interpolation between monthly observed or forecasted values.  
For future dates up to one year beyond the dataset, prices are generated using a Holt-Winters time series model with additive trend and additive seasonality.

## Features
- historical price estimation
- one-year forward forecasting
- repeated user input until `q` is entered to quit

## How to Run
Place the dataset file(Nat_Gas.csv) in the same folder as the script, then run:

```bash
python Nat_Gas_Forecast.py
