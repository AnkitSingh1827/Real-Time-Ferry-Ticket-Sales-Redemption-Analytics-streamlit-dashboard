import pandas as pd
import numpy as np

from .data_cleaning import clean_data
from .feature_engineering import add_features
from .kpi_calculator import calculate_kpis

DAY_ORDER = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]

MONTH_ORDER = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]

SEASONS = ["Winter", "Spring", "Summer", "Fall"]


def prepare_data(df: pd.DataFrame) -> pd.DataFrame:
    df = clean_data(df)
    df = add_features(df)
    df = df.sort_values("Timestamp").reset_index(drop=True)
    return df


def build_global_filters(df: pd.DataFrame, title: str = "Global Filters") -> dict:
    import streamlit as st

    st.sidebar.header(title)

    years = df["Year"].dropna().astype(int).unique().tolist()
    years.sort()

    year_options = ["All"] + [str(year) for year in years]
    selected_year = st.sidebar.selectbox("Year", year_options, index=0)

    month_options = ["All"] + [month for month in MONTH_ORDER if month in df["Month"].unique()]
    selected_month = st.sidebar.selectbox("Month", month_options, index=0)

    season_options = ["All"] + SEASONS
    selected_season = st.sidebar.selectbox("Season", season_options, index=0)

    weekend_options = ["All", "Weekday", "Weekend"]
    selected_weekend = st.sidebar.selectbox("Weekday/Weekend", weekend_options, index=0)

    st.sidebar.markdown("---")
    st.sidebar.markdown("### Toronto Ferry Analytics")
    st.sidebar.write("Real-time and seasonal availability for Toronto Island ferry operations.")

    return {
        "year": selected_year,
        "month": selected_month,
        "season": selected_season,
        "weekend": selected_weekend,
    }


def apply_global_filters(df: pd.DataFrame, filters: dict) -> pd.DataFrame:
    filtered = df.copy()

    if filters.get("year") and filters["year"] != "All":
        filtered = filtered[filtered["Year"] == int(filters["year"])]

    if filters.get("month") and filters["month"] != "All":
        filtered = filtered[filtered["Month"] == filters["month"]]

    if filters.get("season") and filters["season"] != "All":
        filtered = filtered[filtered["Season"] == filters["season"]]

    if filters.get("weekend") and filters["weekend"] != "All":
        filtered = filtered[filtered["Weekend"] == filters["weekend"]]

    return filtered


def latest_metrics(df: pd.DataFrame) -> dict:
    if df.empty:
        return {
            "latest_timestamp": None,
            "latest_sales": 0,
            "latest_redemption": 0,
            "net_movement": 0,
            "last_1h_sales": 0,
            "last_4h_sales": 0,
            "last_24h_sales": 0,
        }

    latest_timestamp = df["Timestamp"].max()
    latest_record = df[df["Timestamp"] == latest_timestamp].iloc[-1]

    last_1h_start = latest_timestamp - pd.Timedelta(hours=1)
    last_4h_start = latest_timestamp - pd.Timedelta(hours=4)
    last_24h_start = latest_timestamp - pd.Timedelta(hours=24)

    return {
        "latest_timestamp": latest_timestamp,
        "latest_sales": int(latest_record["Sales Count"]),
        "latest_redemption": int(latest_record["Redemption Count"]),
        "net_movement": int(latest_record["Sales Count"] - latest_record["Redemption Count"]),
        "last_1h_sales": int(df[df["Timestamp"] > last_1h_start]["Sales Count"].sum()),
        "last_4h_sales": int(df[df["Timestamp"] > last_4h_start]["Sales Count"].sum()),
        "last_24h_sales": int(df[df["Timestamp"] > last_24h_start]["Sales Count"].sum()),
    }


