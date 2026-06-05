from __future__ import annotations

import streamlit as st

from utils.ui import inject_global_styles


st.set_page_config(
    page_title="Cody Xu | Data Science Portfolio",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_global_styles()

pages = [
    st.Page("pages/0_App_Introduction.py", title="App Introduction", icon=":material/home:"),
    st.Page(
        "pages/2_Marketing_Mix_Modelling_Google_Meridian.py",
        title="Marketing Mix Modelling",
        icon=":material/analytics:",
    ),
    st.Page(
        "pages/1_Geo_Based_Incrementality_Test.py",
        title="Geo-based Incrementality Test",
        icon=":material/map:",
    ),
    st.Page(
        "pages/5_Luxury_Customer_Segmentation.py",
        title="Customer Segmentation",
        icon=":material/groups:",
    ),
    st.Page(
        "pages/3_Third_Party_Data_Dashboard.py",
        title="Sales Dashboard",
        icon=":material/dashboard:",
    ),
    st.Page(
        "pages/4_Macro_Economy_Financial_KPI_Tracker.py",
        title="Macro-economy & Financial KPI Tracker",
        icon=":material/monitoring:",
    ),
]

navigation = st.navigation(pages, position="top")
navigation.run()
