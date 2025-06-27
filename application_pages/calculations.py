
import numpy as np
import pandas as pd
from application_pages.data_utils import load_default_parameters, load_job_data, load_education_data, load_school_tier_data, load_company_type_data

# Load static data and parameters once
DEFAULT_PARAMS = load_default_parameters()
JOB_DATA = load_job_data()
EDUCATION_LEVEL_DATA, EDUCATION_FIELD_DATA = load_education_data()
SCHOOL_TIER_DATA = load_school_tier_data()
COMPANY_TYPE_DATA = load_company_type_data()

def calculate_f_exp(years_experience):
    """
    Calculates the Experience Factor (f_exp).
    f_exp = 1 - (a * min(Y_i, Y_cap))
    """
    a = DEFAULT_PARAMS['a_decay']
    Y_cap = DEFAULT_PARAMS['Y_cap']
    f_exp = 1 - (a * min(years_experience, Y_cap))
    return max(0.0, f_exp) # Ensure f_exp doesn't go negative

def calculate_fhc(job_title, education_level, education_field, school_tier, years_experience):
    """
    Calculates the Human Capital Factor (FHC).
    FHC = f_role * f_level * f_field * f_school * f_exp
    """
    f_role = JOB_DATA[JOB_DATA['Job Title'] == job_title]['f_role'].iloc[0] if job_title in JOB_DATA['Job Title'].values else 1.0
    f_level = EDUCATION_LEVEL_DATA.get(education_level, 1.0)
    f_field = EDUCATION_FIELD_DATA.get(education_field, 1.0)
    f_school = SCHOOL_TIER_DATA.get(school_tier, 1.0)
    f_exp = calculate_f_exp(years_experience)

    FHC = f_role * f_level * f_field * f_school * f_exp
    return FHC

def calculate_fcr(company_type):
    """
    Calculates the Company Risk Factor (FCR).
    In this simplified synthetic example, FCR is directly looked up by company type.
    FCR = w1 * S_senti + w2 * S_fin + w3 * S_growth (abstracted for synthetic data)
    """
    # For synthetic data, we directly use a pre-defined FCR per company type
    return COMPANY_TYPE_DATA.get(company_type, {'FCR': 1.0})['FCR']

def calculate_fus(p_gen_t, p_spec_t):
    """
    Calculates the Upskilling Factor (FUS).
    FUS = 1 - (gamma_gen * P_gen(t) + gamma_spec * P_spec(t))
    """
    gamma_gen = DEFAULT_PARAMS['gamma_gen']
    gamma_spec = DEFAULT_PARAMS['gamma_spec']
    FUS = 1 - (gamma_gen * (p_gen_t / 100.0) + gamma_spec * (p_spec_t / 100.0))
    return FUS

def calculate_v_raw(fhc, fcr, fus):
    """
    Calculates the Raw Idiosyncratic Risk (V_raw).
    V_raw = FHC * (w_CR * FCR + w_US * FUS)
    """
    w_CR = DEFAULT_PARAMS['w_CR']
    w_US = DEFAULT_PARAMS['w_US']
    V_raw = fhc * (w_CR * fcr + w_US * fus)
    return V_raw

def calculate_idiosyncratic_risk(v_raw):
    """
    Calculates the Idiosyncratic Risk (Vi(t)).
    V_i(t) = min(100.0, max(5.0, V_raw - 50.0))
    """
    V_i_t = min(100.0, max(5.0, v_raw - 50.0))
    return V_i_t

def calculate_h_base_ttv(k, ttv, h_current, h_target):
    """
    Calculates the Time-to-Value (TTV) Modified Base Occupational Hazard (H_base(k)).
    H_base(k) = (1 - k/TTV) * H_current + (k/TTV) * H_target
    """
    if ttv == 0: # Avoid division by zero if TTV is 0 (should not happen with default min_value=1)
        return h_target
    k = min(k, ttv) # Cap k at TTV to ensure smooth transition
    H_base_k = (1 - k / ttv) * h_current + (k / ttv) * h_target
    return H_base_k

def calculate_systematic_risk(h_base_t, m_econ, iai):
    """
    Calculates the Systematic Risk (H_i).
    H_i = H_base(t) * (w_econ * M_econ + w_inno * IAI)
    """
    w_econ = DEFAULT_PARAMS['w_econ']
    w_inno = DEFAULT_PARAMS['w_inno']
    H_i = h_base_t * (w_econ * m_econ + w_inno * iai)
    return H_i

def calculate_p_systemic(h_i):
    """
    Calculates the Systemic Event Base Probability (P_systemic).
    P_systemic = (H_i / 100) * beta_systemic
    """
    beta_systemic = DEFAULT_PARAMS['beta_systemic']
    P_sys = (h_i / 100.0) * beta_systemic
    return P_sys

def calculate_p_individual_systemic(v_i_t):
    """
    Calculates the Individual Loss Base Probability (P_individual|systemic).
    P_individual|systemic = (V_i(t) / 100) * beta_individual
    """
    beta_individual = DEFAULT_PARAMS['beta_individual']
    P_ind_sys = (v_i_t / 100.0) * beta_individual
    return P_ind_sys

def calculate_p_claim(p_systemic, p_individual_systemic):
    """
    Calculates the Annual Claim Probability (P_claim).
    P_claim = P_systemic * P_individual|systemic
    """
    P_claim = p_systemic * p_individual_systemic
    return P_claim

def calculate_l_payout(annual_salary, coverage_duration_months, coverage_percentage):
    """
    Calculates the Total Payout Amount (L_payout).
    L_payout = (Annual Salary / 12) * Coverage Duration * Coverage Percentage
    """
    L_payout = (annual_salary / 12.0) * coverage_duration_months * (coverage_percentage / 100.0)
    return L_payout

def calculate_e_loss(p_claim, l_payout):
    """
    Calculates the Annual Expected Loss (E[Loss]).
    E[Loss] = P_claim * L_payout
    """
    E_Loss = p_claim * l_payout
    return E_Loss

def calculate_p_monthly(e_loss, p_min):
    """
    Calculates the Monthly Insurance Premium (P_monthly).
    P_monthly = max((E[Loss] * lambda) / 12, P_min)
    """
    lambda_loading = DEFAULT_PARAMS['lambda_loading']
    P_monthly = max((e_loss * lambda_loading) / 12.0, p_min)
    return P_monthly

def get_h_base_for_job_title(job_title):
    """
    Helper to get H_base from job data.
    """
    return JOB_DATA[JOB_DATA['Job Title'] == job_title]['H_base'].iloc[0] if job_title in JOB_DATA['Job Title'].values else 0
