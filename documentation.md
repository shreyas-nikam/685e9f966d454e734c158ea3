id: 685e9f966d454e734c158ea3_documentation
summary: AI Risk Score - V4-2 Documentation
feedback link: https://docs.google.com/forms/d/e/1FAIpQLSfWkOK-in_bMMoHSZfcIvAeO58PAH9wrDqcxnJABHaxiDqhSA/viewform?usp=sf_link
environments: Web
status: Published
# AI Risk Score - Career Path Diversification Tool Codelab

This codelab provides a comprehensive guide to understanding and utilizing the "AI Risk Score - Career Path Diversification Tool." This application helps users assess and mitigate their career risk due to AI-driven job displacement. You'll learn about the key concepts behind the application, the formulas used, and how to interpret the results.  This tool is valuable for anyone wanting to understand and proactively manage their career in the face of increasing automation.

## Understanding the Core Concepts
Duration: 00:10

Before diving into the code, let's define the core concepts:

*   **Idiosyncratic Risk ($V_i(t)$):**  This is the individual-specific risk, influenced by factors like skills, education, experience, and company stability. It's something you can directly influence.

*   **Systematic Risk ($H_i$):** This is the macro-level risk associated with an occupation or industry, influenced by economic conditions and the pace of AI innovation. It's harder to control directly but can be managed through career diversification.

*   **Career Path Diversification:** Strategically transitioning to roles or industries with lower inherent AI hazard to mitigate systematic risk.

*   **Time-to-Value (TTV):** The time it takes to fully realize the benefits (reduced risk) of a career transition.

## Application Architecture
Duration: 00:05

The application follows a modular structure:

*   **`app.py`:**  The main Streamlit application, handling the user interface and orchestrating the calculations and visualizations.

*   **`data_utils.py`:**  Loads and provides the data needed for the calculations, including job data, education factors, and actuarial parameters.

*   **`calculations.py`:**  Contains the functions for calculating the various risk scores and insurance premiums.

*   **`visualization.py`:**  Generates the plots and charts used to visualize the risk scores and their components.

<aside class="positive">
This modular structure makes the application easy to understand, maintain, and extend.  Each module has a clear responsibility, promoting code reusability and testability.
</aside>

## Setting up the Environment
Duration: 00:05

1.  Make sure you have Python installed (version 3.7 or higher).
2.  Install the necessary libraries:

```console
pip install streamlit pandas numpy plotly
```

3.  Create the files `app.py`, `data_utils.py`, `calculations.py`, and `visualization.py` and copy the code provided into them.

## Exploring `data_utils.py`
Duration: 00:15

This module is responsible for loading and providing the data used in the application. Let's examine the key functions:

*   **`load_job_data()`:**  This function creates a Pandas DataFrame containing synthetic data for various job roles, including their base AI hazard scores (`H_base`) and role multipliers (`f_role`).

```python
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
```

*   **`load_education_data()`:** Returns dictionaries containing factors for different education levels and fields.  These factors influence the Human Capital Factor (FHC).

```python
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
```

*   **`load_school_tier_data()`:**  Returns a dictionary containing factors for different institution tiers, also impacting the FHC.

```python
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
```

*   **`load_company_type_data()`:**  Returns a DataFrame containing risk factors associated with different company types (e.g., "Big firm," "Startup"). These factors influence the Company Risk Factor (FCR).

```python
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
```

*   **`load_default_actuarial_parameters()`:** Returns a dictionary containing default values for various actuarial and environmental parameters used in the calculations.

```python
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
```
*   **`get_factor_value()`:** Helper function to safely retrieve values from DataFrames.
*   **`get_dict_value()`:** Helper function to safely retrieve values from Dictionaries.

## Diving into `calculations.py`
Duration: 00:30

This module houses the functions responsible for performing the core calculations of the application.  Understanding these functions is key to understanding how the risk scores are derived.

*   **`calculate_f_exp(years_experience)`:** Calculates the Experience Factor ($f_{exp}$), which decreases the Human Capital Factor (FHC) as experience increases (representing potential skill obsolescence).
    *   Formula:  $f_{exp} = 1 - (a \cdot \min(Y_i, Y_{cap}))$
    *   `a`: Decay constant (`params["a_exp"]`).
    *   `Yi`: Years of experience.
    *   `Y_cap`: Capped years of experience (`params["Y_cap"]`).

