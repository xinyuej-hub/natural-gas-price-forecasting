import pandas as pd
import Nat_Gas_Forecast as NGP


def price_gas_storage_contract(
    injection_dates,
    withdrawal_dates,
    injection_volumes,
    withdrawal_volumes,
    max_storage_volume,
    injection_rate,
    withdrawal_rate,
    storage_cost_per_month,
    injection_cost_per_unit=0.0,
    withdrawal_cost_per_unit=0.0
):
    """
    Price a gas storage contract using estimated gas prices from
    Nat_Gas_Forecast.py.

    Parameters
    ----------
    injection_dates : list of str or datetime
        Dates when gas is injected into storage.
    withdrawal_dates : list of str or datetime
        Dates when gas is withdrawn from storage.
    injection_volumes : list of float
        Volumes injected on each injection date.
    withdrawal_volumes : list of float
        Volumes withdrawn on each withdrawal date.
    max_storage_volume : float
        Maximum storage capacity.
    injection_rate : float
        Maximum injection volume allowed per date.
    withdrawal_rate : float
        Maximum withdrawal volume allowed per date.
    storage_cost_per_month : float
        Fixed monthly storage cost.
    injection_cost_per_unit : float, optional
        Cost per unit of injected gas.
    withdrawal_cost_per_unit : float, optional
        Cost per unit of withdrawn gas.

    Returns
    -------
    dict
        A dictionary containing contract value and cost breakdown.
    """

    if len(injection_dates) != len(injection_volumes):
        raise ValueError("injection_dates and injection_volumes must have the same length.")

    if len(withdrawal_dates) != len(withdrawal_volumes):
        raise ValueError("withdrawal_dates and withdrawal_volumes must have the same length.")

    injection_df = pd.DataFrame({
        "date": pd.to_datetime(injection_dates),
        "type": "inject",
        "volume": injection_volumes
    })

    withdrawal_df = pd.DataFrame({
        "date": pd.to_datetime(withdrawal_dates),
        "type": "withdraw",
        "volume": withdrawal_volumes
    })

    events = pd.concat([injection_df, withdrawal_df], ignore_index=True)
    events = events.sort_values("date").reset_index(drop=True)

    inventory = 0.0
    purchase_cost = 0.0
    sales_revenue = 0.0
    operating_cost = 0.0
    inventory_history = []

    for _, row in events.iterrows():
        event_date = row["date"]
        event_type = row["type"]
        volume = float(row["volume"])

        if volume < 0:
            raise ValueError("Volumes must be non-negative.")

        price = NGP.estimate_price(event_date)

        if event_type == "inject":
            if volume > injection_rate:
                raise ValueError(
                    f"Injection volume {volume} exceeds injection rate limit "
                    f"{injection_rate} on {event_date.date()}."
                )

            if inventory + volume > max_storage_volume:
                raise ValueError(
                    f"Storage capacity exceeded on {event_date.date()}. "
                    f"Inventory would become {inventory + volume}, above max {max_storage_volume}."
                )

            purchase_cost += price * volume
            operating_cost += injection_cost_per_unit * volume
            inventory += volume

        elif event_type == "withdraw":
            if volume > withdrawal_rate:
                raise ValueError(
                    f"Withdrawal volume {volume} exceeds withdrawal rate limit "
                    f"{withdrawal_rate} on {event_date.date()}."
                )

            if volume > inventory:
                raise ValueError(
                    f"Not enough inventory to withdraw {volume} on {event_date.date()}. "
                    f"Current inventory is {inventory}."
                )

            sales_revenue += price * volume
            operating_cost += withdrawal_cost_per_unit * volume
            inventory -= volume

        inventory_history.append({
            "date": event_date,
            "type": event_type,
            "volume": volume,
            "price": price,
            "inventory_after_event": inventory
        })

    if len(events) > 0:
        first_event_date = events["date"].min()
        last_event_date = events["date"].max()

        months_in_storage = (
            (last_event_date.year - first_event_date.year) * 12
            + (last_event_date.month - first_event_date.month)
            + 1
        )
    else:
        months_in_storage = 0

    storage_cost = months_in_storage * storage_cost_per_month
    contract_value = sales_revenue - purchase_cost - storage_cost - operating_cost

    return {
        "contract_value": contract_value,
        "sales_revenue": sales_revenue,
        "purchase_cost": purchase_cost,
        "storage_cost": storage_cost,
        "operating_cost": operating_cost,
        "ending_inventory": inventory,
        "inventory_history": pd.DataFrame(inventory_history)
    }


if __name__ == "__main__":
    result = price_gas_storage_contract(
        injection_dates=["2024-04-15", "2024-06-15", "2024-09-16"],
        withdrawal_dates=["2024-11-15", "2025-01-15"],
        injection_volumes=[400000, 300000, 100000],
        withdrawal_volumes=[300000, 400000],
        max_storage_volume=800000,
        injection_rate=500000,
        withdrawal_rate=500000,
        storage_cost_per_month=80000,
        injection_cost_per_unit=0.02,
        withdrawal_cost_per_unit=0.02
    )

    print("Contract Value: ${:,.2f}".format(result["contract_value"]))
    print("Sales Revenue: ${:,.2f}".format(result["sales_revenue"]))
    print("Purchase Cost: ${:,.2f}".format(result["purchase_cost"]))
    print("Storage Cost: ${:,.2f}".format(result["storage_cost"]))
    print("Operating Cost: ${:,.2f}".format(result["operating_cost"]))
    print("Ending Inventory: {:,.2f}".format(result["ending_inventory"]))

    print("\nInventory History:")
    print(result["inventory_history"])