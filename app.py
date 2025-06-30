import streamlit as st
import pandas as pd
from data_utils import load_job_data, load_education_data, load_school_tier_data, load_company_type_data, load_default_actuarial_parameters
from calculations import (
    calculate_fhc, calculate_fcr, calculate_fus, calculate_v_raw,
    calculate_idiosyncratic_risk, calculate_h_base_ttv, calculate_systematic_risk,
    calculate_p_systemic, calculate_p_individual_systemic, calculate_p_claim,
    calculate_l_payout, calculate_expected_loss, calculate_monthly_premium,
    get_h_base_for_job
)
from visualization import plot_systematic_risk_evolution, plot_factor_contributions_v_raw, plot_factor_contributions_hi

st.set_page_config(page_title="QuLab - AI Risk Score - V4-2", layout="wide")
st.sidebar.image("https://www.quantuniversity.com/assets/img/logo5.jpg")
st.sidebar.divider()
st.title("AI Risk Score - V4-2")

st.markdown("""
In this lab, the **AI Risk Score - V4-2: Career Path Diversification Tool** is designed to help users understand
and mitigate their exposure to systematic AI risk in their careers. Inspired by the principles of risk management,
this application allows you to explore how different career choices and personal development efforts
influence your AI displacement risk profile and potential insurance premiums.

### Understanding AI Displacement Risk
AI displacement risk can be broadly categorized into two types:

1.  **Idiosyncratic Risk ($V_i(t)$):** This refers to individual-specific vulnerabilities that are largely within
    your control. Factors like your skills, education, experience, and even your current employer's stability
    contribute to this risk. Proactive measures, such as continuous learning and skill diversification,
    can effectively mitigate idiosyncratic risk.

2.  **Systematic Risk ($H_i$):** This represents the macro-level automation hazard inherent to an entire occupation
    or industry. It's influenced by broader environmental conditions like the economic climate and the pace of AI
    innovation. While harder to control directly, systematic risk can be managed through **Career Path Diversification**,
    i.e., strategically transitioning to roles or industries with lower inherent AI hazard.

### How This Tool Helps
This application simulates the impact of various inputs on your risk scores and a hypothetical insurance premium
designed to cover potential income loss due to AI-driven job displacement. By interacting with the inputs,
you can gain a clear understanding of:

*   How individual factors (Human Capital, Company Stability, Upskilling) shape your Idiosyncratic Risk.
*   How external factors (Economic Climate, AI Innovation) influence your Systematic Risk.
*   The financial implications (potential insurance premium) of your risk profile.
*   The power of **Career Path Diversification** in reducing systematic risk over time, demonstrated through
    the "Time-to-Value (TTV)" simulation.

Let's explore how your career path, skills, and strategic choices can act as a form of "insurance" against AI risk.
""")

st.divider()

# Load all data and parameters once and store in session state
if 'job_data' not in st.session_state:
    st.session_state.job_data = load_job_data()
    st.session_state.education_level_data, st.session_state.education_field_data = load_education_data()
    st.session_state.school_tier_data = load_school_tier_data()
    st.session_state.company_type_data = load_company_type_data()
    st.session_state.params = load_default_actuarial_parameters()

job_data = st.session_state.job_data
education_level_data = st.session_state.education_level_data
education_field_data = st.session_state.education_field_data
school_tier_data = st.session_state.school_tier_data
company_type_data = st.session_state.company_type_data
params = st.session_state.params

# Sidebar for Inputs
st.sidebar.header("Your Profile & Inputs")

with st.sidebar.expander("1. Current Profile"):
    job_titles = job_data["Job Title"].tolist()
    selected_job_title = st.selectbox("Job Title", job_titles, index=job_titles.index("Software Engineer"))
    
    years_experience = st.number_input("Years of Experience", min_value=0, max_value=50, value=5)
    
    education_levels = list(education_level_data.keys())
    selected_education_level = st.selectbox("Education Level", education_levels, index=education_levels.index("Bachelor's"))
    
    education_fields = list(education_field_data.keys())
    selected_education_field = st.selectbox("Education Field", education_fields, index=education_fields.index("Tech/Engineering"))
    
    school_tiers = list(school_tier_data.keys())
    selected_school_tier = st.selectbox("Institution Tier", school_tiers, index=school_tiers.index("Tier 2 (Top 50)"))
    
    company_types = company_type_data["Company Type"].tolist()
    selected_company_type = st.selectbox("Company Type", company_types, index=company_types.index("Big firm"))

