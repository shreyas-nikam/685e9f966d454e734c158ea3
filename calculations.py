import numpy as np
from data_utils import (
    load_job_data, load_education_data, load_school_tier_data,
    load_company_type_data, load_default_actuarial_parameters,
    get_factor_value, get_dict_value
)

# Load data and parameters once
job_data = load_job_data()
education_level_data, education_field_data = load_education_data()
school_tier_data = load_school_tier_data()
company_type_data = load_company_type_data()
params = load_default_actuarial_parameters()

def calculate_f_exp(years_experience):
    """
    Calculate the Experience Factor ($f_{exp}$).
    Formula: $f_{exp} = 1 - (a \cdot \min(Y_i, Y_{cap}))$
    """
    a = params["a_exp"]
    Y_cap = params["Y_cap"]
    f_exp = 1 - (a * min(years_experience, Y_cap))
    return max(0.1, f_exp) # Ensure f_exp doesn't go too low

def calculate_fhc(job_title, education_level, education_field, school_tier, years_experience):
    """
    Calculate the Human Capital Factor ($FHC$).
    Formula: $FHC = f_{role} \cdot f_{level} \cdot f_{field} \cdot f_{school} \cdot f_{exp}$
    """
    f_role = get_factor_value(job_data, "Job Title", "f_role", job_title)
    f_level = get_dict_value(education_level_data, education_level)
    f_field = get_dict_value(education_field_data, education_field)
    f_school = get_dict_value(school_tier_data, school_tier)
    f_exp = calculate_f_exp(years_experience)

    FHC = f_role * f_level * f_field * f_school * f_exp
    return FHC

def calculate_fcr(company_type):
    """
    Calculate the Company Risk Factor ($FCR$).
    Formula: $FCR = w_1 \cdot S_{senti} + w_2 \cdot S_{fin} + w_3 \cdot S_{growth}$
    (Assuming equal weights for simplicity, as per spec suggestion: 0.33 each)
    """
    w1, w2, w3 = 1/3, 1/3, 1/3 # Simplified as per technical spec for simplicity

    s_senti = get_factor_value(company_type_data, "Company Type", "S_senti", company_type)
    s_fin = get_factor_value(company_type_data, "Company Type", "S_fin", company_type)
    s_growth = get_factor_value(company_type_data, "Company Type", "S_growth", company_type)

    FCR = (w1 * s_senti) + (w2 * s_fin) + (w3 * s_growth)
    return FCR

def calculate_fus(gen_skill_progress, firm_skill_progress):
    """
    Calculate the Upskilling Factor ($FUS$).
    Formula: $FUS = 1 - (\gamma_{gen} P_{gen}(t) + \gamma_{spec} P_{spec}(t))$
    """
    gamma_gen = params["gamma_gen"]
    gamma_spec = params["gamma_spec"]
    P_gen = gen_skill_progress / 100.0 # Convert percentage to decimal
    P_spec = firm_skill_progress / 100.0 # Convert percentage to decimal

    FUS = 1 - (gamma_gen * P_gen + gamma_spec * P_spec)
    return FUS

def calculate_v_raw(FHC, FCR, FUS):
    """
    Calculate the Raw Idiosyncratic Risk ($V_{raw}$).
    Formula: $V_{raw} = FHC \cdot (w_{CR} FCR + w_{US} FUS)$
    """
    w_CR = params["w_CR"]
    w_US = params["w_US"]

    V_raw = FHC * (w_CR * FCR + w_US * FUS)
    return V_raw

def calculate_idiosyncratic_risk(V_raw):
    """
    Calculate the Idiosyncratic Risk ($V_i(t)$).
    Formula: $V_i(t) = \min(100.0, \max(5.0, V_{raw} - 50.0))$
    """
    V_i_t = min(100.0, max(5.0, V_raw - 50.0))
    return V_i_t

def calculate_h_base_ttv(k, ttv, h_current, h_target):
    """
    Calculate the Time-to-Value (TTV) Modified Base Occupational Hazard ($H_{base}(k)$).
    Formula: $H_{base}(k) = \left(1 - \frac{k}{TTV}\right) H_{current} + \left(\frac{k}{TTV}\right) H_{target}$
    """
    if ttv == 0: # Avoid division by zero if TTV is 0 (though UI enforces min_value=1)
        return h_target if k >= 0 else h_current
    
    k = max(0, min(k, ttv)) # Ensure k is within [0, TTV]
    H_base_k = (1 - k/ttv) * h_current + (k/ttv) * h_target
    return H_base_k

def calculate_systematic_risk(h_base_t, m_econ, iai):
    """
    Calculate the Systematic Risk ($H_i$).
    Formula: $H_i = H_{base}(t) \cdot (w_{econ} M_{econ} + w_{inno} IAI)$
    """
    w_econ = params["w_econ"]
    w_inno = params["w_inno"]

    H_i = h_base_t * (w_econ * m_econ + w_inno * iai)
    return H_i

def calculate_p_systemic(H_i):
    """
    Calculate the Systemic Event Base Probability ($P_{systemic}$).
    Formula: $P_{systemic} = \frac{H_i}{100} \cdot \beta_{systemic}$
    """
    beta_systemic = params["beta_systemic"]
    P_systemic = (H_i / 100.0) * beta_systemic
    return P_systemic

def calculate_p_individual_systemic(V_i_t):
    """
    Calculate the Individual Loss Base Probability ($P_{individual|systemic}$).
    Formula: $P_{individual|systemic} = \frac{V_i(t)}{100} \cdot \beta_{individual}$
    """
    beta_individual = params["beta_individual"]
    P_individual_systemic = (V_i_t / 100.0) * beta_individual
    return P_individual_systemic

def calculate_p_claim(P_systemic, P_individual_systemic):
    """
    Calculate the Annual Claim Probability ($P_{claim}$).
    Formula: $P_{claim} = P_{systemic} \cdot P_{individual|systemic}$
    """
    P_claim = P_systemic * P_individual_systemic
    return P_claim

def calculate_l_payout(annual_salary, coverage_duration_months, coverage_percentage):
    """
    Calculate the Total Payout Amount ($L_{payout}$).
    Formula: $L_{payout} = \left( \frac{\text{Annual Salary}}{12} \right) \cdot \text{Coverage Duration} \cdot \text{Coverage Percentage}$
    """
    L_payout = (annual_salary / 12.0) * coverage_duration_months * (coverage_percentage / 100.0)
    return L_payout

def calculate_expected_loss(P_claim, L_payout):
    """
    Calculate the Annual Expected Loss ($E[Loss]$).
    Formula: $E[Loss] = P_{claim} \cdot L_{payout}$
    """
    E_Loss = P_claim * L_payout
    return E_Loss

def calculate_monthly_premium(E_Loss):
    """
    Calculate the Monthly Insurance Premium ($P_{monthly}$).
    Formula: $P_{monthly} = \max \left( \frac{E[Loss] \cdot \lambda}{12}, P_{min} \right)$
    """
    loading_factor = params["loading_factor"]
    min_premium = params["min_premium"]

    P_monthly = max((E_Loss * loading_factor) / 12.0, min_premium)
    return P_monthly

def get_h_base_for_job(job_title):
    """Helper to retrieve H_base for a given job title."""
    return get_factor_value(job_data, "Job Title", "H_base", job_title)