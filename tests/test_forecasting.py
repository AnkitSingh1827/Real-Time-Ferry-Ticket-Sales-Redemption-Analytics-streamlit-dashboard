import unittest

import pandas as pd

from utils.forecasting import (
    prepare_prophet_data,
    fit_prophet_model,
    forecast_model,
    forecast_summary,
)


class ForecastingTests(unittest.TestCase):
    def test_forecast_pipeline_runs(self):
        df = pd.DataFrame(
            {
                "Timestamp": pd.date_range("2024-01-01", periods=20, freq="D"),
                "Sales Count": [10, 12, 14, 13, 15, 18, 20, 19, 21, 24, 23, 25, 28, 27, 30, 29, 32, 35, 34, 36],
            }
        )

        daily = prepare_prophet_data(df)
        self.assertIn("ds", daily.columns)
        self.assertIn("y", daily.columns)

        model = fit_prophet_model(daily)
        forecast = forecast_model(model, periods=5)
        self.assertGreaterEqual(len(forecast), 5)
        self.assertIn("yhat", forecast.columns)

        summary = forecast_summary(forecast, daily["ds"].max())
        self.assertIn("next_day", summary)


if __name__ == "__main__":
    unittest.main()
