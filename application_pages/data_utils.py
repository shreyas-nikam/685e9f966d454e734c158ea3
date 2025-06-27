
import pandas as pd
import numpy as np

def load_job_data():
    """
    Generates a synthetic dataset for job roles, their f_role multipliers,
    and baseline H_base (occupational hazard) scores.
    """
    data = {
        'Job Title': [
            'Software Engineer', 'Data Scientist', 'AI/ML Engineer',
            'Financial Analyst', 'Marketing Manager', 'HR Specialist',
            'Accountant', 'Customer Service Rep', 'Truck Driver',
            'Graphic Designer', 'Nurse', 'Teacher'
        ],
        'f_role': [
            0.8, 0.75, 0.7,  # Lower for tech/data roles due to demand/reskilling
            0.9, 0.95, 1.0,
            1.05, 1.1, 1.2,  # Higher for roles with more routine/automatable tasks
            0.95, 0.85, 0.9
        ],
        'H_base': [
            40, 50, 60,  # Higher H_base for roles more directly impacted by AI
            35, 30, 20,
            25, 45, 70,  # Truck driver, customer service more susceptible
            30, 15, 20   # Nurse/Teacher lower H_base
        ],
        'Industry': [
            'Tech', 'Tech', 'Tech',
            'Finance', 'Marketing', 'HR',
            'Finance', 'Service', 'Logistics',
            'Creative', 'Healthcare', 'Education'
        ]
    }
    return pd.DataFrame(data)

def load_education_data():
    """
    Generates a synthetic lookup table for education level and field factors.
    """
    education_level_data = {
        'PhD': 0.7,
        'Master's': 0.8,
        'Bachelor's': 0.9,
        'Associate's': 1.0,
        'High School': 1.1,
    }
    education_field_data = {
        'Tech/Engineering': 0.75,
        'Data Science/AI': 0.7,
        'Business/Finance': 0.85,
        'Humanities/Arts': 1.0,
        'Healthcare': 0.8,
        'Education': 0.9,
        'Trades/Vocational': 1.05
    }
    return education_level_data, education_field_data

def load_school_tier_data():
    """
    Generates a synthetic lookup table for institution tier factors.
    """
    school_tier_data = {
        'Tier 1 (Top 10%)': 0.75,
        'Tier 2 (Top 25%)': 0.85,
        'Tier 3 (Top 50%)': 0.95,
        'Tier 4 (Other)': 1.05
    }
    return school_tier_data

def load_company_type_data():
    """
    Generates synthetic data for company type to base FCR values.
    Simplified for this example; in a real scenario, this might involve
    S_senti, S_fin, S_growth directly. Here we use a direct FCR.
    """
    company_type_data = {
        'Big Firm (Stable)': {'FCR': 0.8},
        'Mid-size Firm (Growth)': {'FCR': 0.9},
        'Startup (High Risk/Reward)': {'FCR': 1.1},
        'Government/Non-Profit (Very Stable)': {'FCR': 0.7}
    }
    return company_type_data

def load_default_parameters():
    """
    Loads default actuarial and weighting parameters.
    """
    return {
        'w_CR': 0.4, # Weight assigned to the Company Risk Factor
        'w_US': 0.6, # Weight assigned to the Upskilling Factor
        'a_decay': 0.015, # Decay constant for Experience Factor
        'Y_cap': 20, # Capped years of experience
        'w1_FCR': 0.33, 'w2_FCR': 0.33, 'w3_FCR': 0.34, # Weights for S_senti, S_fin, S_growth (sum to 1)
        'gamma_gen': 0.6, # Weighting parameter for general skills (rewards more heavily)
        'gamma_spec': 0.4, # Weighting parameter for firm-specific skills
        'w_econ': 0.5, # Calibration weight for economic modifier
        'w_inno': 0.5, # Calibration weight for AI innovation index
        'beta_systemic': 0.10, # Base annual probability of systemic event in highest-risk industry
        'beta_individual': 0.50, # Base conditional probability of job loss for most vulnerable person
        'lambda_loading': 1.5, # Loading Factor for premium
        'P_min': 20.00, # Minimum monthly premium
        'TTV_default': 12 # Default Time-to-Value period in months
    }
