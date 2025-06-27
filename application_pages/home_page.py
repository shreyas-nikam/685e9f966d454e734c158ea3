
import streamlit as st

def run_home_page():
    st.markdown("""
    ## Welcome to the AI Risk Score - V4-2: Career Path Diversification Tool!

    In an era of rapid technological advancement, particularly with the rise of Artificial Intelligence,
    understanding and managing career risk has become paramount. This tool is designed to help you
    assess your personal and professional exposure to AI-driven job displacement and explore strategies
    to enhance your career resilience.

    ### What is AI Risk Score?

    Our model helps you calculate two primary types of risk:

    1.  **Idiosyncratic Risk ($V_i(t)$)**: This represents your individual vulnerability to job displacement.
        It's influenced by factors directly within your control, such as your skills, education, experience,
        and proactive efforts in upskilling. Think of it as the risk specific to *you*.

    2.  **Systematic Risk ($H_i$)**: This reflects the broader, macro-level automation hazard inherent
        to your occupation or industry. It's influenced by external factors like the overall economic climate
        and the pace of AI innovation. This is the risk that affects *everyone* in your field,
        regardless of individual merit.

    ### The "Education is Insurance" Concept

    Just as financial insurance protects against unforeseen losses, continuous learning and strategic career
    planning can act as a form of "career insurance" against AI displacement. This tool allows you to
    simulate how investing in new skills or transitioning to a different career path can reduce your
    risk profile and, conceptually, your "insurance premium."

    ### How It Works

    The application utilizes a set of mathematical models, inspired by actuarial science, to quantify these risks:

    -   **Human Capital Factor ($FHC$)**: Assesses your foundational resilience based on education, experience, and role.
    -   **Company Risk Factor ($FCR$)**: Evaluates the stability and AI adoption of your current employer.
    -   **Upskilling Factor ($FUS$)**: Quantifies the impact of your general and firm-specific training efforts.
    -   These factors combine to determine your **Idiosyncratic Risk ($V_i(t)$)**.

    -   Your **Systematic Risk ($H_i$)** is derived from your occupation's base hazard, adjusted by
        economic conditions ($M_{econ}$) and the AI Innovation Index ($IAI$).

    -   Finally, these risk scores are translated into an **Annual Claim Probability ($P_{claim}$)**
        and an **Annual Expected Loss ($E[Loss]$)**, which then determine your
        **Monthly Insurance Premium ($P_{monthly}$)**.

    You can navigate through the different sections using the sidebar:
    -   **Home**: This introductory page.
    -   **Risk & Premium Calculator**: Input your details to calculate your risk scores and estimated premium.
    -   **Career Transition Simulator**: Explore how changing career paths can mitigate your systematic risk over time.

    Start by exploring the **Risk & Premium Calculator** to understand your current profile!
    """)
