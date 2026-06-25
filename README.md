# Toronto Ferry Analytics

## 🚢 Project Overview

This project is a Streamlit dashboard for analyzing Toronto Island ferry ticket sales and redemption activity. It helps users understand demand patterns, passenger movement, seasonal trends, and executive insights from the ticket dataset.

The dashboard is organized into pages with charts, metrics, and simple filters to support ferry operations planning and passenger analytics.

## 📌 Key Features

- Overview dashboard with main KPIs and dataset summary
- Demand analysis using hourly sales and redemption trends
- Passenger movement analysis comparing ticket sales to redemptions
- Seasonal analysis of monthly sales, seasons, and weekend vs. weekday demand
- Executive summary with key findings and recommendations

## 🗂 Project Structure

- `app.py` — Streamlit entry point and landing page
- `README.md` — Project documentation
- `requirements.txt` — Python libraries required to run the dashboard
- `assets/` — Static files used for dashboard styling and theme
- `data/` — Source dataset file(s)
- `pages/` — Streamlit pages for each analysis section
- `utils/` — Helper modules for data loading, cleaning, feature engineering, KPI calculation, visualization, and theme styling

### Pages

- `pages/1_Overview.py` — Dashboard overview with KPIs and dataset preview
- `pages/2_Demand_Analysis.py` — Hourly demand charts and peak demand hour by year
- `pages/3_Passenger_Movement.py` — Sales vs redemption comparison and net movement trends
- `pages/4_Seasonal_Analysis.py` — Monthly and seasonal demand analysis
- `pages/5_Executive_Summary.py` — High-level insights and recommendations

## 🔧 Data Flow

1. Load the dataset from `data/Toronto Island Ferry Tickets.csv`
2. Clean and standardize columns in `utils/data_cleaning.py`
3. Add time-based features in `utils/feature_engineering.py`
4. Calculate KPIs in `utils/kpi_calculator.py`
5. Build visual charts in `utils/visualization.py`
6. Apply visual theme in `utils/theme.py`

## 📥 Prerequisites

Install Python dependencies from `requirements.txt`.

## 🚀 Installation & Running

1. Open a terminal in the project folder.
2. (Optional) Create a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Install dependencies:

```powershell
pip install -r requirements.txt
```

4. Run the Streamlit app:

```powershell
streamlit run app.py
```

5. Open the browser page shown by Streamlit to view the dashboard.

## 🧠 What the Dashboard Shows

- Total tickets sold and total tickets redeemed
- Net passenger movement and average sales
- Hourly sales and redemption patterns
- Peak demand hour for selected years
- Comparison of sales vs redemption by hour
- Seasonal demand across months and seasons
- Weekend vs weekday ticket sales

## 📊 Dataset Notes

The dashboard reads the file:

- `data/Toronto Island Ferry Tickets.csv`

The cleaning process:

- Converts `Timestamp` values to datetime
- Drops invalid timestamps and duplicate rows
- Converts `Sales Count` and `Redemption Count` to numbers
- Fills missing sales / redemption values with `0`

## ☑️ Dependencies

This project uses:

- `streamlit`
- `pandas`
- `numpy`
- `plotly`
- `matplotlib`
- `seaborn`

## 💡 Notes

- The app uses a custom dashboard theme from `utils/theme.py`.
- Make sure `assets/dashboard_banner.jpg` exists if the theme loads an image background.
- If the data file is updated, refresh the app to reflect new analysis.

## 🙋‍♂️ Next Steps

- Add more filters for date ranges and ferry routes
- Include forecasting for future ferry demand
- Add a download option for the cleaned dataset
- Improve the executive summary with automated insights
