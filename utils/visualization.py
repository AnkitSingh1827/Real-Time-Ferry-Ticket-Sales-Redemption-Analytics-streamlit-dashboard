import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def hourly_sales_chart(df):
    hourly = (
        df.groupby("Hour")["Sales Count"]
        .sum()
        .reset_index()
    )

    fig = px.line(
        hourly,
        x="Hour",
        y="Sales Count",
        title="Hourly Ticket Sales",
        markers=True,
    )
    fig.update_layout(xaxis=dict(dtick=1))
    return fig


def hourly_redemption_chart(df):
    hourly = (
        df.groupby("Hour")["Redemption Count"]
        .sum()
        .reset_index()
    )

    fig = px.line(
        hourly,
        x="Hour",
        y="Redemption Count",
        title="Hourly Ticket Redemption",
        markers=True,
    )
    fig.update_layout(xaxis=dict(dtick=1))
    return fig


def sales_vs_redemption(df):
    hourly = (
        df.groupby("Hour")
        [["Sales Count", "Redemption Count"]]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        hourly,
        x="Hour",
        y=["Sales Count", "Redemption Count"],
        barmode="group",
        title="Sales vs Redemption",
    )
    fig.update_layout(xaxis=dict(dtick=1))
    return fig


def monthly_sales_chart(df):
    monthly = (
        df.groupby("Month")["Sales Count"]
        .sum()
        .reset_index()
    )
    month_order = [
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
    monthly["Month"] = pd.Categorical(monthly["Month"], categories=month_order, ordered=True)
    monthly = monthly.sort_values("Month")

    fig = px.bar(
        monthly,
        x="Month",
        y="Sales Count",
        title="Monthly Sales Trend",
    )
    return fig


def rolling_average_chart(hourly_df):
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=hourly_df["Timestamp"],
            y=hourly_df["Sales Count"],
            mode="lines+markers",
            name="Actual Sales",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=hourly_df["Timestamp"],
            y=hourly_df["Sales MA 1H"],
            mode="lines",
            name="1-Hour Rolling Avg",
            line=dict(dash="dash"),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=hourly_df["Timestamp"],
            y=hourly_df["Sales MA 4H"],
            mode="lines",
            name="4-Hour Rolling Avg",
            line=dict(dash="dot"),
        )
    )
    fig.update_layout(
        title="Sales with Rolling Averages",
        xaxis_title="Timestamp",
        yaxis_title="Sales Count",
        hovermode="x unified",
    )
    return fig


def peak_window_heatmap(heatmap_df):
    fig = px.imshow(
        heatmap_df.values,
        x=heatmap_df.columns,
        y=heatmap_df.index,
        labels={"x": "Hour", "y": "Day", "color": "Sales"},
        aspect="auto",
        title="Hourly Sales Heatmap by Day",
        color_continuous_scale="Blues",
    )
    fig.update_xaxes(side="bottom")
    return fig


def off_peak_comparison_chart(metrics):
    chart_df = pd.DataFrame(
        {
            "Window": ["Peak", "Off Peak"],
            "Sales Count": [metrics["peak_sales"], metrics["off_peak_sales"]],
        }
    )
    fig = px.bar(
        chart_df,
        x="Window",
        y="Sales Count",
        title="Peak vs Off-Peak Sales Comparison",
        text="Sales Count",
    )
    fig.update_traces(texttemplate="%{text:,}", textposition="outside")
    return fig


def outlier_box_plot(df, column, title):
    fig = px.box(
        df,
        y=column,
        title=title,
    )
    return fig


def off_season_trend_chart(df):
    monthly = (
        df.groupby("Month")["Sales Count"]
        .sum()
        .reset_index()
    )
    month_order = [
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
    monthly["Month"] = pd.Categorical(monthly["Month"], categories=month_order, ordered=True)
    monthly = monthly.sort_values("Month")

    fig = px.line(
        monthly,
        x="Month",
        y="Sales Count",
        markers=True,
        title="Monthly Sales Trend for Utilization Index",
    )
    return fig


def forecast_line_chart(daily, forecast):
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=daily["ds"],
            y=daily["y"],
            mode="lines+markers",
            name="Actual Sales",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=forecast["ds"],
            y=forecast["yhat"],
            mode="lines",
            name="Forecast",
            line=dict(color="royalblue", width=2),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=forecast["ds"],
            y=forecast["yhat_upper"],
            mode="lines",
            line=dict(color="lightblue"),
            showlegend=False,
        )
    )
    fig.add_trace(
        go.Scatter(
            x=forecast["ds"],
            y=forecast["yhat_lower"],
            mode="lines",
            line=dict(color="lightblue"),
            fill="tonexty",
            fillcolor="rgba(173,216,230,0.25)",
            showlegend=False,
        )
    )
    fig.update_layout(
        title="Demand Forecast with Confidence Interval",
        xaxis_title="Date",
        yaxis_title="Sales Count",
        hovermode="x unified",
    )
    return fig
