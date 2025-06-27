
import pandas as pd
import numpy as np

def load_job_data():
    # O*NET-like data for job roles and their intrinsic AI hazard scores (H_base)
    # and f_role multipliers.
    data = {
        'Job Title': [
            'Software Engineer', 'Data Scientist', 'Financial Analyst',
            'Customer Service Rep', 'Truck Driver', 'Accountant',
            'Marketing Specialist', 'HR Manager', 'Research Scientist',
            'Construction Worker'
        ],
        'f_role': [1.0, 1.1, 0.9, 0.7, 0.8, 0.95, 0.85, 0.9, 1.05, 0.6],
        'H_base': [70, 75, 60, 85, 70, 65, 55, 50, 80, 40]
    }
    return pd.DataFrame(data)

def load_education_data():
    # Lookup tables for Human Capital factors (f_level, f_field)
    return {
        'PhD': {'f_level': 1.2},
        'Master's': {'f_level': 1.1},
        'Bachelor's': {'f_level': 1.0},
        'Associate's': {'f_level': 0.9},
        'High School': {'f_level': 0.8},
        'Tech/Engineering': {'f_field': 1.1},
        'Science': {'f_field': 1.05},
        'Business/Finance': {'f_field': 1.0},
        'Liberal Arts': {'f_field': 0.9},
        'Vocational': {'f_field': 0.95}
    }

def load_school_tier_data():
    return {
        'Tier 1': {'f_school': 1.15},
        'Tier 2': {'f_school': 1.05},
        'Tier 3': {'f_school': 1.0},
        'Tier 4': {'f_school': 0.95},
        'Tier 5': {'f_school': 0.9}
    }

def load_company_type_data():
    # Dummy data for Company Risk factors (S_senti, S_fin, S_growth)
    # Weights w1, w2, w3 for FCR are 0.33 each for simplicity.
    return {
        'Big Firm': {'S_senti': 0.8, 'S_fin': 0.9, 'S_growth': 0.7},
        'Mid-size Firm': {'S_senti': 0.7, 'S_fin': 0.8, 'S_growth': 0.6},
        'Startup': {'S_senti': 0.6, 'S_fin': 0.6, 'S_growth': 0.8},
        'Non-profit': {'S_senti': 0.7, 'S_fin': 0.7, 'S_growth': 0.5},
        'Government': {'S_senti': 0.9, 'S_fin': 0.95, 'S_growth': 0.4}
    }

def get_default_parameters():
    return {
        # Raw Idiosyncratic Risk (V_raw) weights
        'w_CR': 0.4,
        'w_US': 0.6,

        # Experience Factor (f_exp) parameters
        'a_exp_decay': 0.015,
        'Y_cap_exp': 20,

        # Upskilling Factor (FUS) weights
        'gamma_gen': 0.6, # Reward portable skills more heavily
        'gamma_spec': 0.4,

        # Systematic Risk (H_i) weights
        'w_econ': 0.5,
        'w_inno': 0.5,

        # Actuarial parameters
        'beta_systemic': 0.10, # Base annual probability of systemic displacement event in highest-risk industry
        'beta_individual': 0.50, # Base conditional probability of job loss for most vulnerable person
        'loading_factor': 1.5, # Lambda (lambda)
        'min_premium': 20.00, # P_min
        'default_ttv_months': 12, # Default TTV in months
    }