def hourly_aggregate(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(
            columns=["Timestamp", "Sales Count", "Redemption Count"]
        )

    hourly = (
        df.set_index("Timestamp")["Sales Count"]
        .resample("h")
        .sum()
        .to_frame()
        .join(
            df.set_index("Timestamp")["Redemption Count"].resample("h").sum()
        )
        .reset_index()
        .fillna(0)
    )

    return hourly


def rolling_averages(df: pd.DataFrame) -> pd.DataFrame:
    hourly = hourly_aggregate(df)
    hourly["Sales MA 1H"] = hourly["Sales Count"].rolling(window=1, min_periods=1).mean()
    hourly["Sales MA 4H"] = hourly["Sales Count"].rolling(window=4, min_periods=1).mean()
    return hourly


def get_peak_windows(df: pd.DataFrame, top_n: int = 4) -> (pd.DataFrame, pd.DataFrame):
    hourly = (
        df.groupby("Hour")["Sales Count"]
        .sum()
        .reset_index()
    )

    peak_hours = hourly.nlargest(top_n, "Sales Count").copy()
    peak_hours["Window"] = "Peak"

    off_peak_hours = hourly.nsmallest(top_n, "Sales Count").copy()
    off_peak_hours["Window"] = "Off Peak"

    heatmap = (
        df.pivot_table(
            index="Day",
            columns="Hour",
            values="Sales Count",
            aggfunc="sum",
            fill_value=0,
        )
        .reindex(index=DAY_ORDER, fill_value=0)
        .fillna(0)
    )

    summary = pd.concat([peak_hours, off_peak_hours], ignore_index=True)
    summary = summary.sort_values(["Window", "Sales Count"], ascending=[True, False])

    return heatmap, summary


def off_peak_metrics(df: pd.DataFrame) -> dict:
    if df.empty:
        return {
            "peak_utilization_pct": 0.0,
            "off_peak_utilization_pct": 0.0,
            "peak_sales": 0,
            "off_peak_sales": 0,
        }

    total_sales = df["Sales Count"].sum()
    hourly = df.groupby("Hour")["Sales Count"].sum()

    top_hours = hourly.nlargest(4).index.tolist()
    bottom_hours = hourly.nsmallest(4).index.tolist()

    peak_sales = int(df[df["Hour"].isin(top_hours)]["Sales Count"].sum())
    off_peak_sales = int(df[df["Hour"].isin(bottom_hours)]["Sales Count"].sum())

    return {
        "peak_utilization_pct": round((peak_sales / total_sales * 100) if total_sales else 0.0, 2),
        "off_peak_utilization_pct": round((off_peak_sales / total_sales * 100) if total_sales else 0.0, 2),
        "peak_sales": peak_sales,
        "off_peak_sales": off_peak_sales,
        "peak_hours": top_hours,
        "off_peak_hours": bottom_hours,
    }


def off_season_utilization(df: pd.DataFrame) -> dict:
    if df.empty:
        return {
            "annual_avg_sales": 0.0,
            "winter_avg_sales": 0.0,
            "off_season_index": 0.0,
        }

    annual_avg_sales = float(df["Sales Count"].mean())
    winter_sales = df[df["Season"] == "Winter"]["Sales Count"]
    winter_avg_sales = float(winter_sales.mean()) if not winter_sales.empty else 0.0
    off_season_index = round((winter_avg_sales / annual_avg_sales) if annual_avg_sales else 0.0, 3)

    return {
        "annual_avg_sales": round(annual_avg_sales, 2),
        "winter_avg_sales": round(winter_avg_sales, 2),
        "off_season_index": off_season_index,
    }


def detect_outliers(df: pd.DataFrame) -> dict:
    def bounds(series: pd.Series) -> tuple:
        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        return lower, upper

    sales_lower, sales_upper = bounds(df["Sales Count"])
    redemption_lower, redemption_upper = bounds(df["Redemption Count"])

    sales_outliers = df[
        (df["Sales Count"] < sales_lower) | (df["Sales Count"] > sales_upper)
    ].copy()
    redemption_outliers = df[
        (df["Redemption Count"] < redemption_lower)
        | (df["Redemption Count"] > redemption_upper)
    ].copy()

    return {
        "sales_outliers": sales_outliers,
        "redemption_outliers": redemption_outliers,
        "sales_outlier_count": len(sales_outliers),
        "redemption_outlier_count": len(redemption_outliers),
        "sales_bounds": (sales_lower, sales_upper),
        "redemption_bounds": (redemption_lower, redemption_upper),
    }


def data_quality_report(raw_df: pd.DataFrame) -> dict:
    parsed = raw_df.copy()
    parsed["Timestamp"] = pd.to_datetime(parsed["Timestamp"], errors="coerce")

    missing_values = parsed.isna().sum().to_dict()
    duplicate_rows = int(parsed.duplicated().sum())
    invalid_timestamps = int(parsed["Timestamp"].isna().sum())
    negative_sales = int(
        (pd.to_numeric(parsed["Sales Count"], errors="coerce") < 0).sum()
    )
    negative_redemption = int(
        (pd.to_numeric(parsed["Redemption Count"], errors="coerce") < 0).sum()
    )

    total_missing = sum(missing_values.values())
    negative_values = negative_sales + negative_redemption
    quality_score = max(
        0,
        100
        - total_missing * 5
        - duplicate_rows * 2
        - invalid_timestamps * 10
        - negative_values * 5,
    )

    return {
        "missing_values": missing_values,
        "duplicate_rows": duplicate_rows,
        "invalid_timestamps": invalid_timestamps,
        "negative_sales": negative_sales,
        "negative_redemption": negative_redemption,
        "negative_values": negative_values,
        "total_missing": total_missing,
        "quality_score": quality_score,
    }


def build_executive_insights(df: pd.DataFrame) -> dict:
    if df.empty:
        return {
            "peak_hour": None,
            "peak_season": None,
            "highest_month": None,
            "lowest_month": None,
            "net_trend": "No data available.",
            "staffing_recommendation": "Extend monitoring when data returns.",
            "scheduling_recommendation": "Collect more historical data for a complete forecast.",
            "summary": "No valid records are available for executive analysis.",
        }

    peak_hour = int(df.groupby("Hour")["Sales Count"].sum().idxmax())
    peak_season = df.groupby("Season")["Sales Count"].sum().idxmax()

    month_sales = (
        df.groupby("Month")["Sales Count"]
        .sum()
        .reindex(MONTH_ORDER)
        .fillna(0)
    )

    highest_month = month_sales.idxmax()
    lowest_month = month_sales.idxmin()

    monthly_net = (
        df.set_index("Timestamp")["Sales Count"].resample("ME").sum()
        - df.set_index("Timestamp")["Redemption Count"].resample("ME").sum()
    )

    net_trend = "stable"
    if len(monthly_net) >= 2:
        net_trend = (
            "increasing"
            if monthly_net.iloc[-1] > monthly_net.iloc[0]
            else "decreasing"
        )

    summary = (
        f"The fleet is busiest around {peak_hour}:00, with {peak_season} as the top demand season. "
        f"{highest_month} is the highest-demand month while {lowest_month} is the softest. "
        f"Net passenger movement is {net_trend}, and scheduling should favor peak hourly windows."
    )

    staffing_recommendation = (
        f"Increase staffing levels around peak hours ({peak_hour}:00) and during {peak_season}. "
        f"Review weekend and holiday ferry frequency in {highest_month}." 
    )

    scheduling_recommendation = (
        "Target additional ferry trips during identified peak windows and preserve capacity "
        "during off-peak hours to improve system resilience."
    )

    return {
        "peak_hour": peak_hour,
        "peak_season": peak_season,
        "highest_month": highest_month,
        "lowest_month": lowest_month,
        "net_trend": net_trend,
        "staffing_recommendation": staffing_recommendation,
        "scheduling_recommendation": scheduling_recommendation,
        "summary": summary,
    }


def dataframe_to_csv(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8")


def dict_to_csv(data: dict) -> bytes:
    lines = ["Metric,Value"]
    for key, value in data.items():
        lines.append(f"{key},{value}")
    return "\n".join(lines).encode("utf-8")


def dict_to_text(data: dict) -> bytes:
    lines = []
    for key, value in data.items():
        lines.append(f"{key}: {value}")
    return "\n".join(lines).encode("utf-8")