with st.sidebar.expander("2. Upskilling Efforts"):
    gen_skill_progress = st.slider("% General Skill Training Completed", 0, 100, 30)
    firm_skill_progress = st.slider("% Firm-Specific Skill Training Completed", 0, 100, 10)

with st.sidebar.expander("3. Career Transition Simulation"):
    simulate_transition = st.checkbox("Simulate Career Transition")
    
    if simulate_transition:
        target_career_paths = job_data["Job Title"].tolist()
        # Filter out current job from target options for clarity if desired, or allow
        # target_career_paths = [job for job in job_titles if job != selected_job_title]
        default_target_index = target_career_paths.index("Nurse") if "Nurse" in target_career_paths else 0
        selected_target_career_path = st.selectbox("Target Career Path (Industry/Job)", target_career_paths, index=default_target_index)
        
        ttv_months = st.number_input("Transition Time-to-Value (TTV) in Months", value=params["ttv_default"], min_value=1, max_value=60)
        months_elapsed = st.slider("Months Elapsed Since Transition Started ($k$)", 0, ttv_months, 0)
    else:
        selected_target_career_path = selected_job_title # No transition, target is current
        ttv_months = params["ttv_default"] # Default value, not used if not simulating
        months_elapsed = 0 # Not used if not simulating

with st.sidebar.expander("4. Actuarial Parameters"):
    annual_salary = st.number_input("Annual Salary ($)", value=90000, min_value=0, step=1000)
    coverage_percentage = st.slider("Coverage Percentage (%)", 0, 100, 25)
    coverage_duration_months = st.number_input("Coverage Duration (Months)", value=6, min_value=1, max_value=24)
    
    loading_factor = st.number_input("Loading Factor ($\lambda$)", value=params["loading_factor"], min_value=1.0, step=0.1)
    min_premium = st.number_input("Minimum Monthly Premium ($P_{min}$)", value=params["min_premium"], min_value=0.0, step=1.0)

with st.sidebar.expander("5. Environmental Modifiers"):
    econ_modifier = st.slider("Economic Climate Modifier ($M_{econ}$)", 0.8, 1.2, 1.0, step=0.01,
                              help="0.8 = Recession, 1.0 = Normal, 1.2 = Boom")
    iai_index = st.slider("AI Innovation Index ($IAI$)", 0.8, 1.2, 1.0, step=0.01,
                          help="0.8 = Slowdown, 1.0 = Normal, 1.2 = Rapid Breakthrough")

st.header("Risk Assessment Results")

# --- Calculations ---
# Idiosyncratic Risk Factors
fhc = calculate_fhc(selected_job_title, selected_education_level, selected_education_field, selected_school_tier, years_experience)
fcr = calculate_fcr(selected_company_type)
fus = calculate_fus(gen_skill_progress, firm_skill_progress)
v_raw = calculate_v_raw(fhc, fcr, fus)
idiosyncratic_risk_score = calculate_idiosyncratic_risk(v_raw)

# Systematic Risk
current_h_base = get_h_base_for_job(selected_job_title)
target_h_base = get_h_base_for_job(selected_target_career_path)

if simulate_transition:
    h_base_t = calculate_h_base_ttv(months_elapsed, ttv_months, current_h_base, target_h_base)
else:
    h_base_t = current_h_base # No transition, use current H_base

systematic_risk_score = calculate_systematic_risk(h_base_t, econ_modifier, iai_index)

# Insurance Premium Calculations
l_payout = calculate_l_payout(annual_salary, coverage_duration_months, coverage_percentage)
p_systemic = calculate_p_systemic(systematic_risk_score)
p_individual_systemic = calculate_p_individual_systemic(idiosyncratic_risk_score)
p_claim = calculate_p_claim(p_systemic, p_individual_systemic)
expected_loss = calculate_expected_loss(p_claim, l_payout)
monthly_premium = calculate_monthly_premium(expected_loss)


