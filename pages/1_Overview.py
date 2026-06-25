import streamlit as st

from utils.data_loader import load_data
from utils.dashboard_utils import (
    prepare_data,
    build_global_filters,
    apply_global_filters,
    calculate_kpis,
)
from utils.theme import apply_theme

apply_theme()

st.set_page_config(layout="wide")

st.title("📊 Dashboard Overview")

raw_df = load_data()
df = prepare_data(raw_df)
filters = build_global_filters(df)
df = apply_global_filters(df, filters)

kpis = calculate_kpis(df)

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Tickets Sold", f"{kpis['total_sales']:,}")
col2.metric("Total Redeemed", f"{kpis['total_redemption']:,}")
col3.metric("Net Movement", f"{kpis['net_movement']:,}")
col4.metric("Peak Hour", f"{kpis['peak_hour']}:00")
col5.metric("Avg Sales", kpis['avg_sales'])

st.markdown("---")

st.subheader("Dataset Overview")
if df.empty:
    st.warning("No data is available for the selected filters.")
else:
    st.write(df.head())
    st.write("Total Records:", len(df))
    st.write(
        f"Data range: {df['Timestamp'].min().strftime('%Y-%m-%d')} to {df['Timestamp'].max().strftime('%Y-%m-%d')}"
    )
