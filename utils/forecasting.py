import numpy as np
import pandas as pd

try:
    from prophet import Prophet as ProphetModel
except ImportError:  # pragma: no cover - depends on environment
    ProphetModel = None


class SimpleProphetFallback:
    def __init__(self, daily_seasonality=True, weekly_seasonality=True, yearly_seasonality=True):
        self.daily_seasonality = daily_seasonality
        self.weekly_seasonality = weekly_seasonality
        self.yearly_seasonality = yearly_seasonality
        self.history_ = None

    def fit(self, df_daily: pd.DataFrame):
        df = df_daily.copy()
        df["ds"] = pd.to_datetime(df["ds"])
        df = df.sort_values("ds").reset_index(drop=True)
        df["y"] = pd.to_numeric(df["y"], errors="coerce").fillna(0)

        self.history_ = df
        x = np.arange(len(df))
        y = df["y"].to_numpy(dtype=float)
        self._trend_params = np.polyfit(x, y, 1)

        weekly_means = df.groupby(df["ds"].dt.dayofweek)["y"].mean()
        weekly_means = weekly_means.reindex(range(7), fill_value=weekly_means.mean())
        self._weekly_effect = weekly_means.to_dict()

        yearly_means = df.groupby(df["ds"].dt.dayofyear)["y"].mean()
        yearly_means = yearly_means.reindex(range(1, 367), fill_value=yearly_means.mean())
        self._yearly_effect = yearly_means.to_dict()
        return self

    def make_future_dataframe(self, periods: int = 30, freq: str = "D") -> pd.DataFrame:
        if self.history_ is None or self.history_.empty:
            raise ValueError("The model must be fitted before creating a future dataframe.")

        last_date = self.history_["ds"].max()
        future_dates = pd.date_range(last_date + pd.Timedelta(days=1), periods=periods, freq=freq)
        return pd.DataFrame({"ds": future_dates})

    def predict(self, future: pd.DataFrame) -> pd.DataFrame:
        if self.history_ is None:
            raise ValueError("The model must be fitted before predicting.")

        future = future.copy()
        future["ds"] = pd.to_datetime(future["ds"])
        history_len = len(self.history_)
        x_future = np.arange(history_len, history_len + len(future))
        trend = np.polyval(self._trend_params, x_future)

        weekly = future["ds"].dt.dayofweek.map(lambda day: self._weekly_effect.get(day, 0))
        yearly = future["ds"].dt.dayofyear.map(lambda day: self._yearly_effect.get(day, 0))

        yhat = trend + weekly.to_numpy(dtype=float) + yearly.to_numpy(dtype=float)
        yhat = np.maximum(yhat, 0)

        future["yhat"] = yhat
        future["yhat_lower"] = np.maximum(yhat - 2, 0)
        future["yhat_upper"] = yhat + 2
        return future


Prophet = ProphetModel if ProphetModel is not None else SimpleProphetFallback


def prepare_prophet_data(df: pd.DataFrame) -> pd.DataFrame:
    daily = (
        df.set_index("Timestamp")["Sales Count"]
        .resample("D")
        .sum()
        .reset_index()
    )
    daily = daily.rename(columns={"Timestamp": "ds", "Sales Count": "y"})
    return daily


def fit_prophet_model(df_daily: pd.DataFrame) -> Prophet:
    model = Prophet(
        daily_seasonality=True,
        weekly_seasonality=True,
        yearly_seasonality=True,
    )
    model.fit(df_daily)
    return model


def forecast_model(model: Prophet, periods: int = 30) -> pd.DataFrame:
    future = model.make_future_dataframe(periods=periods, freq="D")
    forecast = model.predict(future)
    return forecast


def forecast_summary(forecast: pd.DataFrame, last_date: pd.Timestamp) -> dict:
    future = forecast[forecast["ds"] > last_date]
    next_day = future.head(1)
    next_week = future.head(7)
    next_month = future.head(30)

    return {
        "next_day": int(next_day["yhat"].iloc[0]) if not next_day.empty else 0,
        "next_week_avg": round(float(next_week["yhat"].mean()), 2) if not next_week.empty else 0.0,
        "next_month_avg": round(float(next_month["yhat"].mean()), 2) if not next_month.empty else 0.0,
        "next_day_lower": int(next_day["yhat_lower"].iloc[0]) if not next_day.empty else 0,
        "next_day_upper": int(next_day["yhat_upper"].iloc[0]) if not next_day.empty else 0,
    }
