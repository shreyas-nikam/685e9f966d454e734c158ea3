
import streamlit as st
import os

# Set Streamlit page configuration
st.set_page_config(page_title="QuLab: AI Risk Score - V4-2", layout="wide")

# Sidebar for logo and navigation
st.sidebar.image("https://www.quantuniversity.com/assets/img/logo5.jpg")
st.sidebar.divider()
st.title("QuLab: AI Risk Score - V4-2")
st.sidebar.divider()

# Business logic explanation for the end users
st.markdown("""
## AI Risk Score - V4-2: Career Path Diversification Tool

In an era of rapid technological advancement, particularly with the rise of Artificial Intelligence,
understanding and managing career risk has become paramount. This **QuLab** application is designed to help you
assess your personal and professional exposure to AI-driven job displacement and explore strategies
to enhance your career resilience.

### Key Concepts:

*   **Idiosyncratic Risk ($V_i(t)$)**: Your individual vulnerability to job displacement. It's influenced by
    factors within your direct control (skills, education, experience, upskilling efforts).
    This is the risk specific to *you*.

    The formula for Idiosyncratic Risk is:
    $$
    V_i(t) = \min(100.0, \max(5.0, V_{raw} - 50.0))
    $$
    Where $V_{raw}$ combines Human Capital, Company, and Upskilling Factors.

*   **Systematic Risk ($H_i$)**: The broader, macro-level automation hazard inherent to your occupation or industry.
    It's influenced by external factors like economic climate ($M_{econ}$) and AI innovation ($IAI$).
    This is the risk that affects *everyone* in your field.

    The formula for Systematic Risk is:
    $$
    H_i = H_{base}(t) \cdot (w_{econ} M_{econ} + w_{inno} IAI)
    $$
    Where $H_{base}(t)$ is the Base Occupational Hazard for the occupation.

*   **"Education is Insurance"**: This concept illustrates how continuous learning and strategic career
    planning can act as a form of "career insurance" against AI displacement. By managing your risk factors,
    you effectively reduce your potential "insurance premium" against job loss.

    Your **Monthly Insurance Premium ($P_{monthly}$)** is derived from your **Annual Expected Loss ($E[Loss]$)**:
    $$
    P_{monthly} = \max \left( \frac{E[Loss] \cdot \lambda}{12}, P_{min} \right)
    $$
    Where $\lambda$ is the loading factor and $P_{min}$ is the minimum premium.

Use the navigation menu on the left to explore different aspects of the tool.
""")

# Navigation
st.markdown("---")
page = st.sidebar.selectbox(
    label="Navigation",
    options=["Home", "Risk & Premium Calculator", "Career Transition Simulator"],
    help="Select a page to navigate through the application."
)

# Load and run the selected page
if page == "Home":
    from application_pages.home_page import run_home_page
    run_home_page()
elif page == "Risk & Premium Calculator":
    from application_pages.risk_premium_calculator import run_risk_premium_calculator
    run_risk_premium_calculator()
elif page == "Career Transition Simulator":
    from application_pages.transition_simulator import run_transition_simulator
    run_transition_simulator()

st.divider()
st.write("© 2025 QuantUniversity. All Rights Reserved.")
st.caption("The purpose of this demonstration is solely for educational use and illustration. "
           "Any reproduction of this demonstration "
           "requires prior written consent from QuantUniversity. "
           "This lab was generated using the QuCreate platform. QuCreate relies on AI models for generating code, which may contain inaccuracies or errors.")