```python
def calculate_f_exp(years_experience):
    """
    Calculate the Experience Factor ($f_{exp}$).
    Formula: $f_{exp} = 1 - (a \cdot \min(Y_i, Y_{cap}))$
    """
    a = params["a_exp"]
    Y_cap = params["Y_cap"]
    f_exp = 1 - (a * min(years_experience, Y_cap))
    return max(0.1, f_exp) # Ensure f_exp doesn't go too low
```

*   **`calculate_fhc(job_title, education_level, education_field, school_tier, years_experience)`:** Calculates the Human Capital Factor (FHC) based on various factors related to the individual's background and experience.
    *   Formula: $FHC = f_{role} \cdot f_{level} \cdot f_{field} \cdot f_{school} \cdot f_{exp}$

```python
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
```

*   **`calculate_fcr(company_type)`:**  Calculates the Company Risk Factor (FCR) based on sentiment, financial health, and growth factors associated with the individual's employer.
    *   Formula:  $FCR = w_1 \cdot S_{senti} + w_2 \cdot S_{fin} + w_3 \cdot S_{growth}$

```python
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
```

*   **`calculate_fus(gen_skill_progress, firm_skill_progress)`:** Calculates the Upskilling Factor (FUS), which reflects the individual's efforts to acquire new skills. General skills are weighted more heavily than firm-specific skills.
    *   Formula: $FUS = 1 - (\gamma_{gen} P_{gen}(t) + \gamma_{spec} P_{spec}(t))$

```python
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
```

*   **`calculate_v_raw(FHC, FCR, FUS)`:** Calculates the Raw Idiosyncratic Risk ($V_{raw}$) based on the Human Capital Factor, Company Risk Factor, and Upskilling Factor.
    *   Formula: $V_{raw} = FHC \cdot (w_{CR} FCR + w_{US} FUS)$

```python
def calculate_v_raw(FHC, FCR, FUS):
    """
    Calculate the Raw Idiosyncratic Risk ($V_{raw}$).
    Formula: $V_{raw} = FHC \cdot (w_{CR} FCR + w_US FUS)$
    """
    w_CR = params["w_CR"]
    w_US = params["w_US"]

    V_raw = FHC * (w_CR * FCR + w_US * FUS)
    return V_raw
```

*   **`calculate_idiosyncratic_risk(V_raw)`:**  Calculates the Idiosyncratic Risk ($V_i(t)$) by normalizing the Raw Idiosyncratic Risk score.
    *   Formula:  $V_i(t) = \min(100.0, \max(5.0, V_{raw} - 50.0))$

```python
def calculate_idiosyncratic_risk(V_raw):
    """
    Calculate the Idiosyncratic Risk ($V_i(t)$).
    Formula: $V_i(t) = \min(100.0, \max(5.0, V_{raw} - 50.0))$
    """
    V_i_t = min(100.0, max(5.0, V_raw - 50.0))
    return V_i_t
```

*   **`calculate_h_base_ttv(k, ttv, h_current, h_target)`:** Calculates the Time-to-Value (TTV) Modified Base Occupational Hazard ($H_{base}(k)$) during a career transition.
    *   Formula: $H_{base}(k) = \left(1 - \frac{k}{TTV}\right) H_{current} + \left(\frac{k}{TTV}\right) H_{target}$

```python
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
```

*   **`calculate_systematic_risk(h_base_t, m_econ, iai)`:** Calculates the Systematic Risk ($H_i$) based on the base hazard of the occupation, the economic climate modifier, and the AI innovation index.
    *   Formula: $H_i = H_{base}(t) \cdot (w_{econ} M_{econ} + w_{inno} IAI)$

```python
def calculate_systematic_risk(h_base_t, m_econ, iai):
    """
    Calculate the Systematic Risk ($H_i$).
    Formula: $H_i = H_{base}(t) \cdot (w_{econ} M_{econ} + w_{inno} IAI)$
    """
    w_econ = params["w_econ"]
    w_inno = params["w_inno"]

    H_i = h_base_t * (w_econ * m_econ + w_inno * iai)
    return H_i
```

