# Natural Gas Pricing and Storage Contract Valuation

A Python project for estimating natural gas prices and valuing a gas storage contract using time-series forecasting and cash-flow logic.

## Overview

This project is organized into two Python modules:

- `Nat_Gas_Forecast.py`  
  This is the first part of the project. It estimates natural gas prices for specific dates using historical monthly data, Holt-Winters forecasting, and time-based interpolation.

- `Pricing.py`  
  This is the second part of the project. It imports the forecasting module as `NGP` and uses the estimated gas prices to value a gas storage contract.

## What `Pricing.py` Does

`Pricing.py` prices a gas storage contract by combining:

- injection dates
- withdrawal dates
- injection and withdrawal volumes
- estimated gas prices on those dates
- storage capacity limits
- injection and withdrawal rate limits
- storage and operating costs

The contract value is calculated as:

**Contract Value = Sales Revenue - Purchase Cost - Storage Cost - Operating Cost**

## Files

- `Nat_Gas_Forecast.py` — price forecasting module
- `Pricing.py` — gas storage contract valuation module
Note: The dataset file is not included in this repository.

## Method

### Part 1: Price Estimation
The forecasting script:
- loads monthly natural gas price data,
- models trend and seasonality using Holt-Winters Exponential Smoothing,
- forecasts prices for the next 12 months,
- and estimates prices for user-input dates.

### Part 2: Contract Valuation
The pricing script:
- imports `Nat_Gas_Forecast.py` as `NGP`,
- calls `NGP.estimate_price(date)` to estimate gas prices,
- calculates purchase cost for injections,
- calculates sales revenue for withdrawals,
- deducts storage and operating costs,
- and checks inventory and storage constraints.

## How to Run

### Run Part 1: Forecasting
Make sure the dataset file (Nat_Gas.csv) is in the same folder as `Nat_Gas_Forecast.py`, then run:

```bash
python Nat_Gas_Forecast.py
```

### Run Part 2: Pricing
```bash
python Pricing.py


