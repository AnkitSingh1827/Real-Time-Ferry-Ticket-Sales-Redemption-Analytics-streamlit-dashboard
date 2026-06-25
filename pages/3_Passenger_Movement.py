import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import load_data
from utils.dashboard_utils import (
    prepare_data,
    build_global_filters,
    apply_global_filters,
)
from utils.visualization import sales_vs_redemption
from utils.theme import apply_theme

apply_theme()

st.title("🚶 Passenger Movement Analysis")

raw_df = load_data()
df = prepare_data(raw_df)
filters = build_global_filters(df)
df = apply_global_filters(df, filters)

if df.empty:
    st.warning("No data is available for the selected filters.")
else:
    df["Net Movement"] = df["Sales Count"] - df["Redemption Count"]

    st.plotly_chart(sales_vs_redemption(df), use_container_width=True)

    movement = (
        df.groupby("Hour")["Net Movement"]
        .sum()
        .reset_index()
    )

    fig = px.line(
        movement,
        x="Hour",
        y="Net Movement",
        title="Net Passenger Movement",
        markers=True,
    )
    fig.update_layout(xaxis=dict(dtick=1))

    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(movement.sort_values("Net Movement", ascending=False))
