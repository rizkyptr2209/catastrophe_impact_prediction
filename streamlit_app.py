import streamlit as st

# --- PAGE SETUP ---
about_page = st.Page(
    page = "views/about_me.py",
    title = "About Me",
    icon = ":material/account_circle:",
    default = True
)
project_1_page = st.Page(
    page = "views/catastrophe_dashboard.py",
    title = "Analytics Dashboard",
    icon = ":material/analytics:",
)
project_2_page = st.Page(
    page = "views/time_series_model.py",
    title = "Casualties Prediction",
    icon = ":material/network_intel_node:",
)

# --- NAVIGATION SETUP [WITHOUT SECTIONS] ---
# pg = st.navigation(pages = [about_page, project_1_page, project_2_page])

# --- NAVIGATION SETUP [WITH SECTIONS] ---
pg = st.navigation(
    {
        "Info" : [about_page],
        "Projects": [project_1_page, project_2_page]
    }
)

# --- SHARED ON ALL PAGES ---
st.logo("assets/Logo.png", size="large")
st.sidebar.text("My first ever Portofolio")

# --- RUN NAVIGATION ---
pg.run()