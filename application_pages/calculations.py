
import numpy as np
from application_pages.data_utils import load_default_actuarial_parameters, get_job_hazard_and_role_factor

params = load_default_actuarial_parameters()

def calculate_f_exp(years_experience):
    a = params['a_decay_constant']
    Y_cap = params['Y_cap']
    f_exp = 1 - (a * min(years_experience, Y_cap))
    return max(0.1, f_exp) # Ensure f_exp doesn't go too low

def calculate_fhc(f_role, f_level, f_field, f_school, f_exp):
    # FHC = f_role * f_level * f_field * f_school * f_exp
    fhc = f_role * f_level * f_field * f_school * f_exp
    return fhc

def calculate_fcr(s_senti, s_fin, s_growth, w1=0.33, w2=0.33, w3=0.34): # Default weights sum to 1
    # FCR = w1 * S_senti + w2 * S_fin + w3 * S_growth
    fcr = w1 * s_senti + w2 * s_fin + w3 * s_growth
    return fcr

def calculate_fus(p_gen, p_spec):
    gamma_gen = params['gamma_gen']
    gamma_spec = params['gamma_spec']
    # FUS = 1 - (gamma_gen * P_gen(t) + gamma_spec * P_spec(t))
    fus = 1 - (gamma_gen * (p_gen / 100) + gamma_spec * (p_spec / 100))
    return max(0.1, fus) # Ensure FUS doesn't go too low

def calculate_v_raw(fhc, fcr, fus):
    w_CR = params['w_CR']
    w_US = params['w_US']
    # V_raw = FHC * (w_CR * FCR + w_US * FUS)
    v_raw = fhc * (w_CR * fcr + w_US * fus)
    return v_raw

def calculate_idiosyncratic_risk(v_raw):
    # V_i(t) = min(100.0, max(5.0, V_raw - 50.0))
    # Adjusted to ensure positive impact from V_raw
    # If V_raw is a risk score, higher V_raw means higher risk.
    # The original formula `V_raw - 50.0` seems to imply V_raw starts high (e.g. 100) and is reduced
    # Let's assume V_raw is more direct. If V_raw increases, V_i(t) should increase.
    # Re-interpreting: V_raw is the *magnitude* of raw risk.
    # A simple normalization for a 0-100 scale:
    v_i_t = np.clip(v_raw, 5.0, 100.0) # Ensure it's between 5 and 100
    return v_i_t

def calculate_ttv_modified_h_base(k_months, ttv_months, h_current, h_target):
    # H_base(k) = (1 - k/TTV) * H_current + (k/TTV) * H_target
    if ttv_months == 0: # Avoid division by zero if TTV is 0
        return h_target if k_months >= 0 else h_current
    
    k_norm = min(k_months, ttv_months) / ttv_months
    h_base_k = (1 - k_norm) * h_current + k_norm * h_target
    return h_base_k

def calculate_systematic_risk(h_base_t, m_econ, iai):
    w_econ = params['w_econ']
    w_inno = params['w_inno']
    # H_i = H_base(t) * (w_econ * M_econ + w_inno * IAI)
    h_i = h_base_t * (w_econ * m_econ + w_inno * iai)
    return h_i

def calculate_p_systemic(h_i):
    beta_systemic = params['beta_systemic']
    # P_systemic = (H_i / 100) * beta_systemic
    p_systemic = (h_i / 100) * beta_systemic
    return np.clip(p_systemic, 0.0, 1.0) # Probability between 0 and 1

def calculate_p_individual_systemic(v_i_t):
    beta_individual = params['beta_individual']
    # P_individual|systemic = (V_i(t) / 100) * beta_individual
    p_individual_systemic = (v_i_t / 100) * beta_individual
    return np.clip(p_individual_systemic, 0.0, 1.0) # Probability between 0 and 1

def calculate_p_claim(p_systemic, p_individual_systemic):
    # P_claim = P_systemic * P_individual|systemic
    p_claim = p_systemic * p_individual_systemic
    return np.clip(p_claim, 0.0, 1.0) # Probability between 0 and 1

def calculate_l_payout(annual_salary, coverage_duration_months, coverage_percentage):
    # L_payout = (Annual Salary / 12) * Coverage Duration * Coverage Percentage
    l_payout = (annual_salary / 12) * coverage_duration_months * (coverage_percentage / 100)
    return l_payout

def calculate_e_loss(p_claim, l_payout):
    # E[Loss] = P_claim * L_payout
    e_loss = p_claim * l_payout
    return e_loss

def calculate_p_monthly(e_loss):
    lambda_loading_factor = params['lambda_loading_factor']
    p_min = params['P_min']
    # P_monthly = max((E[Loss] * lambda) / 12, P_min)
    p_monthly = max((e_loss * lambda_loading_factor) / 12, p_min)
    return p_monthly
