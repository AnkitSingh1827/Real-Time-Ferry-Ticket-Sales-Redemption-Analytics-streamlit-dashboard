import streamlit as st
import base64


def apply_theme():
    try:
        with open("assets/dashboard_banner.jpg", "rb") as img:
            encoded = base64.b64encode(img.read()).decode()
        background_style = f"background-image: url(\"data:image/jpg;base64,{encoded}\");"
    except Exception:
        background_style = "background-color: #0b3d91;"

    st.markdown(
        f"""
        <style>

        .stApp {{
            {background_style}
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}

        .block-container {{
            background: rgba(1, 23, 71, 0.92);
            padding: 2rem 2.4rem;
            border-radius: 24px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.35);
        }}

        section[data-testid="stSidebar"] {{
            background: rgba(2, 45, 112, 0.94);
            color: white;
        }}

        div[data-testid="metric-container"] {{
            background: rgba(255, 255, 255, 0.12);
            border: 1px solid rgba(255, 255, 255, 0.18);
            padding: 18px;
            border-radius: 16px;
        }}

        .stButton>button, .stDownloadButton>button {{
            border-radius: 12px;
            background-color: #0576f3;
            color: white;
            border: none;
        }}

        h1, h2, h3, h4, h5, h6, p, label, span, div {{
            color: white !important;
        }}

        </style>
        """,
        unsafe_allow_html=True,
    )
