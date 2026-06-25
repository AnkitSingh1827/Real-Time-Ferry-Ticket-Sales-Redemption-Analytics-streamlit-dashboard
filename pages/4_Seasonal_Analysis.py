import streamlit as st
import plotly.express as px

from utils.data_loader import load_data
from utils.dashboard_utils import (
    prepare_data,
    build_global_filters,
    apply_global_filters,
    off_season_utilization,
)
from utils.visualization import monthly_sales_chart, off_season_trend_chart
from utils.theme import apply_theme

apply_theme()

st.title("🌤 Seasonal Analysis")

raw_df = load_data()
df = prepare_data(raw_df)
filters = build_global_filters(df)
df = apply_global_filters(df, filters)

if df.empty:
    st.warning("No data is available for the selected filters.")
else:
    st.plotly_chart(monthly_sales_chart(df), use_container_width=True)

    season_data = (
        df.groupby("Season")["Sales Count"]
        .sum()
        .reset_index()
    )
    fig = px.pie(
        season_data,
        names="Season",
        values="Sales Count",
        title="Season-wise Demand",
    )
    st.plotly_chart(fig, use_container_width=True)

    weekend_data = (
        df.groupby("Weekend")["Sales Count"]
        .sum()
        .reset_index()
    )
    fig2 = px.bar(
        weekend_data,
        x="Weekend",
        y="Sales Count",
        title="Weekend vs Weekday Demand",
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")
    st.subheader("Off-Season Utilization Index")
    off_season = off_season_utilization(df)
    c1, c2, c3 = st.columns(3)
    c1.metric("Annual Avg Sales", f"{off_season['annual_avg_sales']}")
    c2.metric("Winter Avg Sales", f"{off_season['winter_avg_sales']}")
    c3.metric("Utilization Index", f"{off_season['off_season_index']}")
    st.plotly_chart(off_season_trend_chart(df), use_container_width=True)
