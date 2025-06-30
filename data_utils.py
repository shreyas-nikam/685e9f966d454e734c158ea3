import pandas as pd
import numpy as np

def load_job_data():
    """
    Generates synthetic O*NET-like data for job roles, their intrinsic AI hazard scores,
    and role multipliers for Human Capital factors.
    """
    data = {
        "Job Title": [
            "Data Scientist", "Software Engineer", "Accountant", "Customer Service Rep",
            "Truck Driver", "Graphic Designer", "HR Manager", "Financial Analyst",
            "Marketing Specialist", "Operations Manager", "Nurse", "Teacher",
            "Construction Worker", "Chef", "Lawyer", "Doctor"
        ],
        "f_role": [ # Role Multiplier for FHC (lower is better, <1)
            0.6, 0.7, 0.9, 0.95,
            0.8, 0.75, 0.85, 0.7,
            0.8, 0.8, 0.65, 0.65,
            0.9, 0.85, 0.7, 0.6
        ],
        "H_base": [ # Base Occupational Hazard (higher is more risk, 0-100)
            85, 70, 90, 95,
            75, 60, 50, 80,
            65, 55, 30, 25,
            40, 35, 60, 20
        ]
    }
    return pd.DataFrame(data)

def load_education_data():
    """
    Generates lookup tables for education level and field factors.
    """
    education_level_data = {
        "PhD": 0.5, "Master's": 0.6, "Bachelor's": 0.7,
        "Associate's": 0.8, "High School": 0.9, "None": 1.0
    }
    education_field_data = {
        "Tech/Engineering": 0.6, "Science/Research": 0.65, "Healthcare": 0.55,
        "Business/Finance": 0.7, "Arts/Humanities": 0.8, "Liberal Arts": 0.85,
        "Trades/Vocational": 0.75, "Education": 0.7
    }
    return education_level_data, education_field_data

def load_school_tier_data():
    """
    Generates lookup table for institution tier factors.
    """
    return {
        "Tier 1 (Top 25)": 0.6,
        "Tier 2 (Top 50)": 0.7,
        "Tier 3 (Top 100)": 0.8,
        "Tier 4 (Others)": 0.9,
        "No Degree": 1.0
    }

def load_company_type_data():
    """
    Generates dummy data for Company Risk factors based on company types.
    Assumes S_senti, S_fin, S_growth contribute to FCR (lower FCR is better).
    """
    data = {
        "Company Type": ["Big firm", "Mid-size firm", "Startup", "Government/Non-profit"],
        "S_senti": [0.6, 0.7, 0.8, 0.65], # Sentiment Score (lower is better for risk)
        "S_fin": [0.5, 0.6, 0.85, 0.6],  # Financial Health (lower is better for risk)
        "S_growth": [0.7, 0.65, 0.5, 0.75] # Growth & AI-Adoption (lower is better for risk, implies higher risk if not adapting)
    }
    return pd.DataFrame(data)

def load_default_actuarial_parameters():
    """
    Provides default values for actuarial and environmental parameters.
    """
    return {
        "w_CR": 0.4, # Weight for Company Risk Factor in V_raw
        "w_US": 0.6, # Weight for Upskilling Factor in V_raw
        "a_exp": 0.015, # Decay constant for f_exp
        "Y_cap": 20, # Capped years of experience for f_exp
        "gamma_gen": 0.005, # Weight for general skills in FUS
        "gamma_spec": 0.002, # Weight for firm-specific skills in FUS (gamma_gen > gamma_spec)
        "w_econ": 0.5, # Calibration weight for economic modifier in Hi
        "w_inno": 0.5, # Calibration weight for AI innovation index in Hi
        "beta_systemic": 0.10, # Base annual probability of a systemic displacement event
        "beta_individual": 0.50, # Base conditional probability of job loss for most vulnerable
        "loading_factor": 1.5, # Standard insurance multiplier (lambda)
        "min_premium": 20.00, # Minimum monthly premium (P_min)
        "ttv_default": 12 # Default Time-to-Value period in months
    }

def get_factor_value(df, key_column, value_column, key):
    """Helper to get a factor value from a DataFrame based on a key."""
    if key in df[key_column].values:
        return df.loc[df[key_column] == key, value_column].iloc[0]
    return 1.0 # Default to no impact if key not found (or handle error)

def get_dict_value(data_dict, key):
    """Helper to get a factor value from a dictionary based on a key."""
    return data_dict.get(key, 1.0) # Default to no impact if key not found