import streamlit as st

from utils.data_loader import load_data
from utils.dashboard_utils import (
    prepare_data,
    build_global_filters,
    apply_global_filters,
    rolling_averages,
    get_peak_windows,
    off_peak_metrics,
)
from utils.theme import apply_theme
from utils.visualization import (
    hourly_sales_chart,
    hourly_redemption_chart,
    rolling_average_chart,
    peak_window_heatmap,
    off_peak_comparison_chart,
)

apply_theme()

st.title("📈 Demand Analysis")

raw_df = load_data()
df = prepare_data(raw_df)
filters = build_global_filters(df)
df = apply_global_filters(df, filters)

if df.empty:
    st.warning("No data is available for the selected filters.")
else:
    st.plotly_chart(hourly_sales_chart(df), use_container_width=True)
    st.plotly_chart(hourly_redemption_chart(df), use_container_width=True)

    st.markdown("---")
    st.subheader("Rolling Average Sales")
    hourly = rolling_averages(df)
    st.plotly_chart(rolling_average_chart(hourly), use_container_width=True)

    st.markdown("---")
    st.subheader("Peak and Off-Peak Windows")
    heatmap_data, peak_summary = get_peak_windows(df)
    st.plotly_chart(peak_window_heatmap(heatmap_data), use_container_width=True)
    st.dataframe(peak_summary)

    off_peak = off_peak_metrics(df)
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    col1.metric("Peak Sales", f"{off_peak['peak_sales']:,}")
    col2.metric("Off-Peak Sales", f"{off_peak['off_peak_sales']:,}")
    col3.metric("Peak Utilization", f"{off_peak['peak_utilization_pct']}%")
    st.plotly_chart(off_peak_comparison_chart(off_peak), use_container_width=True)
