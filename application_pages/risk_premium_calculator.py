
import streamlit as st
import pandas as pd
from application_pages.calculations import (
    calculate_fhc, calculate_fcr, calculate_fus, calculate_v_raw,
    calculate_idiosyncratic_risk, calculate_systematic_risk,
    calculate_l_payout, calculate_p_systemic, calculate_p_individual_systemic,
    calculate_p_claim, calculate_e_loss, calculate_p_monthly,
    get_h_base_for_job_title
)
from application_pages.data_utils import (
    load_job_data, load_education_data, load_school_tier_data,
    load_company_type_data, load_default_parameters
)
from application_pages.visualization import plot_factor_impact_bar_chart

def run_risk_premium_calculator():
    st.header("Risk & Premium Calculator")
    st.markdown("""
    This section allows you to input your career details, upskilling progress, and financial
    parameters to calculate your Idiosyncratic Risk, Systematic Risk, and estimated Monthly Insurance Premium.
    """)

    job_data = load_job_data()
    education_level_data, education_field_data = load_education_data()
    school_tier_data = load_school_tier_data()
    company_type_data = load_company_type_data()
    default_params = load_default_parameters()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("1. Current Profile")
        job_title = st.selectbox(
            "Job Title",
            options=job_data['Job Title'].tolist(),
            index=job_data['Job Title'].tolist().index('Software Engineer') if 'Software Engineer' in job_data['Job Title'].tolist() else 0,
            help="Select your current job role. This influences your base occupational hazard."
        )
        years_experience = st.number_input(
            "Years of Experience",
            min_value=0, max_value=50, value=5,
            help="Your total years of professional experience. More experience generally reduces idiosyncratic risk."
        )
        education_level = st.selectbox(
            "Highest Education Level",
            options=list(education_level_data.keys()),
            index=list(education_level_data.keys()).index('Bachelor\'s') if 'Bachelor\'s' in education_level_data.keys() else 0,
            help="Your highest educational attainment. Higher education levels can reduce idiosyncratic risk."
        )
        education_field = st.selectbox(
            "Education Field",
            options=list(education_field_data.keys()),
            index=list(education_field_data.keys()).index('Tech/Engineering') if 'Tech/Engineering' in education_field_data.keys() else 0,
            help="The field of your education. Fields with in-demand or transferable skills can reduce risk."
        )
        school_tier = st.selectbox(
            "Institution Tier",
            options=list(school_tier_data.keys()),
            index=list(school_tier_data.keys()).index('Tier 2 (Top 25%)') if 'Tier 2 (Top 25%)' in school_tier_data.keys() else 0,
            help="The tier of your educational institution, a proxy for training quality."
        )
        company_type = st.selectbox(
            "Company Type",
            options=list(company_type_data.keys()),
            index=list(company_type_data.keys()).index('Big Firm (Stable)') if 'Big Firm (Stable)' in company_type_data.keys() else 0,
            help="The type of company you work for, influencing company risk."
        )

    with col2:
        st.subheader("2. Upskilling Efforts")
        p_gen_t = st.slider(
            "% General Skill Training Completed",
            min_value=0, max_value=100, value=0,
            help="Progress in general, portable skills (e.g., coding, project management)."
        )
        p_spec_t = st.slider(
            "% Firm-Specific Skill Training Completed",
            min_value=0, max_value=100, value=0,
            help="Progress in skills specific to your current firm or tools."
        )

        st.subheader("3. Environmental Modifiers")
        m_econ = st.slider(
            "Economic Climate Modifier ($M_{econ}$)",
            min_value=0.8, max_value=1.2, value=1.0, step=0.01,
            help="Reflects the overall macroeconomic environment (e.g., 0.8 for recession, 1.2 for boom)."
        )
        iai = st.slider(
            "AI Innovation Index ($IAI$)",
            min_value=0.8, max_value=1.2, value=1.0, step=0.01,
            help="Reflects the velocity of technological change in AI (e.g., 0.8 for slowdown, 1.2 for rapid breakthrough)."
        )

        st.subheader("4. Actuarial Parameters")
        annual_salary = st.number_input(
            "Annual Salary ($)",
            min_value=0, value=90000, step=1000,
            help="Your current annual salary, used to calculate potential payout."
        )
        coverage_percentage = st.slider(
            "Coverage Percentage (%)",
            min_value=0, max_value=100, value=25,
            help="Percentage of your salary to be covered in case of a claim."
        )
        coverage_duration_months = st.number_input(
            "Coverage Duration (Months)",
            min_value=1, value=6, step=1,
            help="Duration for which the payout would be made (e.g., 6 months of salary)."
        )
        loading_factor = st.number_input(
            "Loading Factor ($\lambda$)",
            min_value=1.0, max_value=5.0, value=default_params['lambda_loading'], step=0.01,
            help="An insurance multiplier to cover administrative costs and profit margin."
        )
        minimum_premium = st.number_input(
            "Minimum Monthly Premium ($P_{min}$)",
            min_value=0.0, value=default_params['P_min'], step=0.1,
            help="The minimum monthly premium charged to ensure policy viability."
        )

    st.divider()
    st.subheader("Calculated Risk Scores & Premium")

    # --- Calculations ---
    # FHC
    fhc = calculate_fhc(job_title, education_level, education_field, school_tier, years_experience)
    # FCR
    fcr = calculate_fcr(company_type)
    # FUS
    fus = calculate_fus(p_gen_t, p_spec_t)
    # V_raw
    v_raw = calculate_v_raw(fhc, fcr, fus)
    # V_i(t)
    v_i_t = calculate_idiosyncratic_risk(v_raw)

    # H_base(t) (current job)
    h_base_current_job = get_h_base_for_job_title(job_title)
    # H_i
    h_i = calculate_systematic_risk(h_base_current_job, m_econ, iai)

    # L_payout
    l_payout = calculate_l_payout(annual_salary, coverage_duration_months, coverage_percentage)

    # P_systemic
    p_systemic = calculate_p_systemic(h_i)
    # P_individual|systemic
    p_individual_systemic = calculate_p_individual_systemic(v_i_t)
    # P_claim
    p_claim = calculate_p_claim(p_systemic, p_individual_systemic)

    # E[Loss]
    e_loss = calculate_e_loss(p_claim, l_payout)

    # P_monthly
    # Temporarily override lambda_loading and P_min with user inputs for this calculation
    st.session_state['lambda_loading_override'] = loading_factor
    st.session_state['P_min_override'] = minimum_premium
    P_monthly = max((e_loss * st.session_state['lambda_loading_override']) / 12.0, st.session_state['P_min_override'])

    # Display Results
    results_col1, results_col2, results_col3 = st.columns(3)
    with results_col1:
        st.metric(label="Idiosyncratic Risk ($V_i(t)$)", value=f"{v_i_t:.2f}")
        st.caption("Your personal vulnerability to job displacement.")
    with results_col2:
        st.metric(label="Systematic Risk ($H_i$)", value=f"{h_i:.2f}")
        st.caption("Macro-level automation hazard for your occupation/industry.")
    with results_col3:
        st.metric(label="Monthly Premium ($P_{monthly}$)", value=f"${P_monthly:.2f}")
        st.caption("Estimated monthly insurance premium based on your risk profile.")

    st.markdown("---")
    st.subheader("Intermediate Calculations & Explanations")

    with st.expander("Idiosyncratic Risk Components"):
        st.markdown(r"""
**Idiosyncratic Risk ($V_i(t)$)** quantifies an individual's specific vulnerability to job displacement,
reflecting factors within their direct control.
$$
V_i(t) = \min(100.0, \max(5.0, V_{raw} - 50.0))
$$
Where:
-   $V_i(t)$: The final Idiosyncratic Risk score at time $t$.
-   $V_{raw}$: The raw (unnormalized) Idiosyncratic Risk score.
""")
        st.info(f"Raw Idiosyncratic Risk ($V_{{raw}}$): {v_raw:.2f}")
        st.info(f"Calculated Idiosyncratic Risk ($V_i(t)$): {v_i_t:.2f}")

        st.markdown(r"""
**Raw Idiosyncratic Risk ($V_{raw}$)** is an intermediate calculation combining key individual-specific factors.
$$
V_{raw} = FHC \cdot (w_{CR} FCR + w_{US} FUS)
$$
Where:
-   $FHC$: Human Capital Factor, assessing foundational resilience.
-   $FCR$: Company Risk Factor, assessing employer stability.
-   $FUS$: Upskilling Factor, assessing proactive training efforts.
-   $w_{CR}$: Weight assigned to the Company Risk Factor (default: 0.4).
-   $w_{US}$: Weight assigned to the Upskilling Factor (default: 0.6).
""")

        st.info(f"Human Capital Factor ($FHC$): {fhc:.2f}")
        st.info(f"Company Risk Factor ($FCR$): {fcr:.2f}")
        st.info(f"Upskilling Factor ($FUS$): {fus:.2f}")

        fig_idiosyncratic, _ = plot_factor_impact_bar_chart(fhc, fcr, fus, h_base_current_job, m_econ, iai)
        st.plotly_chart(fig_idiosyncratic)

        st.markdown(r"""
**Human Capital Factor ($FHC$)**: Assesses an individual's foundational resilience.
$$
FHC = f_{role} \cdot f_{level} \cdot f_{field} \cdot f_{school} \cdot f_{exp}
$$
The Experience Factor ($f_{exp}$) is calculated as:
$$
f_{exp} = 1 - (a \cdot \min(Y_i, Y_{cap}))
$$
Where $a$ is decay constant ({default_params['a_decay']}), $Y_i$ is years of experience ({years_experience}), and $Y_{cap}$ is capped years ({default_params['Y_cap']}).
""".format(default_params=default_params, years_experience=years_experience))

        st.markdown(r"""
**Company Risk Factor ($FCR$)**: Quantifies the stability and growth prospects of the employer.
For simplicity in this synthetic model, $FCR$ is directly derived from the company type.
$$
FCR = w_1 \cdot S_{senti} + w_2 \cdot S_{fin} + w_3 \cdot S_{growth} \quad (\text{simplified for synthetic data})
$$
""")

        st.markdown(r"""
**Upskilling Factor ($FUS$)**: Reflects the impact of proactive training efforts.
$$
FUS = 1 - (\gamma_{gen} P_{gen}(t) + \gamma_{spec} P_{spec}(t))
$$
Where $\gamma_{gen}$ is weight for general skills ({default_params['gamma_gen']}) and $\gamma_{spec}$ is for firm-specific skills ({default_params['gamma_spec']}).
""".format(default_params=default_params))

    with st.expander("Systematic Risk Components"):
        st.markdown(r"""
**Systematic Risk ($H_i$)** is a dynamic index reflecting the macro-level automation hazard of an occupation,
adjusted by broader environmental conditions.
$$
H_i = H_{base}(t) \cdot (w_{econ} M_{econ} + w_{inno} IAI)
$$
Where:
-   $H_{base}(t)$: The Base Occupational Hazard for the occupation ({h_base_current_job}).
-   $M_{econ}$: Economic Climate Modifier ({m_econ}).
-   $IAI$: AI Innovation Index ({iai}).
-   $w_{econ}$: Calibration weight for economic modifier ({default_params['w_econ']}).
-   $w_{inno}$: Calibration weight for AI innovation index ({default_params['w_inno']}).
""".format(h_base_current_job=h_base_current_job, m_econ=m_econ, iai=iai, default_params=default_params))
        st.info(f"Base Occupational Hazard ($H_{{base}}$): {h_base_current_job:.2f}")
        st.info(f"Calculated Systematic Risk ($H_i$): {h_i:.2f}")

        _, fig_systematic = plot_factor_impact_bar_chart(fhc, fcr, fus, h_base_current_job, m_econ, iai)
        st.plotly_chart(fig_systematic)

    with st.expander("Premium Calculation Details"):
        st.markdown(r"""
**Total Payout Amount ($L_{payout}$)**: The financial benefit defined by the policy.
$$
L_{payout} = \left( \frac{\text{Annual Salary}}{12} \right) \cdot \text{Coverage Duration} \cdot \text{Coverage Percentage}
$$
""")
        st.info(f"Total Payout Amount ($L_{{payout}}$): ${l_payout:.2f}")

        st.markdown(r"""
**Annual Claim Probability ($P_{claim}$)**: Joint probability of a systemic event and individual loss.
$$
P_{claim} = P_{systemic} \cdot P_{individual|systemic}
$$
-   **Systemic Event Base Probability ($P_{systemic}$)**:
    $$
    P_{systemic} = \frac{H_i}{100} \cdot \beta_{systemic}
    $$
    ($\beta_{systemic}$ = {default_params['beta_systemic']})
-   **Individual Loss Base Probability ($P_{individual|systemic}$)**:
    $$
    P_{individual|systemic} = \frac{V_i(t)}{100} \cdot \beta_{individual}
    $$
    ($\beta_{individual}$ = {default_params['beta_individual']})
""".format(default_params=default_params))
        st.info(f"Systemic Event Probability ($P_{{systemic}}$): {p_systemic:.4f}")
        st.info(f"Individual Loss Probability given Systemic Event ($P_{{individual|systemic}}$): {p_individual_systemic:.4f}")
        st.info(f"Annual Claim Probability ($P_{{claim}}$): {p_claim:.4f}")

        st.markdown(r"""
**Annual Expected Loss ($E[Loss]$)**: Total payout multiplied by claim probability.
$$
E[Loss] = P_{claim} \cdot L_{payout}
$$
""")
        st.info(f"Annual Expected Loss ($E[Loss]$): ${e_loss:.2f}")

        st.markdown(r"""
**Monthly Insurance Premium ($P_{monthly}$)**: Final financial output.
$$
P_{monthly} = \max \left( \frac{E[Loss] \cdot \lambda}{12}, P_{min} \right)
$$
Where $\lambda$ is Loading Factor ({loading_factor}) and $P_{min}$ is Minimum Monthly Premium (${minimum_premium:.2f}).
""".format(loading_factor=loading_factor, minimum_premium=minimum_premium))
        st.info(f"Monthly Insurance Premium ($P_{{monthly}}$): ${P_monthly:.2f}")

    # Ensure st.session_state is reset or managed properly if these overrides are not desired globally
    # In a real app, these parameters would typically be passed directly to the function
    # rather than modifying default_params in session_state, but for simplicity we keep it here.
    if 'lambda_loading_override' in st.session_state:
        del st.session_state['lambda_loading_override']
    if 'P_min_override' in st.session_state:
        del st.session_state['P_min_override']
