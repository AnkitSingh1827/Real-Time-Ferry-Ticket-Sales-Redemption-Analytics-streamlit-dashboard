# Toronto Ferry Analytics

## 🚢 Project Overview

This repository contains a multi-page Streamlit dashboard for analyzing Toronto Island ferry ticket sales and redemption activity. It is designed for operations teams, planners, and stakeholders who want to understand demand patterns, passenger movement, seasonality, data quality, and short-term forecasting.

📍 *Live App*: 👉 [Check it out here](https://real-time-ferry-ticket-sales-redemption-analytics-app-dashboar.streamlit.app/)


## ✨ What the Dashboard Includes

- Overview metrics for total sales, redemptions, net movement, and average demand
- Demand analysis with hourly, daily, and seasonal trends
- Passenger movement insights comparing ticket sales to redemptions
- Seasonal analysis covering monthly patterns, weekend vs. weekday behavior, and utilization trends
- Executive summary with high-level findings and recommendations
- Real-time monitoring page with auto-refresh behavior
- Forecasting page for short-term demand projections
- Data quality page for integrity checks and outlier detection
- Download center for exporting cleaned data and summary reports

## 🗂 Project Structure

- app.py — Streamlit entry point and landing page
- README.md — Project documentation
- requirements.txt — Python dependencies
- assets/ — Static assets for dashboard styling
- data/ — Input dataset files
- pages/ — Multi-page Streamlit app modules
- utils/ — Data loading, cleaning, feature engineering, KPI calculations, forecasting, visualization, and theme helpers
- tests/ — Automated tests for forecasting and visualization logic
- scripts/ — Utility scripts and support helpers
- reports/ — Report outputs and export artifacts

### Dashboard Pages

- pages/1_Overview.py — Summary KPIs and dataset snapshot
- pages/2_Demand_Analysis.py — Hourly demand and peak-window analysis
- pages/3_Passenger_Movement.py — Sales vs. redemption movement insights
- pages/4_Seasonal_Analysis.py — Monthly and seasonal demand patterns
- pages/5_Executive_Summary.py — Key findings and recommendations
- pages/6_Real_Time_Monitor.py — Auto-refresh monitoring page
- pages/7_Demand_Forecast.py — Forecasting interface for future demand
- pages/8_Download_Center.py — Downloadable exports and reports
- pages/9_Data_Quality.py — Data health and outlier analysis

## 🔧 Data Flow

1. Load the dataset from data/Toronto Island Ferry Tickets.csv
2. Clean and standardize the data in utils/data_cleaning.py
3. Create time-based features in utils/feature_engineering.py
4. Calculate KPIs in utils/kpi_calculator.py
5. Build visualizations in utils/visualization.py
6. Apply the dashboard theme in utils/theme.py

## 📊 Data Source

The dashboard uses the file:

- data/Toronto Island Ferry Tickets.csv

The cleaning pipeline converts timestamp values, removes invalid or duplicate records, and fills missing values where needed.

## 🛠 Installation

1. Open a terminal in the project folder.
2. Create and activate a virtual environment (optional but recommended):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Install the required packages:

```powershell
pip install -r requirements.txt
```

4. Run the dashboard:

```powershell
streamlit run app.py
```

## 📦 Dependencies

The project uses:

- streamlit
- pandas
- numpy
- plotly
- matplotlib
- seaborn

Forecasting support is also included and can use Prophet when it is available in the environment.

## 💡 Notes

- The app uses a custom theme defined in utils/theme.py.
- If the data file changes, refresh the app to reflect the latest analysis.
- The project includes automated tests under tests/ for forecasting and visualization behavior.
