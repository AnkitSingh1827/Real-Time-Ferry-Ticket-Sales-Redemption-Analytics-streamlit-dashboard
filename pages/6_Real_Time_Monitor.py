import streamlit as st

from utils.data_loader import load_data
from utils.dashboard_utils import (
    prepare_data,
    build_global_filters,
    apply_global_filters,
    latest_metrics,
)
from utils.theme import apply_theme

st.set_page_config(
    page_title="Real-Time Monitoring",
    page_icon="⏱️",
    layout="wide",
)

apply_theme()

st.title("⏱️ Real-Time Monitoring")
st.markdown(
    "Live-style operations metrics for the most recent Toronto Island ferry data. "
    "The page refreshes automatically every 60 seconds to simulate real-time monitoring."
)

st.markdown(
    "<script>setTimeout(function(){window.location.reload();}, 60000);</script>",
    unsafe_allow_html=True,
)

raw_df = load_data()
df = prepare_data(raw_df)
filters = build_global_filters(df)
df = apply_global_filters(df, filters)

metrics = latest_metrics(df)

if df.empty:
    st.warning("No data is available for the selected filters.")
else:
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("Latest Timestamp", metrics["latest_timestamp"].strftime("%Y-%m-%d %H:%M"))
    kpi2.metric("Latest Sales Count", f"{metrics['latest_sales']:,}")
    kpi3.metric("Latest Redemption Count", f"{metrics['latest_redemption']:,}")
    kpi4.metric("Current Net Movement", f"{metrics['net_movement']:,}")

    st.markdown("---")
    hour1, hour4, hour24 = st.columns(3)
    hour1.metric("Last 1-Hour Sales", f"{metrics['last_1h_sales']:,}")
    hour4.metric("Last 4-Hour Sales", f"{metrics['last_4h_sales']:,}")
    hour24.metric("Last 24-Hour Sales", f"{metrics['last_24h_sales']:,}")

    st.markdown("---")
    st.write(
        "The latest metrics are based on the filtered dataset. Adjust the sidebar filters to inspect different years, seasons, or weekday/weekend traffic."
    )