# --- Output Display ---
st.subheader("Your AI Displacement Risk Profile")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Idiosyncratic Risk ($V_i(t)$)", value=f"{idiosyncratic_risk_score:.2f}")
    st.info(f"**Your controllable risk.** Lower is better. Calculated based on your Human Capital, Company Risk, and Upskilling efforts.")
with col2:
    st.metric(label="Systematic Risk ($H_i$)", value=f"{systematic_risk_score:.2f}")
    st.info(f"**Inherent job/industry risk.** Lower is better. Influenced by your job's base hazard, economic climate, and AI innovation pace.")
with col3:
    st.metric(label="Estimated Monthly Premium ($P_{monthly}$)", value=f"${monthly_premium:.2f}")
    st.info(f"**Cost of 'AI Insurance'.** Lower is better. Reflects the financial quantification of your combined risk.")

st.divider()

tab1, tab2, tab3 = st.tabs(["Detailed Risk Factors", "Actuarial Breakdown", "Career Transition Simulation"])

with tab1:
    st.subheader("Deep Dive: Risk Factor Contributions")
    st.markdown("Understanding how each component contributes to your overall risk helps in identifying areas for improvement.")

    st.markdown("""
    #### Idiosyncratic Risk ($V_i(t)$) Components
    Your Idiosyncratic Risk is influenced by:
    - **Human Capital Factor ($FHC$):** Your foundational resilience (education, experience, institution).
    - **Company Risk Factor ($FCR$):** Your employer's stability and AI adoption.
    - **Upskilling Factor ($FUS$):** Your proactive efforts in general and firm-specific training.
    
    The raw idiosyncratic risk score is given by:
    $$
    V_{raw} = FHC \cdot (w_{CR} FCR + w_{US} FUS)
    $$
    And then normalized to $V_i(t) = \min(100.0, \max(5.0, V_{raw} - 50.0))$.
    """)
    st.write(f"**Human Capital Factor ($FHC$):** `{fhc:.3f}`")
    st.write(f"**Company Risk Factor ($FCR$):** `{fcr:.3f}`")
    st.write(f"**Upskilling Factor ($FUS$):** `{fus:.3f}`")
    st.write(r"**Raw Idiosyncratic Risk ($V_{raw}$):**"\
        f"`{v_raw:.2f}`")

    # Plot contributions for V_raw (simplified as bar chart showing FHC, and the two weighted components)
    st.plotly_chart(plot_factor_contributions_v_raw(fhc, fcr, fus, params["w_CR"], params["w_US"]))

    st.markdown(r"""
    #### Systematic Risk ($H_i$) Components
    Your Systematic Risk is influenced by:
    - **Base Occupational Hazard ($H_{base}$):** Inherent risk of your job role.
    - **Economic Climate Modifier ($M_{econ}$):** Macroeconomic conditions.
    - **AI Innovation Index ($IAI$):** Pace of technological change.

    The formula for Systematic Risk is:
    $$
    H_i = H_{base}(t) \cdot (w_{econ} M_{econ} + w_{inno} IAI)
    $$
    """)
    st.write(r"**Base Occupational Hazard ($H_{base}(t)$):**"\
        f"`{current_h_base:.2f}` (Current Job)")
    st.write(r"**Economic Climate Modifier ($M_{econ}$):** "\
        f"`{econ_modifier:.2f}`")
    st.write(f"**AI Innovation Index ($IAI$):** `{iai_index:.2f}`")

    st.plotly_chart(plot_factor_contributions_hi(current_h_base, econ_modifier, iai_index, params["w_econ"], params["w_inno"]))