*   **`calculate_p_systemic(H_i)`:** Calculates the Systemic Event Base Probability ($P_{systemic}$).
    *   Formula: $P_{systemic} = \frac{H_i}{100} \cdot \beta_{systemic}$

```python
def calculate_p_systemic(H_i):
    """
    Calculate the Systemic Event Base Probability ($P_{systemic}$).
    Formula: $P_{systemic} = \frac{H_i}{100} \cdot \beta_{systemic}$
    """
    beta_systemic = params["beta_systemic"]
    P_systemic = (H_i / 100.0) * beta_systemic
    return P_systemic
```

*   **`calculate_p_individual_systemic(V_i_t)`:** Calculates the Individual Loss Base Probability ($P_{individual|systemic}$).
    *   Formula: $P_{individual|systemic} = \frac{V_i(t)}{100} \cdot \beta_{individual}$

```python
def calculate_p_individual_systemic(V_i_t):
    """
    Calculate the Individual Loss Base Probability ($P_{individual|systemic}$).
    Formula: $P_{individual|systemic} = \frac{V_i(t)}{100} \cdot \beta_{individual}$
    """
    beta_individual = params["beta_individual"]
    P_individual_systemic = (V_i_t / 100.0) * beta_individual
    return P_individual_systemic
```

*   **`calculate_p_claim(P_systemic, P_individual_systemic)`:** Calculates the Annual Claim Probability ($P_{claim}$).
    *   Formula: $P_{claim} = P_{systemic} \cdot P_{individual|systemic}$

```python
def calculate_p_claim(P_systemic, P_individual_systemic):
    """
    Calculate the Annual Claim Probability ($P_{claim}$).
    Formula: $P_{claim} = P_{systemic} \cdot P_{individual|systemic}$
    """
    P_claim = P_systemic * P_individual_systemic
    return P_claim
```

*   **`calculate_l_payout(annual_salary, coverage_duration_months, coverage_percentage)`:** Calculates the Total Payout Amount ($L_{payout}$).
    *   Formula: $L_{payout} = \left( \frac{\text{Annual Salary}}{12} \right) \cdot \text{Coverage Duration} \cdot \text{Coverage Percentage}$

```python
def calculate_l_payout(annual_salary, coverage_duration_months, coverage_percentage):
    """
    Calculate the Total Payout Amount ($L_{payout}$).
    Formula: $L_{payout} = \left( \frac{\text{Annual Salary}}{12} \right) \cdot \text{Coverage Duration} \cdot \text{Coverage Percentage}$
    """
    L_payout = (annual_salary / 12.0) * coverage_duration_months * (coverage_percentage / 100.0)
    return L_payout
```

*   **`calculate_expected_loss(P_claim, L_payout)`:** Calculates the Annual Expected Loss ($E[Loss]$).
    *   Formula: $E[Loss] = P_{claim} \cdot L_{payout}$

```python
def calculate_expected_loss(P_claim, L_payout):
    """
    Calculate the Annual Expected Loss ($E[Loss]$).
    Formula: $E[Loss] = P_{claim} \cdot L_{payout}$
    """
    E_Loss = P_claim * L_payout
    return E_Loss
```

*   **`calculate_monthly_premium(E_Loss)`:** Calculates the Monthly Insurance Premium ($P_{monthly}$).
    *   Formula: $P_{monthly} = \max \left( \frac{E[Loss] \cdot \lambda}{12}, P_{min} \right)$

```python
def calculate_monthly_premium(E_Loss):
    """
    Calculate the Monthly Insurance Premium ($P_{monthly}$).
    Formula: $P_{monthly} = \max \left( \frac{E[Loss] \cdot \lambda}{12}, P_{min} \right)$
    """
    loading_factor = params["loading_factor"]
    min_premium = params["min_premium"]

    P_monthly = max((E_Loss * loading_factor) / 12.0, min_premium)
    return P_monthly
```

*   **`get_h_base_for_job(job_title)`:** Helper function to retrieve the base hazard for a specific job.

## Visualizing Risk with `visualization.py`
Duration: 00:15

This module provides functions to create informative visualizations of the calculated risk scores.

