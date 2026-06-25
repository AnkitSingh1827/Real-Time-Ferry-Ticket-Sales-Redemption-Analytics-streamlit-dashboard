import streamlit as st
from utils.theme import apply_theme 

st.set_page_config(
    page_title="Toronto Ferry Analytics",
    page_icon="🚢",
    layout="wide"
)

apply_theme()

st.title(
    "🚢 Toronto Island Ferry Analytics Dashboard"
)

st.markdown("---")

st.subheader(
    "Real-Time Ferry Ticket Sales & Redemption Analytics"
)

st.write("""
This dashboard provides comprehensive analytics for Toronto Island Ferry ticket sales and redemption activity, 
with real-time monitoring, demand forecasting, and data quality reporting.

### 📊 Dashboard Pages

**Core Analytics:**
• **Overview** – Key KPIs and dataset snapshot
• **Demand Analysis** – Hourly trends, peak windows, rolling averages
• **Passenger Movement** – Net flow analysis by hour
• **Seasonal Analysis** – Monthly and seasonal patterns with off-season utilization index
• **Executive Summary** – Strategic insights and recommendations

**Advanced Features:**
• **Real-Time Monitor** – Live metrics with auto-refresh (60-second intervals)
• **Demand Forecast** – Prophet-based next day/week/month predictions
• **Data Quality** – Data health scores, outlier detection, and integrity checks
• **Download Center** – Export cleaned data, KPI summaries, and executive reports

### 🎯 Key Capabilities

✓ Global filters for year, month, season, and weekday/weekend analysis
✓ Rolling average calculations (1-hour and 4-hour windows)
✓ Peak/off-peak window detection and heatmaps
✓ Outlier detection with IQR methodology
✓ Data quality reporting with comprehensive health scoring
✓ Time-series forecasting with confidence intervals
✓ Downloadable reports for stakeholder communication

**Use the sidebar to explore individual pages or select filters to customize your analysis.**
""")