with tab2:
    st.subheader("Actuarial Breakdown: From Risk to Premium")
    st.markdown("This section details how your risk scores are translated into a potential monthly insurance premium.")

    st.markdown(r"#### Total Payout Amount ($L_{payout}$)")
    st.latex("L_{payout} = \\left( \\frac{\\text{Annual Salary}}{12} \\right) \\cdot \\text{Coverage Duration} \\cdot \\text{Coverage Percentage}")
    st.write(f"The total potential payout if a claim is triggered: **${l_payout:,.2f}**")

    st.markdown(r"""
    #### Annual Claim Probability ($P_{claim}$)
    This is the likelihood of a job displacement claim in a year, calculated as the joint probability of a systemic event and an individual loss given that event.
    $$
    P_{claim} = P_{systemic} \cdot P_{individual|systemic}
    $$
    """)
    st.latex("P_{systemic} = \\frac{H_i}{100} \\cdot \\beta_{systemic}")
    st.latex("P_{individual|systemic} = \\frac{V_i(t)}{100} \\cdot \\beta_{individual}")
    
    st.write(r"Probability of a Systemic Event ($P_{systemic}$):"\
        f"**{p_systemic:.4f}**")
    st.write(r"Conditional Probability of Individual Loss ($P_{individual|systemic}$):"\
        f"**{p_individual_systemic:.4f}**")
    st.write(r"Annual Claim Probability ($P_{claim}$):"\
        f"**{p_claim:.4f}**")

    st.markdown(r"#### Annual Expected Loss ($E[Loss]$)")
    st.latex("E[Loss] = P_{claim} \\cdot L_{payout}")
    st.write(f"The expected financial loss per year: **${expected_loss:,.2f}**")

    st.markdown(r"#### Monthly Insurance Premium ($P_{monthly}$)")
    st.latex("P_{monthly} = \\max \\left( \\frac{E[Loss] \\cdot \\lambda}{12}, P_{min} \\right)")
    st.write(f"Your final estimated monthly premium: **${monthly_premium:,.2f}**")


with tab3:
    st.subheader("Simulate Career Path Diversification")
    st.markdown(r"""
    This simulation illustrates how **Career Path Diversification** can mitigate your Systematic Risk over time.
    By transitioning to a target career path with a lower inherent AI hazard ($H_{target}$), your overall systematic risk
    gradually reduces over a defined **Time-to-Value (TTV)** period.
    """)
    st.latex("H_{base}(k) = \\left(1 - \\frac{k}{TTV}\\right) H_{current} + \\left(\\frac{k}{TTV}\\right) H_{target}")
    st.markdown(r"**Current Job Base Hazard ($H_{current}$):** "\
        f"`{current_h_base:.2f}` ({selected_job_title})")

    if simulate_transition:
        st.markdown(r"**Target Job Base Hazard ($H_{target}$):** "\
            f"`{target_h_base:.2f}` ({selected_target_career_path})")
        st.markdown(f"**Transition Time-to-Value (TTV):** `{ttv_months}` months")

        # Generate data for the plot
        simulation_months = list(range(ttv_months + 1))
        simulated_h_values = []
        for k_val in simulation_months:
            h_base_at_k = calculate_h_base_ttv(k_val, ttv_months, current_h_base, target_h_base)
            simulated_h = calculate_systematic_risk(h_base_at_k, econ_modifier, iai_index)
            simulated_h_values.append(simulated_h)
        
        simulation_df = pd.DataFrame({
            "Month": simulation_months,
            "Systematic Risk": simulated_h_values
        })
        
        st.plotly_chart(plot_systematic_risk_evolution(simulation_df))
        st.markdown(f"""
        As the "Months Since Transition Started" slider advances, you can observe the projected
        decrease in Systematic Risk ($H_i$) as your career path shifts from '{selected_job_title}'
        to '{selected_target_career_path}'. This demonstrates the value of **re-skilling and career diversification**
        as a proactive strategy against AI-driven job displacement.
        """)
    else:
        st.info("Check the 'Simulate Career Transition' box in the sidebar to see how diversifying your career path can reduce systematic risk.")

st.divider()
st.write("© 2025 QuantUniversity. All Rights Reserved.")
st.caption("The purpose of this demonstration is solely for educational use and illustration. "
           "Any reproduction of this demonstration "
           "requires prior written consent from QuantUniversity. "
           "This lab was generated using the QuCreate platform. QuCreate relies on AI models for generating code, which may contain inaccuracies or errors.")