*   **`plot_systematic_risk_evolution(simulation_data)`:** Generates a line chart showing the evolution of Systematic Risk during a career transition.  This plot is key to understanding the impact of Career Path Diversification.

```python
import plotly.express as px
import pandas as pd

def plot_systematic_risk_evolution(simulation_data):
    """
    Generates a Plotly line chart showing the simulated Systematic Risk evolution
    over a career transition period.

    Args:
        simulation_data (pd.DataFrame): DataFrame with 'Month' and 'Systematic Risk' columns.
    """
    fig = px.line(
        simulation_data,
        x="Month",
        y="Systematic Risk",
        title="Systematic Risk Evolution During Career Transition",
        labels={"Month": "Months Elapsed Since Transition Start", "Systematic Risk": "Systematic Risk Score ($H_i$)"},
        markers=True,
        line_shape="linear"
    )

    fig.update_layout(
        hovermode="x unified",
        xaxis_title="Months Elapsed Since Transition Started ($k$)",
        yaxis_title="Systematic Risk Score ($H_i$)"
    )

    fig.update_traces(
        hovertemplate=\"\"\"<b>Month:</b> %{x}<br>
<b>Systematic Risk ($H_i$):</b> %{y:.2f}
<extra></extra>\"\"\"
    )
    return fig
```

*   **`plot_factor_contributions_v_raw(FHC, FCR, FUS, w_CR, w_US)`:**  Generates a bar chart showing the relative contributions of the Human Capital Factor (FHC), Company Risk Factor (FCR), and Upskilling Factor (FUS) to the Raw Idiosyncratic Risk ($V_{raw}$).  This helps users understand which factors are most heavily influencing their individual risk.

```python
def plot_factor_contributions_v_raw(FHC, FCR, FUS, w_CR, w_US):
    """
    Generates a Plotly bar chart showing contributions of FHC, FCR, FUS to V_raw.
    """
    # V_raw = FHC * (w_CR * FCR + w_US * FUS)
    # To represent contributions, we can show relative impact or just the weighted components.
    # For a simplified visualization of relative impact, let's consider the components
    # that form the sum inside the parenthesis, scaled by FHC.
    
    data = {
        'Factor Component': ['Human Capital (FHC)', 'Company Risk (FCR)', 'Upskilling (FUS)'],
        'Value': [FHC, FCR * FHC, FUS * FHC] # Scaling by FHC to show their multiplicative effect
    }
    df = pd.DataFrame(data)

    fig = px.bar(df, x='Factor Component', y='Value',
                 title='Relative Contribution of Factors to Raw Idiosyncratic Risk (Scaled)',
                 labels={'Value': 'Contribution Value', 'Factor Component': 'Risk Factor'},
                 color='Factor Component') # Differentiate bars by color
    
    fig.update_layout(
        yaxis_title="Scaled Factor Value (Higher = More Risk)"
    )
    
    return fig
```

*   **`plot_factor_contributions_hi(H_base, M_econ, IAI, w_econ, w_inno)`:** Generates a bar chart showing the contributions of the Base Occupational Hazard ($H_{base}$), Economic Climate Modifier ($M_{econ}$), and AI Innovation Index ($IAI$) to the Systematic Risk ($H_i$).

```python
def plot_factor_contributions_hi(H_base, M_econ, IAI, w_econ, w_inno):
    """
    Generates a Plotly bar chart showing contributions of H_base, M_econ, IAI to H_i.
    """
    # H_i = H_base * (w_econ * M_econ + w_inno * IAI)
    # We can show the H_base and then the weighted modifiers' impact.
    
    data = {
        'Component': ['Base Hazard ($H_{base}$)', 'Economic Modifier ($M_{econ}$)', 'AI Innovation ($IAI$)'],
        'Value': [H_base, H_base * w_econ * M_econ, H_base * w_inno * IAI]
    }
    df = pd.DataFrame(data)

    fig = px.bar(df, x='Component', y='Value',
                 title='Relative Contribution to Systematic Risk ($H_i$) Components',
                 labels={'Value': 'Contribution Value', 'Component': 'Systematic Risk Component'},
                 color='Component')
    
    fig.update_layout(
        yaxis_title="Scaled Component Value (Higher = More Risk)"
    )

    return fig
```

