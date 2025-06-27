
import streamlit as st
import pandas as pd
import numpy as np
from calculations import calculate_h_base_ttv, calculate_systematic_risk, get_h_base
from data_utils import load_job_data, get_default_parameters
from visualization import plot_risk_evolution

JOB_DATA = load_job_data()
DEFAULT_PARAMS = get_default_parameters()

def run_simulation_page():
    st.header("Career Path Diversification Simulation")
    st.markdown("Explore how transitioning to a different career path can mitigate your exposure to **Systematic AI Risk** over time. This simulation models the `Time-to-Value (TTV)` concept.")

    st.subheader("1. Your Current Career Context")
    if 'current_job_title' in st.session_state and 'current_job_h_base' in st.session_state:
        current_job_title = st.session_state['current_job_title']
        h_current = st.session_state['current_job_h_base']
        st.info(f"Based on your profile on the 'Risk Profile' page:")
        st.write(f"- **Current Job Title:** `{current_job_title}`")
        st.write(f"- **Base Occupational Hazard ($H_{{current}}$):** `{h_current:.2f}`")
    else:
        st.warning("Please navigate to the 'Risk Profile' page first to set up your current career details.")
        current_job_title = JOB_DATA['Job Title'].tolist()[0]
        h_current = get_h_base(current_job_title)
        st.info(f"Using default current job: **{current_job_title}** (H_base: {h_current:.2f})")


    st.subheader("2. Define Your Target Career Path")
    target_job_title = st.selectbox(
        "Target Career Path (Job Title)",
        [job for job in JOB_DATA['Job Title'].tolist() if job != current_job_title],
        index=0,
        help="Select a new job title you are considering transitioning into. Choose one with a lower H_base to see the diversification effect."
    )
    h_target = get_h_base(target_job_title)
    st.info(f"- **Target Job Title:** `{target_job_title}`")
    st.info(f"- **Target Base Occupational Hazard ($H_{{target}}$):** `{h_target:.2f}`")

    st.subheader("3. Simulation Parameters")
    col_sim1, col_sim2, col_sim3 = st.columns(3)
    with col_sim1:
        ttv_months = st.number_input(
            "Time-to-Value (TTV) Period (Months)",
            min_value=1,
            max_value=60,
            value=DEFAULT_PARAMS['default_ttv_months'],
            step=1,
            help="The total number of months required for the full benefit of the career transition to be realized."
        )
    with col_sim2:
        k_months = st.slider(
            "Months Elapsed Since Transition Started ($k$)",
            0,
            ttv_months,
            0,
            step=1,
            help="Slide this to see the progressive reduction in Systematic Risk over the transition period."
        )
    with col_sim3:
        m_econ_sim = st.slider(
            "Economic Climate Modifier ($M_{econ}$)",
            0.8, 1.2, 1.0, step=0.01,
            help="Adjust the economic climate during the simulation."
        )
        iai_sim = st.slider(
            "AI Innovation Index ($IAI$)",
            0.8, 1.2, 1.0, step=0.01,
            help="Adjust the AI innovation pace during the simulation."
        )

    st.divider()

    # --- Simulation Logic ---
    st.subheader("Simulated Systematic Risk Over Time")

    # Calculate H_base(k) for the current month k
    current_sim_h_base_k = calculate_h_base_ttv(k_months, ttv_months, h_current, h_target)
    current_sim_h_i = calculate_systematic_risk(current_sim_h_base_k, m_econ_sim, iai_sim)

    st.metric(label=f"Systematic Risk ($H_i$) at Month {k_months}", value=f"{current_sim_h_i:.2f}")

    # Generate data for the plot: H_i for each month in TTV period
    simulation_points = []
    for month in range(ttv_months + 1):
        h_base_k = calculate_h_base_ttv(month, ttv_months, h_current, h_target)
        h_i_at_month = calculate_systematic_risk(h_base_k, m_econ_sim, iai_sim)
        simulation_points.append({'Month': month, 'Systematic Risk (H_i)': h_i_at_month})

    simulation_df = pd.DataFrame(simulation_points)

    st.plotly_chart(plot_risk_evolution(simulation_df))

    with st.expander("Understanding the TTV Simulation"):
        st.markdown(r"The **Time-to-Value (TTV) Modified Base Occupational Hazard** ($H_{base}(k)$) illustrates how your occupational risk gradually changes as you transition to a new role. It is calculated as:")
        st.latex(r"H_{base}(k) = \left(1 - rac{k}{TTV}ight) H_{current} + \left(rac{k}{TTV}ight) H_{target}")
        st.markdown(r"Where:")
        st.markdown(f"- $H_{{current}}$: Your original job's base hazard ({h_current:.2f}).")
        st.markdown(f"- $H_{{target}}$: Your target job's base hazard ({h_target:.2f}).")
        st.markdown(f"- $TTV$: Total transition period in months ({ttv_months} months).")
        st.markdown(f"- $k$: Months elapsed since transition started ({k_months} months).")
        st.markdown(r"This formula shows a linear interpolation between your current and target occupational hazards. As $k$ approaches $TTV$, your base hazard shifts from $H_{current}$ to $H_{target}$, reflecting a successful career path diversification.")
        st.markdown(r"The **Systematic Risk ($H_i$)** at any point $k$ is then calculated by adjusting this $H_{base}(k)$ with environmental modifiers:")
        st.latex(r"H_i = H_{base}(k) \cdot (w_{econ} M_{econ} + w_{inno} IAI)")
        st.markdown(f"Current $M_{{econ}}$: `{m_econ_sim:.2f}`, Current $IAI$: `{iai_sim:.2f}`.")
        st.markdown("This simulation demonstrates that by strategically choosing a career path with a lower systematic risk (lower $H_{target}$) and investing in a transition, you can actively reduce your long-term exposure to AI displacement.")
