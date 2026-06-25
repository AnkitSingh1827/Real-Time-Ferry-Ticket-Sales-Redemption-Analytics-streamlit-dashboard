import streamlit as st
import pandas as pd

from utils.data_loader import load_data
from utils.dashboard_utils import (
    prepare_data,
    build_global_filters,
    apply_global_filters,
    data_quality_report,
    detect_outliers,
)
from utils.theme import apply_theme
from utils.visualization import outlier_box_plot

apply_theme()

st.title("🧩 Data Quality & Outlier Analysis")

raw_df = load_data()
df = prepare_data(raw_df)
filters = build_global_filters(df)
df = apply_global_filters(df, filters)

quality = data_quality_report(raw_df)

st.markdown("## Data Quality Summary")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Quality Score", f"{quality['quality_score']} / 100")
col2.metric("Missing Values", f"{quality['total_missing']}")
col3.metric("Duplicate Rows", f"{quality['duplicate_rows']}")
col4.metric("Invalid Timestamps", f"{quality['invalid_timestamps']}")

st.markdown("### Data Health Details")
st.write(quality['missing_values'])

st.markdown("---")

outliers = detect_outliers(df)

st.markdown("## Outlier Detection")
col5, col6 = st.columns(2)
col5.metric("Sales Outliers", outliers['sales_outlier_count'])
col6.metric("Redemption Outliers", outliers['redemption_outlier_count'])

if not outliers['sales_outliers'].empty:
    st.plotly_chart(
        outlier_box_plot(outliers['sales_outliers'], 'Sales Count', 'Sales Outliers'),
        use_container_width=True,
    )

if not outliers['redemption_outliers'].empty:
    st.plotly_chart(
        outlier_box_plot(outliers['redemption_outliers'], 'Redemption Count', 'Redemption Outliers'),
        use_container_width=True,
    )

st.markdown("---")
st.write(
    "Use this page to check the underlying dataset quality, identify outlier records, "
    "and confirm the health of the ticket sales and redemption streams before operational planning."
)    