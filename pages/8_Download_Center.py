import streamlit as st

from utils.data_loader import load_data
from utils.dashboard_utils import (
    prepare_data,
    build_global_filters,
    apply_global_filters,
    calculate_kpis,
    build_executive_insights,
    dataframe_to_csv,
    dict_to_csv,
    dict_to_text,
)
from utils.theme import apply_theme

st.set_page_config(
    page_title="Download Center",
    page_icon="⬇️",
    layout="wide",
)

apply_theme()

st.title("⬇️ Download Center")
st.markdown(
    "Download cleaned data, KPI summaries, and the executive summary as shareable reports for operations and stakeholder review."
)

raw_df = load_data()
df = prepare_data(raw_df)
filters = build_global_filters(df)
df = apply_global_filters(df, filters)

if df.empty:
    st.warning("No data is available to download with the selected filters.")
else:
    kpis = calculate_kpis(df)
    insights = build_executive_insights(df)

    col1, col2, col3 = st.columns(3)
    col1.download_button(
        label="Download Cleaned Dataset",
        data=dataframe_to_csv(df),
        file_name="cleaned_toronto_ferry_data.csv",
        mime="text/csv",
    )

    col2.download_button(
        label="Download KPI Summary",
        data=dict_to_csv(kpis),
        file_name="ferry_kpi_summary.csv",
        mime="text/csv",
    )

    col3.download_button(
        label="Download Executive Summary",
        data=dict_to_text(insights),
        file_name="executive_summary.txt",
        mime="text/plain",
    )

    st.markdown("---")
    st.write("### Download Notes")
    st.write(
        "The cleaned dataset includes all filters applied in the sidebar. "
        "Use KPI or executive summary exports for decision support, staffing, and schedule planning."
    )
