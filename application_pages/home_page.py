
import streamlit as st
import pandas as pd
from calculations import (
    calculate_fhc, calculate_fcr, calculate_fus, calculate_v_raw, calculate_idiosyncratic_risk,
    get_h_base, calculate_systematic_risk, calculate_l_payout, calculate_e_loss,
    calculate_p_systemic, calculate_p_individual_systemic, calculate_p_claim, calculate_p_monthly
)
from data_utils import load_job_data, load_education_data, load_school_tier_data, load_company_type_data, get_default_parameters
from visualization import plot_factor_impact

JOB_DATA = load_job_data()
EDU_DATA = load_education_data()
SCHOOL_DATA = load_school_tier_data()
COMPANY_DATA = load_company_type_data()
DEFAULT_PARAMS = get_default_parameters()

def run_home_page():
    st.header("Your Current AI Risk Profile")
    st.markdown("Adjust the parameters below to understand your current AI displacement risk and potential insurance premium.")

    # --- Input Forms and Widgets ---
    st.subheader("1. Your Professional Profile")
    col1, col2 = st.columns(2)
    with col1:
        job_title = st.selectbox(
            "Job Title",
            JOB_DATA['Job Title'].tolist(),
            index=0,
            help="Select your current job title to determine your base role vulnerability."
        )
        years_experience = st.number_input(
            "Years of Experience",
            min_value=0,
            max_value=50,
            value=5,
            step=1,
            help="Your total years of professional experience. More experience can reduce risk."
        )
        education_level = st.selectbox(
            "Highest Education Level",
            list(EDU_DATA.keys())[:5], # First 5 are levels
            index=2, # Bachelor's
            help="Your highest academic qualification."
        )
    with col2:
        education_field = st.selectbox(
            "Education Field",
            list(EDU_DATA.keys())[5:], # Last items are fields
            index=0, # Tech/Engineering
            help="Your primary field of study. Some fields offer more transferable skills."
        )
        school_tier = st.selectbox(
            "Institution Tier",
            list(SCHOOL_DATA.keys()),
            index=2, # Tier 3
            help="The perceived tier of your educational institution. A proxy for training quality."
        )
        company_type = st.selectbox(
            "Company Type",
            list(COMPANY_DATA.keys()),
            index=0, # Big Firm
            help="The type of company you work for. Affects company risk factors."
        )

    st.subheader("2. Your Upskilling Efforts")
    col_up1, col_up2 = st.columns(2)
    with col_up1:
        p_gen = st.slider(
            "General Skills Training Progress (%)",
            0, 100, 0,
            help="Progress in general/portable skills (e.g., coding, data analysis, project management)."
        ) / 100.0
    with col_up2:
        p_spec = st.slider(
            "Firm-Specific Skills Training Progress (%)",
            0, 100, 0,
            help="Progress in skills specific to your current firm/industry (e.g., internal software, niche processes)."
        ) / 100.0

    st.subheader("3. Environmental Modifiers")
    col_env1, col_env2 = st.columns(2)
    with col_env1:
        m_econ = st.slider(
            "Economic Climate Modifier ($M_{econ}$)",
            0.8, 1.2, 1.0, step=0.01,
            help="Reflects the overall economic environment. <1.0 for recession, >1.0 for boom. Affects Systematic Risk."
        )
    with col_env2:
        iai = st.slider(
            "AI Innovation Index ($IAI$)",
            0.8, 1.2, 1.0, step=0.01,
            help="Momentum indicator for AI technological change. <1.0 for slowdown, >1.0 for rapid breakthrough. Affects Systematic Risk."
        )

    st.subheader("4. Actuarial Parameters")
    col_act1, col_act2 = st.columns(2)
    with col_act1:
        annual_salary = st.number_input(
            "Annual Salary ($)",
            min_value=0, value=90000, step=1000,
            help="Your current annual salary. Used to calculate potential payout."
        )
        coverage_percentage = st.slider(
            "Coverage Percentage (%)",
            0, 100, 25,
            help="Percentage of your monthly salary covered by the policy."
        ) / 100.0
    with col_act2:
        coverage_duration_months = st.number_input(
            "Coverage Duration (Months)",
            min_value=1, value=6, step=1,
            help="Duration in months for which the salary will be paid out if a claim is triggered."
        )
        loading_factor = st.number_input(
            "Loading Factor ($\lambda$)",
            min_value=1.0, value=1.5, step=0.1, format="%.1f",
            help="An insurance multiplier to cover administrative costs and profit margin."
        )
        min_premium = st.number_input(
            "Minimum Monthly Premium ($P_{min}$)",
            min_value=0.0, value=20.00, step=1.0, format="%.2f",
            help="The minimum monthly premium to ensure policy viability."
        )

    st.divider()

    # --- Calculations ---
    # Human Capital Factor
    fhc = calculate_fhc(job_title, education_level, education_field, school_tier, years_experience)

    # Company Risk Factor
    fcr = calculate_fcr(company_type)

    # Upskilling Factor
    fus = calculate_fus(p_gen, p_spec)

    # Raw Idiosyncratic Risk
    v_raw = calculate_v_raw(fhc, fcr, fus)

    # Idiosyncratic Risk
    v_i_t = calculate_idiosyncratic_risk(v_raw)

    # Base Occupational Hazard (Current)
    h_base_current = get_h_base(job_title)

    # Systematic Risk
    h_i = calculate_systematic_risk(h_base_current, m_econ, iai)

    # Actuarial Calculations
    l_payout = calculate_l_payout(annual_salary, coverage_duration_months, coverage_percentage)
    p_systemic = calculate_p_systemic(h_i)
    p_individual_systemic = calculate_p_individual_systemic(v_i_t)
    p_claim = calculate_p_claim(p_systemic, p_individual_systemic)
    e_loss = calculate_e_loss(p_claim, l_payout)
    p_monthly = calculate_p_monthly(e_loss)

    # Store calculated values in session state for potential use by other pages
    st.session_state['current_job_h_base'] = h_base_current
    st.session_state['current_job_title'] = job_title


    # --- Output Display ---
    st.subheader("Your AI Risk Assessment Summary")

    col_res1, col_res2, col_res3 = st.columns(3)
    with col_res1:
        st.metric(label="Idiosyncratic Risk ($V_i(t)$)", value=f"{v_i_t:.2f}")
    with col_res2:
        st.metric(label="Systematic Risk ($H_i$)", value=f"{h_i:.2f}")
    with col_res3:
        st.metric(label="Estimated Monthly Premium ($P_{monthly}$)", value=f"${p_monthly:.2f}")

    st.info("Higher risk scores indicate greater vulnerability to AI-driven job displacement.")

    with st.expander("Detailed Calculation Breakdown"):
        st.markdown(r"**Idiosyncratic Risk ($V_i(t)$)** quantifies your personal vulnerability. It is calculated as:")
        st.latex(r"V_i(t) = \min(100.0, \max(5.0, V_{raw} - 50.0))")
        st.markdown(f"Your Raw Idiosyncratic Risk ($V_{raw}$): `{v_raw:.2f}`")
        st.markdown(f"Your Idiosyncratic Risk ($V_i(t)$): `{v_i_t:.2f}`")

        st.markdown(r"Where $V_{raw}$ combines the **Human Capital Factor ($FHC$)**, **Company Risk Factor ($FCR$)**, and **Upskilling Factor ($FUS$):**")
        st.latex(r"V_{raw} = FHC \cdot (w_{CR} FCR + w_{US} FUS)")
        st.markdown(f"- Human Capital Factor ($FHC$): `{fhc:.2f}`")
        st.markdown(f"- Company Risk Factor ($FCR$): `{fcr:.2f}`")
        st.markdown(f"- Upskilling Factor ($FUS$): `{fus:.2f}`")

        st.markdown(r"**Systematic Risk ($H_i$)** reflects the macro-level automation hazard of your occupation, adjusted by broader environmental conditions. It is calculated as:")
        st.latex(r"H_i = H_{base}(t) \cdot (w_{econ} M_{econ} + w_{inno} IAI)")
        st.markdown(f"Your Base Occupational Hazard ($H_{base}(t)$): `{h_base_current:.2f}`")
        st.markdown(f"Your Systematic Risk ($H_i$): `{h_i:.2f}`")

        st.markdown(r"**Insurance Premium Calculation**: The premium is derived from the **Annual Expected Loss ($E[Loss]$)**, which is the product of **Annual Claim Probability ($P_{claim}$)** and **Total Payout Amount ($L_{payout}$)**.")
        st.latex(r"E[Loss] = P_{claim} \cdot L_{payout}")
        st.latex(r"P_{monthly} = \max \left( rac{E[Loss] \cdot \lambda}{12}, P_{min} ight)")
        st.markdown(f"- Total Potential Payout Amount ($L_{payout}$): `${l_payout:.2f}`")
        st.markdown(f"- Annual Claim Probability ($P_{claim}$): `{p_claim:.4f}`")
        st.markdown(f"- Annual Expected Loss ($E[Loss]$): `${e_loss:.2f}`")
        st.markdown(f"- Monthly Insurance Premium ($P_{monthly}$): `${p_monthly:.2f}` (Loading Factor $\lambda={loading_factor}$, Minimum Premium $P_{min}=${min_premium})")
        st.markdown(r"Where $P_{claim} = P_{systemic} \cdot P_{individual|systemic}$, with:")
        st.markdown(f"- Probability of a systemic event ($P_{systemic}$): `{p_systemic:.4f}`")
        st.markdown(f"- Conditional probability of individual loss ($P_{individual|systemic}$): `{p_individual_systemic:.4f}`")

    st.subheader("Factor Impact Visualization (Idiosyncratic Risk)")
    st.plotly_chart(plot_factor_impact(fhc, fcr, fus))

