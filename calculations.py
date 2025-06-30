
import numpy as np
import pandas as pd

def calculate_f_exp(years_experience, decay_constant_a, years_cap_y):
    """
    Calculates the Experience Factor (f_exp).
    f_exp = 1 - (a * min(Y_i, Y_cap))
    """
    return 1 - (decay_constant_a * min(years_experience, years_cap_y))

def calculate_fhc(f_role, f_level, f_field, f_school, f_exp):
    """
    Calculates the Human Capital Factor (FHC).
    FHC = f_role * f_level * f_field * f_school * f_exp
    """
    return f_role * f_level * f_field * f_school * f_exp

def calculate_fcr(s_senti, s_fin, s_growth, w1, w2, w3):
    """
    Calculates the Company Risk Factor (FCR).
    FCR = w1 * S_senti + w2 * S_fin + w3 * S_growth
    """
    return w1 * s_senti + w2 * s_fin + w3 * s_growth

def calculate_fus(p_gen_t, p_spec_t, gamma_gen, gamma_spec):
    """
    Calculates the Upskilling Factor (FUS).
    FUS = 1 - (gamma_gen * P_gen(t) + gamma_spec * P_spec(t))
    """
    return 1 - (gamma_gen * p_gen_t + gamma_spec * p_spec_t)

def calculate_v_raw(fhc, fcr, fus, w_cr, w_us):
    """
    Calculates the Raw Idiosyncratic Risk (V_raw).
    V_raw = FHC * (w_CR * FCR + w_US * FUS)
    """
    return fhc * (w_cr * fcr + w_us * fus)

def calculate_idiosyncratic_risk(v_raw):
    """
    Calculates the Idiosyncratic Risk (V_i(t)).
    V_i(t) = min(100.0, max(5.0, V_raw - 50.0))
    """
    return min(100.0, max(5.0, v_raw - 50.0))

def calculate_h_base_ttv(k, ttv, h_current, h_target):
    """
    Calculates the Time-to-Value (TTV) Modified Base Occupational Hazard (H_base(k)).
    H_base(k) = (1 - k/TTV) * H_current + (k/TTV) * H_target
    """
    if ttv == 0: # Avoid division by zero if TTV is 0 (e.g., instant transition)
        return h_target
    if k >= ttv: # If transition is complete or beyond TTV, it's fully target
        return h_target
    return (1 - k/ttv) * h_current + (k/ttv) * h_target

def calculate_systematic_risk(h_base_t, m_econ, iai, w_econ, w_inno):
    """
    Calculates the Systematic Risk (H_i).
    H_i = H_base(t) * (w_econ * M_econ + w_inno * IAI)
    """
    return h_base_t * (w_econ * m_econ + w_inno * iai)

def calculate_p_systemic(h_i, beta_systemic):
    """
    Calculates the Systemic Event Base Probability (P_systemic).
    P_systemic = (H_i / 100) * beta_systemic
    """
    return (h_i / 100.0) * beta_systemic

def calculate_p_individual_systemic(v_i_t, beta_individual):
    """
    Calculates the Individual Loss Base Probability (P_individual|systemic).
    P_individual|systemic = (V_i(t) / 100) * beta_individual
    """
    return (v_i_t / 100.0) * beta_individual

def calculate_p_claim(p_systemic, p_individual_systemic):
    """
    Calculates the Annual Claim Probability (P_claim).
    P_claim = P_systemic * P_individual|systemic
    """
    return p_systemic * p_individual_systemic

def calculate_l_payout(annual_salary, coverage_duration_months, coverage_percentage):
    """
    Calculates the Total Payout Amount (L_payout).
    L_payout = (Annual Salary / 12) * Coverage Duration * Coverage Percentage
    """
    return (annual_salary / 12.0) * coverage_duration_months * (coverage_percentage / 100.0)

def calculate_expected_loss(p_claim, l_payout):
    """
    Calculates the Annual Expected Loss (E[Loss]).
    E[Loss] = P_claim * L_payout
    """
    return p_claim * l_payout

def calculate_monthly_premium(e_loss, loading_factor, p_min):
    """
    Calculates the Monthly Insurance Premium (P_monthly).
    P_monthly = max((E[Loss] * lambda) / 12, P_min)
    """
    return max((e_loss * loading_factor) / 12.0, p_min)

