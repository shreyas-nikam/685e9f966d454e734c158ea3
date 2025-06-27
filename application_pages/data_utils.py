
import pandas as pd
import numpy as np

def load_job_data():
    # O*NET-like data for job roles and their intrinsic AI hazard scores (H_base)
    # and f_role multipliers
    return pd.DataFrame({
        'Job Title': [
            'Software Engineer', 'Data Scientist', 'Accountant', 'HR Manager',
            'Financial Analyst', 'Marketing Specialist', 'Customer Service Rep',
            'Truck Driver', 'Construction Worker', 'Nurse', 'Teacher',
            'Web Developer', 'Cybersecurity Analyst', 'Graphic Designer',
            'Sales Manager', 'Manufacturing Worker', 'Supply Chain Analyst',
            'Medical Doctor', 'Researcher', 'Legal Assistant'
        ],
        'H_base': [
            75, 85, 90, 60,  # High AI hazard for SE, DS, Accountant
            80, 70, 95, 50,  # High for CSR, FA, Marketing
            40, 30, 45, 65,  # Lower for Truck Driver, Construction, Nurse, Teacher
            70, 78, 60, 40,  # Web Dev, Cybersecurity, Graphic Design
            55, 35, 72, 25,  # Sales, Manufacturing, Supply Chain, Doctor
            88, 70           # Researcher, Legal Assistant
        ],
        'f_role': [
            0.6, 0.7, 0.8, 0.5, # Lower f_role means higher resilience for the role (closer to 0)
            0.75, 0.65, 0.9, 0.4,
            0.3, 0.25, 0.35, 0.55,
            0.6, 0.7, 0.45, 0.3,
            0.4, 0.2, 0.68, 0.22
        ]
    })

def load_education_data():
    # Lookup tables for Human Capital factors (f_level, f_field, f_school)
    return {
        'Education Level': {
            'PhD': 0.7, 'Master\'s': 0.8, 'Bachelor\'s': 0.9,
            'Associate\'s': 0.95, 'High School': 1.0
        },
        'Education Field': {
            'Tech/Engineering': 0.7, 'STEM (Non-Tech)': 0.75,
            'Business/Finance': 0.8, 'Healthcare': 0.6,
            'Humanities/Arts': 0.9, 'Social Sciences': 0.85
        },
        'Institution Tier': {
            'Tier 1': 0.7, 'Tier 2': 0.8, 'Tier 3': 0.9, 'Tier 4+': 1.0
        }
    }

def load_company_type_data():
    # Dummy data for Company Risk factors (S_senti, S_fin, S_growth) based on company types
    # Values are proxies for risk, lower means less risk
    return {
        'Big Firm': {'S_senti': 0.7, 'S_fin': 0.6, 'S_growth': 0.7},
        'Mid-size Firm': {'S_senti': 0.8, 'S_fin': 0.8, 'S_growth': 0.8},
        'Startup': {'S_senti': 0.9, 'S_fin': 0.95, 'S_growth': 0.9}, # Startups are riskier
        'Government/Non-Profit': {'S_senti': 0.6, 'S_fin': 0.5, 'S_growth': 0.6}
    }

def load_default_actuarial_parameters():
    # Default values for environmental modifiers (M_econ, IAI) and actuarial parameters
    return {
        'a_decay_constant': 0.015,  # for f_exp
        'Y_cap': 20,                # for f_exp
        'w_CR': 0.4,                # weight for Company Risk in V_raw
        'w_US': 0.6,                # weight for Upskilling in V_raw
        'gamma_gen': 0.7,           # weight for general skills in FUS
        'gamma_spec': 0.3,          # weight for firm-specific skills in FUS
        'w_econ': 0.5,              # weight for Economic Climate in H_i
        'w_inno': 0.5,              # weight for AI Innovation Index in H_i
        'beta_systemic': 0.10,      # base annual probability of systemic event
        'beta_individual': 0.50,    # base conditional probability of job loss
        'lambda_loading_factor': 1.5, # loading factor for premium
        'P_min': 20.0,              # minimum monthly premium
        'TTV_default': 12,          # default Time-to-Value period in months
        'M_econ_default': 1.0,      # default Economic Climate Modifier
        'IAI_default': 1.0          # default AI Innovation Index
    }

def get_job_hazard_and_role_factor(job_title):
    job_data = load_job_data()
    row = job_data[job_data['Job Title'] == job_title]
    if not row.empty:
        return row['H_base'].iloc[0], row['f_role'].iloc[0]
    return 70, 0.7 # Default if not found

def get_education_factor(level, field, school_tier):
    edu_data = load_education_data()
    f_level = edu_data['Education Level'].get(level, 1.0)
    f_field = edu_data['Education Field'].get(field, 1.0)
    f_school = edu_data['Institution Tier'].get(school_tier, 1.0)
    return f_level, f_field, f_school

def get_company_risk_scores(company_type):
    comp_data = load_company_type_data()
    return comp_data.get(company_type, {'S_senti': 0.8, 'S_fin': 0.8, 'S_growth': 0.8}) # Default if not found
