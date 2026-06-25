def calculate_kpis(df):

    total_sales = int(df["Sales Count"].sum())

    total_redemption = int(
        df["Redemption Count"].sum()
    )

    net_movement = (
        total_sales -
        total_redemption
    )

    peak_hour = (
        df.groupby("Hour")["Sales Count"]
        .sum()
        .idxmax()
    )

    avg_sales = round(
        df["Sales Count"].mean(),
        2
    )

    return {

        "total_sales": total_sales,

        "total_redemption": total_redemption,

        "net_movement": net_movement,

        "peak_hour": peak_hour,

        "avg_sales": avg_sales
    }