
import streamlit as st
import pandas as pd
import numpy as np
from data_utils import load_job_data, load_human_capital_factors, load_company_risk_factors, load_actuarial_parameters, load_weights
from calculations import (
    calculate_f_exp, calculate_fhc, calculate_fcr, calculate_fus,
    calculate_v_raw, calculate_idiosyncratic_risk, calculate_systematic_risk
)
from visualization import plot_risk_factor_contributions

def run_risk_profile_page():
    st.header("Risk Profile Assessment")
    st.markdown("This section helps you understand your current Idiosyncratic and Systematic AI Risk scores.")

    # Load data and parameters
    job_data = load_job_data()
    education_level_factors, education_field_factors, school_tier_factors = load_human_capital_factors()
    company_type_data = load_company_risk_factors()
    actuarial_params = load_actuarial_parameters()
    weights = load_weights()

    # --- User Input Collection ---
    st.subheader("Your Current Professional Profile")
    col1, col2 = st.columns(2)

    with col1:
        current_job_title = st.selectbox(
            "Job Title",
            options=job_data.index.tolist(),
            index=job_data.index.get_loc("Data Scientist")
        )
        years_experience = st.number_input(
            "Years of Experience",
            min_value=0, max_value=50, value=5, step=1,
            help="Your total years of professional experience."
        )
        education_level = st.selectbox(
            "Highest Education Level",
            options=list(education_level_factors.keys()),
            index=list(education_level_factors.keys()).index("Master's")
        )

    with col2:
        education_field = st.selectbox(
            "Education Field",
            options=list(education_field_factors.keys()),
            index=list(education_field_factors.keys()).index("Tech/Engineering")
        )
        school_tier = st.selectbox(
            "Institution Tier",
            options=list(school_tier_factors.keys()),
            index=list(school_tier_factors.keys()).index("Tier 2 (Reputable State/Private)")
        )
        company_type = st.selectbox(
            "Company Type",
            options=list(company_type_data.keys()),
            index=list(company_type_data.keys()).index("Mid-size firm (Growing)")
        )

    st.subheader("Upskilling Efforts")
    st.markdown("Indicate your progress in acquiring new skills:")
    col_upskill1, col_upskill2 = st.columns(2)
    with col_upskill1:
        p_gen_t = st.slider(
            "% General (Portable) Skill Training Completed",
            0, 100, 20, step=5,
            help="Progress in skills broadly applicable across industries (e.g., programming, project management)."
        ) / 100.0
    with col_upskill2:
        p_spec_t = st.slider(
            "% Firm-Specific Skill Training Completed",
            0, 100, 10, step=5,
            help="Progress in skills highly specific to your current company or its unique processes."
        ) / 100.0

    st.subheader("Environmental Modifiers (Systematic Risk)")
    st.markdown("Adjust these sliders to simulate different macroeconomic conditions and AI innovation paces, affecting your **Systematic Risk ($H_i$)**.")
    col_env1, col_env2 = st.columns(2)
    with col_env1:
        m_econ = st.slider(
            "Economic Climate ($M_{econ}$)",
            0.8, 1.2, 1.0, step=0.01,
            help="A composite index reflecting macroeconomic environment. 0.8 = Recession, 1.0 = Normal, 1.2 = Boom."
        )
    with col_env2:
        iai = st.slider(
            "AI Innovation Index ($IAI$)",
            0.8, 1.2, 1.0, step=0.01,
            help="A momentum indicator reflecting the velocity of technological change. 0.8 = Slowdown, 1.0 = Normal, 1.2 = Rapid Breakthrough."
        )

    # --- Calculations ---
    # Human Capital Factor (FHC)
    f_role = job_data.loc[current_job_title, 'f_role_multiplier']
    f_level = education_level_factors[education_level]
    f_field = education_field_factors[education_field]
    f_school = school_tier_factors[school_tier]
    f_exp = calculate_f_exp(years_experience, actuarial_params['decay_constant_a'], actuarial_params['years_cap_y'])
    fhc = calculate_fhc(f_role, f_level, f_field, f_school, f_exp)

    # Company Risk Factor (FCR)
    company_factors = company_type_data[company_type]
    s_senti = company_factors['S_senti']
    s_fin = company_factors['S_fin']
    s_growth = company_factors['S_growth']
    fcr = calculate_fcr(s_senti, s_fin, s_growth, weights['w1_fcr'], weights['w2_fcr'], weights['w3_fcr'])

    # Upskilling Factor (FUS)
    fus = calculate_fus(p_gen_t, p_spec_t, weights['gamma_gen'], weights['gamma_spec'])

    # Raw Idiosyncratic Risk (V_raw)
    v_raw = calculate_v_raw(fhc, fcr, fus, weights['w_cr'], weights['w_us'])

    # Idiosyncratic Risk (V_i(t))
    v_i_t = calculate_idiosyncratic_risk(v_raw)

    # Systematic Risk (H_i)
    h_base_t = job_data.loc[current_job_title, 'Base_AI_Hazard']
    h_i = calculate_systematic_risk(h_base_t, m_econ, iai, weights['w_econ'], weights['w_inno'])


    # Store calculated values in session state for other pages
    st.session_state['v_i_t'] = v_i_t
    st.session_state['h_i'] = h_i
    st.session_state['h_base_current'] = h_base_t # For transition simulation
    st.session_state['current_job_title'] = current_job_title # For transition simulation

    st.session_state['fhc'] = fhc
    st.session_state['fcr'] = fcr
    st.session_state['fus'] = fus
    st.session_state['m_econ'] = m_econ
    st.session_state['iai'] = iai

    # --- Output Display ---
    st.subheader("Your AI Risk Scores")
    col_metrics1, col_metrics2 = st.columns(2)
    with col_metrics1:
        st.metric(
            label="Idiosyncratic Risk ($V_i(t)$)",
            value=f"{v_i_t:.2f}",
            help="Your individual vulnerability to job displacement, reflecting factors within your direct control."
        )
    with col_metrics2:
        st.metric(
            label="Systematic Risk ($H_i$)",
            value=f"{h_i:.2f}",
            help="The macro-level automation hazard of your occupation, adjusted by broader environmental conditions."
        )

    st.markdown("---")

    # Explanations of core concepts and formulas
    st.subheader("Understanding Your Risk Scores")

    with st.expander("Idiosyncratic Risk ($V_i(t)$) Details"):
        st.markdown("The Idiosyncratic Risk, or Vulnerability, quantifies an individual's specific vulnerability to job displacement, reflecting factors within their direct control. It is calculated using:")
        st.latex(r"V_i(t) = \min(100.0, \max(5.0, V_{raw} - 50.0))")
        st.markdown(f'''Where:
        - $V_i(t)$: The final Idiosyncratic Risk score at time $t$.
        - $V_{raw}$: The raw (unnormalized) Idiosyncratic Risk score.

        **Current Calculated Value:** $V_i(t) = {v_i_t:.2f}
        ''')

        st.markdown("### Raw Idiosyncratic Risk ($V_{raw}$)")
        st.markdown("The raw Idiosyncratic Risk Score is an intermediate calculation before normalization, combining key individual-specific factors. It is calculated using:")
        st.latex(r"V_{raw} = FHC \cdot (w_{CR} FCR + w_{US} FUS)")
        st.markdown(f'''Where:
        - $V_{raw}$: Raw Idiosyncratic Risk Score.
        - $FHC$: Human Capital Factor ({fhc:.2f}).
        - $FCR$: Company Risk Factor ({fcr:.2f}).
        - $FUS$: Upskilling Factor ({fus:.2f}).
        - $w_{CR}$: Weight assigned to the Company Risk Factor ({weights['w_cr']:.2f}).
        - $w_{US}$: Weight assigned to the Upskilling Factor ({weights['w_us']:.2f}).

        **Current Calculated Value:** $V_{raw} = {v_raw:.2f}
        ''')

        st.markdown("### Human Capital Factor ($FHC$)")
        st.markdown("The Human Capital Factor assesses an individual's foundational resilience based on their educational and professional background. It is calculated as a weighted product of several sub-factors:")
        st.latex(r"FHC = f_{role} \cdot f_{level} \cdot f_{field} \cdot f_{school} \cdot f_{exp}")
        st.markdown(f'''Where:
        - $FHC$: Human Capital Factor ({fhc:.2f}).
        - $f_{role}$: Role Multiplier ({f_role:.2f}, from '{current_job_title}').
        - $f_{level}$: Education Level Factor ({f_level:.2f}, from '{education_level}').
        - $f_{field}$: Education Field Factor ({f_field:.2f}, from '{education_field}').
        - $f_{school}$: Institution Tier Factor ({f_school:.2f}, from '{school_tier}').
        - $f_{exp}$: Experience Factor ({f_exp:.2f}).

        **Current Calculated Value:** $FHC = {fhc:.2f}
        ''')

        st.markdown("### Experience Factor ($f_{exp}$)")
        st.markdown("The Experience Factor models how an individual's years of professional experience influence their vulnerability, accounting for diminishing returns. It is calculated using:")
        st.latex(r"f_{exp} = 1 - (a \cdot \min(Y_i, Y_{cap}))")
        st.markdown(f'''Where:
        - $f_{exp}$: Experience Factor ({f_exp:.2f}).
        - $a$: Decay constant ({actuarial_params['decay_constant_a']:.3f}).
        - $Y_i$: Years of experience of the individual ({years_experience}).
        - $Y_{cap}$: Capped years of experience ({actuarial_params['years_cap_y']}).

        **Current Calculated Value:** $f_{exp} = {f_exp:.2f}
        ''')

        st.markdown("### Company Risk Factor ($FCR$)")
        st.markdown("The Company Risk Factor quantifies the stability and growth prospects of the individual's current employer. It is calculated using:")
        st.latex(r"FCR = w_1 \cdot S_{senti} + w_2 \cdot S_{fin} + w_3 \cdot S_{growth}")
        st.markdown(f'''Where:
        - $FCR$: Company Risk Factor ({fcr:.2f}).
        - $S_{senti}$: Sentiment Score ({s_senti:.2f}).
        - $S_{fin}$: Financial Health Score ({s_fin:.2f}).
        - $S_{growth}$: Growth & AI-Adoption Score ({s_growth:.2f}).
        - $w_1, w_2, w_3$: Weights ({weights['w1_fcr']:.2f}, {weights['w2_fcr']:.2f}, {weights['w3_fcr']:.2f}).

        **Current Calculated Value:** $FCR = {fcr:.2f}
        ''')

        st.markdown("### Upskilling Factor ($FUS$)")
        st.markdown("The Upskilling Factor differentiates between skill types, rewarding portable skills more heavily, and reflects the impact of an individual's proactive training efforts. It is calculated using:")
        st.latex(r"FUS = 1 - (\gamma_{gen} P_{gen}(t) + \gamma_{spec} P_{spec}(t))")
        st.markdown(f'''Where:
        - $FUS$: Upskilling Factor ({fus:.2f}).
        - $P_{gen}(t)$: General skill training progress ({p_gen_t:.2f}).
        - $P_{spec}(t)$: Firm-specific skill training progress ({p_spec_t:.2f}).
        - $\gamma_{gen}$: Weight for general skills ({weights['gamma_gen']:.2f}).
        - $\gamma_{spec}$: Weight for firm-specific skills ({weights['gamma_spec']:.2f}).

        **Current Calculated Value:** $FUS = {fus:.2f}
        ''')

        # Bar chart for Idiosyncratic Risk factors
        idiosyncratic_factors = {
            'Human Capital Factor (FHC)': fhc,
            'Company Risk Factor (FCR)': fcr,
            'Upskilling Factor (FUS)': fus
        }
        fig_id, _ = plot_risk_factor_contributions(idiosyncratic_factors, {}) # Pass empty for systematic for now
        st.plotly_chart(fig_id, use_container_width=True)


    with st.expander("Systematic Risk ($H_i$) Details"):
        st.markdown("The Systematic Risk score is a dynamic index reflecting the macro-level automation hazard of an occupation, adjusted by broader environmental conditions. It is calculated using:")
        st.latex(r"H_i = H_{base}(t) \cdot (w_{econ} M_{econ} + w_{inno} IAI)")
        st.markdown(f'''Where:
        - $H_i$: The final Systematic Risk score at time $t$ ({h_i:.2f}).
        - $H_{base}(t)$: The Base Occupational Hazard for '{current_job_title}' ({h_base_t:.2f}).
        - $M_{econ}$: Economic Climate Modifier ({m_econ:.2f}).
        - $IAI$: AI Innovation Index ({iai:.2f}).
        - $w_{econ}$: Calibration weight for economic modifier ({weights['w_econ']:.2f}).
        - $w_{inno}$: Calibration weight for AI innovation index ({weights['w_inno']:.2f}).

        **Current Calculated Value:** $H_i = {h_i:.2f}
        ''')

        # Bar chart for Systematic Risk factors
        # The contribution of M_econ and IAI is their value multiplied by their weights.
        # H_base is a direct base hazard.
        systematic_factors_contrib = {
            'Base Occupational Hazard (H_base)': h_base_t,
            f'Economic Climate (M_econ) * {weights["w_econ"]:.2f}': m_econ * weights['w_econ'] * 100, # Scale for visualization
            f'AI Innovation Index (IAI) * {weights["w_inno"]:.2f}': iai * weights['w_inno'] * 100 # Scale for visualization
        }
        # The plot_risk_factor_contributions function expects factors and values.
        # We'll pass the base hazard directly and the weighted modifiers.
        _, fig_sys = plot_risk_factor_contributions({}, systematic_factors_contrib)
        st.plotly_chart(fig_sys, use_container_width=True)