## Understanding `app.py` - The Main Application
Duration: 00:30

This file contains the Streamlit application logic, bringing together the data, calculations, and visualizations.

1.  **Import Libraries:**  The necessary libraries are imported, including Streamlit, Pandas, and the custom modules.

```python
import streamlit as st
import pandas as pd
from data_utils import load_job_data, load_education_data, load_school_tier_data, load_company_type_data, load_default_actuarial_parameters
from calculations import (
    calculate_fhc, calculate_fcr, calculate_fus, calculate_v_raw,
    calculate_idiosyncratic_risk, calculate_h_base_ttv, calculate_systematic_risk,
    calculate_p_systemic, calculate_p_individual_systemic, calculate_p_claim,
    calculate_l_payout, calculate_expected_loss, calculate_monthly_premium,
    get_h_base_for_job
)
from visualization import plot_systematic_risk_evolution, plot_factor_contributions_v_raw, plot_factor_contributions_hi
```

2.  **App Configuration:** Basic Streamlit configurations are set, such as page title and layout.

```python
st.set_page_config(page_title="QuLab - AI Risk Score - V4-2", layout="wide")
st.sidebar.image("https://www.quantuniversity.com/assets/img/logo5.jpg")
st.sidebar.divider()
st.title("AI Risk Score - V4-2")
```

3.  **Introduction:** Introductory text is displayed to explain the purpose of the application.

```python
st.markdown("""
In this lab, the **AI Risk Score - V4-2: Career Path Diversification Tool** is designed to help users understand
and mitigate their exposure to systematic AI risk in their careers. Inspired by the principles of risk management,
this application allows you to explore how different career choices and personal development efforts
influence your AI displacement risk profile and potential insurance premiums.

### Understanding AI Displacement Risk
AI displacement risk can be broadly categorized into two types:

1.  **Idiosyncratic Risk ($V_i(t)$):** This refers to individual-specific vulnerabilities that are largely within
    your control. Factors like your skills, education, experience, and even your current employer's stability
    contribute to this risk. Proactive measures, such as continuous learning and skill diversification,
    can effectively mitigate idiosyncratic risk.

2.  **Systematic Risk ($H_i$):** This represents the macro-level automation hazard inherent to an entire occupation
    or industry. It's influenced by broader environmental conditions like the economic climate and the pace of AI
    innovation. While harder to control directly, systematic risk can be managed through **Career Path Diversification**,
    i.e., strategically transitioning to roles or industries with lower inherent AI hazard.

### How This Tool Helps
This application simulates the impact of various inputs on your risk scores and a hypothetical insurance premium
designed to cover potential income loss due to AI-driven job displacement. By interacting with the inputs,
you can gain a clear understanding of:

*   How individual factors (Human Capital, Company Stability, Upskilling) shape your Idiosyncratic Risk.
*   How external factors (Economic Climate, AI Innovation) influence your Systematic Risk.
*   The financial implications (potential insurance premium) of your risk profile.
*   The power of **Career Path Diversification** in reducing systematic risk over time, demonstrated through
    the "Time-to-Value (TTV)" simulation.

Let's explore how your career path, skills, and strategic choices can act as a form of "insurance" against AI risk.
""")
```

4.  **Data Loading:** The data is loaded using the functions from `data_utils.py`.  This is done once and stored in `st.session_state` for efficiency.

```python
# Load all data and parameters once and store in session state
if 'job_data' not in st.session_state:
    st.session_state.job_data = load_job_data()
    st.session_state.education_level_data, st.session_state.education_field_data = load_education_data()
    st.session_state.school_tier_data = load_school_tier_data()
    st.session_state.company_type_data = load_company_type_data()
    st.session_state.params = load_default_actuarial_parameters()

job_data = st.session_state.job_data
education_level_data = st.session_state.education_level_data
education_field_data = st.session_state.education_field_data
school_tier_data = st.session_state.school_tier_data
company_type_data = st.session_state.company_type_data
params = st.session_state.params
```

5.  **Sidebar Inputs:** The sidebar is populated with input widgets using Streamlit.  These inputs allow the user to configure their profile, upskilling efforts, and actuarial parameters.

