import streamlit as st

from utils.data_loader import load_data
from utils.dashboard_utils import (
    prepare_data,
    build_global_filters,
    apply_global_filters,
    calculate_kpis,
    build_executive_insights,
)
from utils.theme import apply_theme

apply_theme()

st.title("📋 Executive Summary")

raw_df = load_data()
df = prepare_data(raw_df)
filters = build_global_filters(df)
df = apply_global_filters(df, filters)

if df.empty:
    st.warning("No data is available for the selected filters.")
else:
    kpis = calculate_kpis(df)
    insights = build_executive_insights(df)

    st.markdown("## Key Findings")
    st.write(f"• Total Tickets Sold: {kpis['total_sales']:,}")
    st.write(f"• Total Tickets Redeemed: {kpis['total_redemption']:,}")
    st.write(f"• Net Passenger Movement: {kpis['net_movement']:,}")
    st.write(f"• Peak Demand Hour: {insights['peak_hour']}:00")
    st.write(f"• Peak Demand Season: {insights['peak_season']}")
    st.write(f"• Highest Demand Month: {insights['highest_month']}")
    st.write(f"• Lowest Demand Month: {insights['lowest_month']}")
    st.write(f"• Net Movement Trend: {insights['net_trend']}")

    st.markdown("## Recommended Actions")
    st.success(insights['staffing_recommendation'])
    st.info(insights['scheduling_recommendation'])

    st.markdown("### Executive Summary")
    st.write(insights['summary'])
