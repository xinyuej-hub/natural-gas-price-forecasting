import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing

# =========================
# 1. Load and prepare data
# =========================

file_path = "Nat_Gas.csv"

df = pd.read_csv(file_path)

# Convert columns
df["Dates"] = pd.to_datetime(df["Dates"])
df["Prices"] = pd.to_numeric(df["Prices"])

# Sort by date just in case
df = df.sort_values("Dates").reset_index(drop=True)

# Set index
df.set_index("Dates", inplace=True)

# =========================
# 2. Visualize the data
# =========================

plt.figure(figsize=(12, 6))
plt.plot(df.index, df["Prices"], marker="o")
plt.title("Monthly Natural Gas Prices")
plt.xlabel("Date")
plt.ylabel("Price")
plt.grid(True)
plt.tight_layout()
plt.show()

# =========================
# 3. Fit forecasting model
# =========================
# Monthly data with yearly seasonality -> seasonal_periods = 12

model = ExponentialSmoothing(
    df["Prices"],
    trend="add",
    seasonal="add",
    seasonal_periods=12
).fit()

# Forecast next 12 months
forecast_horizon = 12
future_forecast = model.forecast(forecast_horizon)

# Build future monthly date index from the month-end after last data point
last_date = df.index.max()
future_dates = pd.date_range(
    start=last_date + pd.offsets.MonthEnd(1),
    periods=forecast_horizon,
    freq="M"
)

forecast_series = pd.Series(future_forecast.values, index=future_dates)

# Combine historical + forecast monthly points
full_series = pd.concat([df["Prices"], forecast_series])

# =========================
# 4. Function to estimate price for any date
# =========================

def estimate_price(input_date):
    """
    Estimate the natural gas price for any date in the historical range
    and up to one year beyond the last available date.

    Parameters:
        input_date (str or datetime): date to estimate, e.g. '2023-06-15'

    Returns:
        float: estimated price
    """
    input_date = pd.to_datetime(input_date)

    first_date = df.index.min()
    last_hist_date = df.index.max()
    last_forecast_date = forecast_series.index.max()

    if input_date < first_date:
        raise ValueError(
            f"Date is before available historical data. "
            f"Choose a date on or after {first_date.date()}."
        )

    if input_date > last_forecast_date:
        raise ValueError(
            f"Date is beyond the 1-year forecast horizon. "
            f"Choose a date on or before {last_forecast_date.date()}."
        )

    # Exact monthly point exists
    if input_date in full_series.index:
        return float(full_series.loc[input_date])

    # Interpolate between nearest known monthly points
    combined = full_series.copy()

    # Add the requested date with NaN, then sort and interpolate by time
    combined.loc[input_date] = np.nan
    combined = combined.sort_index()
    combined = combined.interpolate(method="time")

    return float(combined.loc[input_date])

# =========================
# 5. Take user input and estimate
# =========================

user_date = input("Enter a date (YYYY-MM-DD) or 'q' to quit: ").strip()

while user_date.lower() != "q":
    try:
        estimated_price = estimate_price(user_date)
        print(f"Estimated price for {user_date}: {estimated_price:.2f}")
    except Exception as e:
        print("Error:", e)

    user_date = input("Enter a date (YYYY-MM-DD) or 'q' to quit: ").strip()

print("Exiting program.")

# =========================
# 6. Plot historical data + forecast
# =========================

plt.figure(figsize=(12, 6))
plt.plot(df.index, df["Prices"], marker="o", label="Historical Prices")
plt.plot(
    forecast_series.index,
    forecast_series.values,
    marker="o",
    linestyle="--",
    label="Forecast (Next 12 Months)"
)
plt.title("Natural Gas Prices: Historical Data and 12-Month Forecast")
plt.xlabel("Date")
plt.ylabel("Price")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()