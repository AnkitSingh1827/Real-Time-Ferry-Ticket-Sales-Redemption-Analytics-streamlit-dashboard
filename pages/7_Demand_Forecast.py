import streamlit as st

from utils.data_loader import load_data
from utils.dashboard_utils import prepare_data, build_global_filters, apply_global_filters
from utils.forecasting import (
    prepare_prophet_data,
    fit_prophet_model,
    forecast_model,
    forecast_summary,
)
from utils.visualization import forecast_line_chart
from utils.theme import apply_theme

st.set_page_config(
    page_title="Demand Forecast",
    page_icon="📅",
    layout="wide",
)

apply_theme()

st.title("📅 Demand Forecast")
st.markdown(
    "Generate short-term demand projections using Prophet for the next day, week, and month. "
    "Use the forecast confidence interval to support planning decisions."
)

raw_df = load_data()
df = prepare_data(raw_df)
filters = build_global_filters(df)
df = apply_global_filters(df, filters)

if df.empty:
    st.warning("No filtered records are available for forecasting.")
else:
    daily = prepare_prophet_data(df)
    if len(daily) < 14:
        st.warning(
            "Forecasting works best with at least 14 days of historical data. "
            "Use a larger time window for more reliable predictions."
        )

    model = fit_prophet_model(daily)
    forecast = forecast_model(model, periods=30)
    summary = forecast_summary(forecast, daily["ds"].max())

    metric1, metric2, metric3, metric4 = st.columns(4)
    metric1.metric("Next Day Forecast", f"{summary['next_day']:,}")
    metric2.metric("Next Week Avg", f"{summary['next_week_avg']:,}")
    metric3.metric("Next Month Avg", f"{summary['next_month_avg']:,}")
    metric4.metric(
        "Forecast Range",
        f"{summary['next_day_lower']:,} - {summary['next_day_upper']:,}",
    )

    st.markdown("---")
    st.plotly_chart(
        forecast_line_chart(daily, forecast),
        use_container_width=True,
    )

    st.markdown(
        "Forecasts use historical daily sales patterns, weekly seasonality, and annual demand trends. "
        "Review confidence intervals before making operational commitments."
    )
