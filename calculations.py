
import numpy as np
import pandas as pd
from data_utils import get_default_parameters, load_job_data, load_education_data, load_school_tier_data, load_company_type_data

PARAMS = get_default_parameters()
JOB_DATA = load_job_data()
EDU_DATA = load_education_data()
SCHOOL_DATA = load_school_tier_data()
COMPANY_DATA = load_company_type_data()

def calculate_f_exp(years_experience):
    a = PARAMS['a_exp_decay']
    Y_cap = PARAMS['Y_cap_exp']
    return 1 - (a * min(years_experience, Y_cap))

def calculate_fhc(job_title, education_level, education_field, school_tier, years_experience):
    f_role = JOB_DATA[JOB_DATA['Job Title'] == job_title]['f_role'].iloc[0]
    f_level = EDU_DATA[education_level]['f_level']
    f_field = EDU_DATA[education_field]['f_field']
    f_school = SCHOOL_DATA[school_tier]['f_school']
    f_exp = calculate_f_exp(years_experience)
    return f_role * f_level * f_field * f_school * f_exp

def calculate_fcr(company_type):
    # For simplicity, using dummy S_senti, S_fin, S_growth based on company type
    # In a real app, these would come from complex models
    company_info = COMPANY_DATA[company_type]
    S_senti = company_info['S_senti']
    S_fin = company_info['S_fin']
    S_growth = company_info['S_growth']

    # Assuming w1=w2=w3=0.33 for simplicity as per specs
    w1, w2, w3 = 1/3, 1/3, 1/3
    return (w1 * S_senti) + (w2 * S_fin) + (w3 * S_growth)

def calculate_fus(p_gen, p_spec):
    gamma_gen = PARAMS['gamma_gen']
    gamma_spec = PARAMS['gamma_spec']
    return 1 - (gamma_gen * p_gen + gamma_spec * p_spec)

def calculate_v_raw(fhc, fcr, fus):
    w_CR = PARAMS['w_CR']
    w_US = PARAMS['w_US']
    return fhc * (w_CR * fcr + w_US * fus)

def calculate_idiosyncratic_risk(v_raw):
    return min(100.0, max(5.0, v_raw - 50.0))

def get_h_base(job_title):
    return JOB_DATA[JOB_DATA['Job Title'] == job_title]['H_base'].iloc[0]

def calculate_h_base_ttv(k_months, ttv_months, h_current, h_target):
    if ttv_months == 0: # Avoid division by zero if TTV is 0
        return h_target
    if k_months >= ttv_months:
        return h_target # Once transition is complete, it's fully target H_base
    return (1 - k_months / ttv_months) * h_current + (k_months / ttv_months) * h_target

def calculate_systematic_risk(h_base_t, m_econ, iai):
    w_econ = PARAMS['w_econ']
    w_inno = PARAMS['w_inno']
    return h_base_t * (w_econ * m_econ + w_inno * iai)

def calculate_p_systemic(h_i):
    beta_systemic = PARAMS['beta_systemic']
    return (h_i / 100) * beta_systemic

def calculate_p_individual_systemic(v_i_t):
    beta_individual = PARAMS['beta_individual']
    return (v_i_t / 100) * beta_individual

def calculate_p_claim(p_systemic, p_individual_systemic):
    return p_systemic * p_individual_systemic

def calculate_l_payout(annual_salary, coverage_duration_months, coverage_percentage):
    return (annual_salary / 12) * coverage_duration_months * (coverage_percentage / 100)

def calculate_e_loss(p_claim, l_payout):
    return p_claim * l_payout

def calculate_p_monthly(e_loss):
    loading_factor = PARAMS['loading_factor']
    min_premium = PARAMS['min_premium']
    return max((e_loss * loading_factor) / 12, min_premium)
