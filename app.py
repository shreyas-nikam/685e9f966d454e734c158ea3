
import streamlit as st

st.set_page_config(page_title="AI Risk Score - V4-2", layout="wide")
st.sidebar.image("https://www.quantuniversity.com/assets/img/logo5.jpg")
st.sidebar.divider()
st.title("QuLab: AI Risk Score - V4-2")
st.divider()

st.markdown("""
Welcome to the **Career Path Diversification Tool**, a specialized application within QuLab designed to help you understand and manage your career's exposure to AI-driven job displacement risk. This tool allows you to interactively explore how various factors influence your risk profile and how strategic career decisions, like upskilling and career transitions, can mitigate these risks.

### Business Logic Explained

This application models AI displacement risk using two primary components:

1.  **Idiosyncratic Risk ($V_i(t)$):** This reflects your personal vulnerability, influenced by factors directly within your control such as your **Human Capital ($FHC$)**, the stability of your **Company ($FCR$)**, and your **Upskilling Efforts ($FUS$)**.
    *   **Human Capital ($FHC$)**: Assesses your foundational resilience based on job role, education, and experience.
    *   **Company Risk ($FCR$)**: Quantifies your employer's stability and AI adoption efforts.
    *   **Upskilling ($FUS$)**: Rewards continuous learning, especially in general, portable skills.

    $$
    V_i(t) = \\min(100.0, \\max(5.0, V_{raw} - 50.0))
    $$
    Where:
    $$
    V_{raw} = FHC \\cdot (w_{CR} FCR + w_{US} FUS)
    $$

2.  **Systematic Risk ($H_i$):** This represents the unavoidable macro-level automation hazard of your occupation, adjusted by broader environmental conditions like the **Economic Climate ($M_{econ}$)** and the pace of **AI Innovation ($IAI$)**.

    $$
    H_i = H_{base}(t) \\cdot (w_{econ} M_{econ} + w_{inno} IAI)
    $$

These risk scores are then translated into an **Estimated Monthly Insurance Premium ($P_{monthly}$)**. This premium serves as a tangible financial representation of your overall risk, embodying the concept that investing in career resilience (education, skill development, strategic transitions) can act as a form of "insurance" against job displacement.

The application also features a **Career Path Diversification Simulation**, which demonstrates how proactive career transitions to lower-risk fields can reduce your **Systematic Risk** over a defined **Time-to-Value (TTV)** period.

By interacting with this tool, you will gain insights into:
*   The interplay between personal attributes, employer stability, and external economic forces on your career risk.
*   The financial implications of your risk profile.
*   How strategic upskilling and career transitions can proactively reduce your exposure to AI-driven systematic risk.

Explore the pages using the navigation sidebar to analyze your current risk and simulate future career strategies!
"""")

# Your code starts here
page = st.sidebar.selectbox(label="Navigation", options=["Your Risk Profile", "Career Transition Simulation"])

if page == "Your Risk Profile":
    from application_pages.home_page import run_home_page
    run_home_page()
elif page == "Career Transition Simulation":
    from application_pages.simulation_page import run_simulation_page
    run_simulation_page()
# Your code ends

st.divider()
st.write("© 2025 QuantUniversity. All Rights Reserved.")
st.caption("The purpose of this demonstration is solely for educational use and illustration. "
           "Any reproduction of this demonstration "
           "requires prior written consent from QuantUniversity. "
           "This lab was generated using the QuCreate platform. QuCreate relies on AI models for generating code, which may contain inaccuracies or errors")
