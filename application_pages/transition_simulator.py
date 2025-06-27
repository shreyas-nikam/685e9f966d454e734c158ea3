
import streamlit as st
import pandas as pd
import numpy as np
from application_pages.calculations import calculate_h_base_ttv, calculate_systematic_risk, get_h_base_for_job_title
from application_pages.data_utils import load_job_data, load_default_parameters
from application_pages.visualization import plot_systematic_risk_over_time

def run_transition_simulator():
    st.header("Career Transition Simulator")
    st.markdown("""
    This section allows you to simulate the impact of a career transition on your Systematic Risk over time.
    By moving to a new role or industry, you can actively diversify and mitigate your exposure to AI risk.
    The simulation will show how your **Systematic Risk ($H_i$)** gradually adjusts to the target career's
    base hazard over a specified **Time-to-Value (TTV)** period.
    """)

    job_data = load_job_data()
    default_params = load_default_parameters()

    st.subheader("1. Current & Target Career Paths")
    col1, col2 = st.columns(2)
    with col1:
        current_job_title = st.selectbox(
            "Current Job Title",
            options=job_data['Job Title'].tolist(),
            index=job_data['Job Title'].tolist().index('Software Engineer') if 'Software Engineer' in job_data['Job Title'].tolist() else 0,
            key="current_job_sim",
            help="Your current occupation, influencing your initial Systematic Risk."
        )
        h_current = get_h_base_for_job_title(current_job_title)
        st.info(f"Current Base Occupational Hazard ($H_{{current}}$): {h_current}")

    with col2:
        target_job_title = st.selectbox(
            "Target Career Path (Industry/Role)",
            options=job_data['Job Title'].tolist(),
            index=job_data['Job Title'].tolist().index('Nurse') if 'Nurse' in job_data['Job Title'].tolist() else 0,
            key="target_job_sim",
            help="The career path you are transitioning into. Aim for a lower H_base for risk mitigation."
        )
        h_target = get_h_base_for_job_title(target_job_title)
        st.info(f"Target Base Occupational Hazard ($H_{{target}}$): {h_target}")

    st.subheader("2. Transition Parameters")
    ttv = st.number_input(
        "Time-to-Value (TTV) Period (Months)",
        min_value=1, max_value=60, value=default_params['TTV_default'], step=1,
        help="The total number of months required for the transition to be fully effective, "
             "meaning your risk profile aligns with the new career."
    )
    months_elapsed = st.slider(
        "Months Elapsed Since Transition Started ($k$)",
        min_value=0, max_value=ttv, value=int(ttv / 2), step=1,
        help="The number of months passed since you began your transition. "
             "Observe how Systematic Risk changes over this period."
    )

    st.subheader("3. Environmental Modifiers (for simulation)")
    m_econ_sim = st.slider(
        "Economic Climate Modifier ($M_{econ}$)",
        min_value=0.8, max_value=1.2, value=1.0, step=0.01,
        key="m_econ_sim",
        help="Adjust this to see how economic conditions affect systematic risk during transition."
    )
    iai_sim = st.slider(
        "AI Innovation Index ($IAI$)",
        min_value=0.8, max_value=1.2, value=1.0, step=0.01,
        key="iai_sim",
        help="Adjust this to see how the pace of AI innovation affects systematic risk during transition."
    )

    st.divider()
    st.subheader("Simulation Results: Systematic Risk Evolution")

    # Calculate H_base(k) and H_i for the current month in simulation
    h_base_k_current_month = calculate_h_base_ttv(months_elapsed, ttv, h_current, h_target)
    h_i_current_month_sim = calculate_systematic_risk(h_base_k_current_month, m_econ_sim, iai_sim)

    st.metric(label=f"Systematic Risk at Month {months_elapsed} ($H_i$)", value=f"{h_i_current_month_sim:.2f}")
    st.caption(f"Your projected Systematic Risk after {months_elapsed} months into the transition.")

    st.markdown("---")

    st.markdown(r"""
    ### Time-to-Value (TTV) Modified Base Occupational Hazard ($H_{base}(k)$)

    The Base Occupational Hazard for an occupation can change over time, especially during a career transition.
    This formula models the gradual reduction in systematic risk as an individual transitions to a lower-risk occupation.
    It showcases the concept of "Career Path Diversification" by demonstrating how systematic risk can be actively mitigated over time.

    $$
    H_{base}(k) = \left(1 - \frac{k}{TTV}\right) H_{current} + \left(\frac{k}{TTV}\right) H_{target}
    $$
    Where:
    -   $H_{base}(k)$: The Base Occupational Hazard score after $k$ months of transition.
    -   $k$: The number of months that have elapsed since the completion of the transition pathway ({months_elapsed}).
    -   $TTV$: The total number of months in the Time-to-Value period ({ttv}).
    -   $H_{current}$: The Base Occupational Hazard score of the individual's original industry ({h_current}).
    -   $H_{target}$: The Base Occupational Hazard score of the new target industry ({h_target}).
    """.format(months_elapsed=months_elapsed, ttv=ttv, h_current=h_current, h_target=h_target))

    # Generate data for the plot
    months = np.arange(0, ttv + 1, 1) # Including month 0 and TTV
    systematic_risks = []
    for k_val in months: # Changed k to k_val to avoid conflict with loop variable in markdown format
        h_base_k = calculate_h_base_ttv(k_val, ttv, h_current, h_target)
        h_i_k = calculate_systematic_risk(h_base_k, m_econ_sim, iai_sim)
        systematic_risks.append(h_i_k)

    df_risk_over_time = pd.DataFrame({
        'Months Elapsed': months,
        'Systematic Risk (H_i)': systematic_risks
    })

    # Plotting the systematic risk evolution
    fig_risk_evolution = plot_systematic_risk_over_time(df_risk_over_time)
    st.plotly_chart(fig_risk_evolution, use_container_width=True)

    st.markdown("""
    ### Interpretation:
    The line chart above illustrates how your **Systematic Risk ($H_i$)** is projected to change
    as you progress through your career transition. You can observe the initial high risk from your
    current occupation gradually diminishing and aligning with the lower risk of your target career.
    This demonstrates the power of **Career Path Diversification** as a strategy to
    mitigate long-term AI-driven displacement risk.
    """)
