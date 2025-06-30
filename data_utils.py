
import pandas as pd
import numpy as np

def load_job_data():
    """
    Generates synthetic O*NET-like data for job roles, including base AI hazard scores and f_role multipliers.
    """
    data = {
        'Job Title': [
            "Data Scientist", "Software Engineer", "Marketing Manager",
            "Financial Analyst", "HR Specialist", "Customer Service Rep",
            "Truck Driver", "Accountant", "Registered Nurse", "Teacher",
            "AI Engineer", "Machine Learning Scientist", "Cloud Architect",
            "Business Analyst", "Operations Manager", "Graphic Designer",
            "Sales Representative", "Journalist", "Legal Assistant", "Pharmacist"
        ],
        'Base_AI_Hazard': [
            85, 75, 55, 65, 45, 90, 70, 80, 30, 40, 95, 92, 80, 60, 50, 60, 55, 70, 85, 40
        ],
        'f_role_multiplier': [
            1.1, 1.05, 0.9, 0.95, 0.85, 1.2, 1.0, 1.15, 0.7, 0.8, 1.25, 1.2, 1.1, 0.9, 0.85, 0.9, 0.8, 1.0, 1.15, 0.8
        ]
    }
    df = pd.DataFrame(data)
    df.set_index('Job Title', inplace=True)
    return df

def load_human_capital_factors():
    """
    Generates lookup tables for Human Capital factors.
    """
    education_level_factors = {
        "PhD": 0.7,
        "Master's": 0.8,
        "Bachelor's": 0.9,
        "Associate's": 1.0,
        "High School": 1.1
    }

    education_field_factors = {
        "Tech/Engineering": 0.75,
        "Science/Research": 0.8,
        "Business/Finance": 0.9,
        "Healthcare": 0.7,
        "Arts/Humanities": 1.0,
        "Education": 0.85,
        "Law": 0.95
    }

    school_tier_factors = {
        "Tier 1 (Ivy League/Top Research)": 0.7,
        "Tier 2 (Reputable State/Private)": 0.8,
        "Tier 3 (Local/Community)": 0.9
    }

    return education_level_factors, education_field_factors, school_tier_factors

def load_company_risk_factors():
    """
    Generates dummy data for Company Risk factors based on company types.
    S_senti, S_fin, S_growth are inversely correlated with risk (lower score = less risk).
    Here, we'll use base risk values that contribute to FCR.
    The FCR formula specifies FCR = w1*Ssenti + w2*Sfin + w3*Sgrowth.
    Higher S_values here means higher risk contribution.
    """
    company_type_data = {
        "Big firm (Stable)": {"S_senti": 0.7, "S_fin": 0.6, "S_growth": 0.7},
        "Mid-size firm (Growing)": {"S_senti": 0.8, "S_fin": 0.8, "S_growth": 0.9},
        "Startup (High Growth/Risk)": {"S_senti": 0.9, "S_fin": 0.95, "S_growth": 1.1}
    }
    return company_type_data

def load_actuarial_parameters():
    """
    Provides default values for actuarial parameters.
    """
    params = {
        'beta_systemic': 0.10,  # Base annual probability of a systemic displacement event
        'beta_individual': 0.50, # Base conditional probability of job loss for most vulnerable
        'lambda_loading_factor': 1.5, # Loading Factor
        'p_min_monthly': 20.00, # Minimum monthly premium
        'decay_constant_a': 0.015, # for f_exp
        'years_cap_y': 20 # for f_exp
    }
    return params

def load_weights():
    """
    Provides default weights for various factors.
    """
    weights = {
        'w_cr': 0.4, # Weight for Company Risk Factor in V_raw
        'w_us': 0.6, # Weight for Upskilling Factor in V_raw
        'w_econ': 0.5, # Weight for Economic Climate Modifier in H_i
        'w_inno': 0.5, # Weight for AI Innovation Index in H_i
        'w1_fcr': 0.33, 'w2_fcr': 0.33, 'w3_fcr': 0.34, # Weights for S_senti, S_fin, S_growth in FCR (sum to 1)
        'gamma_gen': 0.7, # Weight for general skills in FUS (rewards portable skills more)
        'gamma_spec': 0.3 # Weight for firm-specific skills in FUS
    }
    return weights

