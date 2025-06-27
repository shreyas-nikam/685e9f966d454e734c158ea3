
# Technical Specifications for a Streamlit Application: Career Path Diversification Tool

## Overview

The "Career Path Diversification Tool" is a Streamlit application designed to help users understand and mitigate their exposure to systematic AI risk in their careers. Inspired by concepts from the provided document, the application allows users to explore how different career choices and personal development efforts influence their AI displacement risk profile and potential insurance premiums. It focuses on illustrating "Systematic Risk Exposure Mitigation" or "Career Path Diversification" by simulating the impact of career transitions and skill acquisition on an individual's overall risk score.

The application will transform raw synthetic data into interactive visualizations, providing detailed insights and explanations directly on the charts. Users will be able to interact with input forms and widgets to experiment with various parameters and observe real-time updates, thereby gaining a clear understanding of key concepts such as Idiosyncratic Risk, Systematic Risk, and their implications for career resilience.

## Step-by-Step Development Process

The development of the "Career Path Diversification Tool" will follow a structured approach to ensure all functional requirements are met efficiently.

1.  **Environment Setup and Dependency Installation:**
    *   Create a dedicated Python virtual environment.
    *   Install core libraries: `streamlit`, `pandas`, `numpy`, `plotly`.
    *   Structure the project directory with `app.py`, `calculations.py`, `data_utils.py`, and `visualization.py` files.

2.  **Data Generation and Ingestion:**
    *   **Synthetic Dataset Creation:** Generate in-memory Python dictionaries or Pandas DataFrames to mimic the "Synthetic Dataset" described, including:
        *   O\*NET-like data for job roles and their intrinsic AI hazard scores ($H_{base}$).
        *   Lookup tables for Human Capital factors ($f_{role}, f_{level}, f_{field}, f_{school}, f_{exp}$ parameters).
        *   Dummy data for Company Risk factors ($S_{senti}, S_{fin}, S_{growth}$) based on company types (e.g., "Big firm," "Mid-size firm," "Startup").
        *   Default values for environmental modifiers ($M_{econ}, IAI$) and actuarial parameters ($\beta_{systemic}, \beta_{individual}, \lambda, P_{min}$).
    *   **Data Loaders:** Implement functions in `data_utils.py` to load these synthetic datasets and lookup tables into memory for use by the application.

3.  **Core Calculation Logic Implementation:**
    *   **Module `calculations.py`:** Implement Python functions for each mathematical formula identified in the "Core Concepts" section.
        *   Functions for calculating $FHC$, $FCR$, $FUS$.
        *   Function for calculating $V_i(t)$ (Idiosyncratic Risk).
        *   Functions for calculating $H_{base}(t)$ (including TTV modification) and $H_i$ (Systematic Risk).
        *   Functions for calculating $L_{payout}$, $P_{claim}$, $E[Loss]$, and $P_{monthly}$.
    *   Ensure proper handling of inputs and outputs, and adherence to the mathematical definitions.

4.  **User Interface (UI) Design and Implementation:**
    *   **Module `app.py`:** Set up the Streamlit application layout.
    *   **Input Forms:** Create sidebar or main panel sections using `st.sidebar`, `st.columns`, `st.expander` to collect user data:
        *   Current career details: `st.selectbox` for job title, education level/field, `st.number_input` for experience, `st.selectbox` for company type.
        *   Upskilling progress: `st.slider` for general and firm-specific training progress.
        *   Career Transition: `st.checkbox` for transition status, `st.selectbox` for target career/industry, `st.number_input` for TTV period and elapsed months.
        *   Actuarial parameters: `st.number_input` for annual salary, coverage percentage, duration, loading factor, minimum premium.
        *   Environmental modifiers: `st.slider` or `st.number_input` for $M_{econ}$ and $IAI$ (allowing users to explore their impact).
    *   **Output Display:** Use `st.metric`, `st.write`, `st.info` to display calculated risk scores, premium, and intermediate values.
    *   **Interactive Visualizations:** Integrate `plotly.express` charts for displaying trends (e.g., risk score reduction over transition period) and correlations.

5.  **Interactivity and Simulation Logic:**
    *   Implement `st.session_state` to manage user inputs and maintain calculation results across reruns, enabling dynamic updates.
    *   Add logic to trigger recalculations when input parameters change.
    *   Simulate career transition: When a user selects a target career path, display the projected $H_i$ reduction over the $TTV$ period using a line chart.

6.  **Documentation and Explanations:**
    *   **Inline Help:** Use `st.help`, `st.expander`, `st.info`, and `st.tooltip` (available in `st.help` and some widgets) to provide context and definitions for inputs and outputs.
    *   **Concept Explanation:** Use `st.markdown` with detailed explanations (following the specified LaTeX template) for each core mathematical concept, reinforcing the "Learning Outcomes" and how the application explains "Systematic Risk Exposure Mitigation."

7.  **Testing and Refinement:**
    *   Test calculations with example personas (e.g., "Alex Chen," "Dr. Brenda Smith" from the document's appendix) to validate correctness.
    *   Refine UI layout and user experience based on iterative testing.

## Core Concepts and Mathematical Foundations

This section details the fundamental mathematical models and concepts implemented in the application, all derived from the provided document.

### Idiosyncratic Risk ($V_i(t)$)
The Idiosyncratic Risk, or Vulnerability, quantifies an individual's specific vulnerability to job displacement, reflecting factors within their direct control. It is calculated using:
$$
V_i(t) = \min(100.0, \max(5.0, V_{raw} - 50.0))
$$
Where:
- $V_i(t)$: The final Idiosyncratic Risk score at time $t$.
- $V_{raw}$: The raw (unnormalized) Idiosyncratic Risk score.

This formula normalizes the raw idiosyncratic risk score to a predefined range (e.g., 5-100), ensuring the score remains within an interpretable scale, making it consistent and comparable.

### Raw Idiosyncratic Risk ($V_{raw}$)
The raw Idiosyncratic Risk Score is an intermediate calculation before normalization, combining key individual-specific factors. It is calculated using:
$$
V_{raw} = FHC \cdot (w_{CR} FCR + w_{US} FUS)
$$
Where:
- $V_{raw}$: Raw Idiosyncratic Risk Score.
- $FHC$: Human Capital Factor, assessing foundational resilience.
- $FCR$: Company Risk Factor, assessing employer stability.
- $FUS$: Upskilling Factor, assessing proactive training efforts.
- $w_{CR}$: Weight assigned to the Company Risk Factor (e.g., 0.4).
- $w_{US}$: Weight assigned to the Upskilling Factor (e.g., 0.6).

This formula combines the Human Capital, Company Risk, and Upskilling factors, weighted according to their importance, to derive an initial unnormalized vulnerability score that reflects an individual's total manageable risk.

### Human Capital Factor ($FHC$)
The Human Capital Factor assesses an individual's foundational resilience based on their educational and professional background. It is calculated as a weighted product of several sub-factors:
$$
FHC = f_{role} \cdot f_{level} \cdot f_{field} \cdot f_{school} \cdot f_{exp}
$$
Where:
- $FHC$: Human Capital Factor.
- $f_{role}$: Role Multiplier, representing inherent job title vulnerability.
- $f_{level}$: Education Level Factor, based on highest education attained.
- $f_{field}$: Education Field Factor, rewarding transferable and in-demand skills.
- $f_{school}$: Institution Tier Factor, a proxy for training quality and network.
- $f_{exp}$: Experience Factor, a decaying function of years of experience.

This factor is a multiplicative combination of sub-factors reflecting various aspects of human capital, providing a comprehensive assessment of an individual's intrinsic resilience against job displacement.

### Experience Factor ($f_{exp}$)
The Experience Factor models how an individual's years of professional experience influence their vulnerability, accounting for diminishing returns. It is calculated using:
$$
f_{exp} = 1 - (a \cdot \min(Y_i, Y_{cap}))
$$
Where:
- $f_{exp}$: Experience Factor.
- $a$: Decay constant (e.g., 0.015, as per document example).
- $Y_i$: Years of experience of the individual.
- $Y_{cap}$: Capped years of experience (e.g., 20, as per document example).

This decaying function captures the principle that professional experience reduces vulnerability, but with diminishing returns after a certain point, reflecting that excessive experience beyond a cap offers diminishing additional risk reduction benefits.

### Company Risk Factor ($FCR$)
The Company Risk Factor quantifies the stability and growth prospects of the individual's current employer, analogous to a corporate credit rating. It is calculated using:
$$
FCR = w_1 \cdot S_{senti} + w_2 \cdot S_{fin} + w_3 \cdot S_{growth}
$$
Where:
- $FCR$: Company Risk Factor.
- $S_{senti}$: Sentiment Score, derived from real-time NLP analysis of news concerning the company.
- $S_{fin}$: Financial Health Score, based on company's financial statements (e.g., 10-K, 10-Q filings).
- $S_{growth}$: Growth & AI-Adoption Score, based on analyst reports and R&D spending.
- $w_1, w_2, w_3$: Weights summing to 1.0 (e.g., 0.33 each for simplicity, assuming equal weighting unless otherwise specified).

This factor provides a comprehensive assessment of the employer's stability and proactive adaptation to AI, which directly impacts the employee's displacement risk.

### Upskilling Factor ($FUS$)
The Upskilling Factor differentiates between skill types, rewarding portable skills more heavily, and reflects the impact of an individual's proactive training efforts. It is calculated using:
$$
FUS = 1 - (\gamma_{gen} P_{gen}(t) + \gamma_{spec} P_{spec}(t))
$$
Where:
- $FUS$: Upskilling Factor.
- $P_{gen}(t)$: The individual's training progress (from 0 to 1) in general or "portable" skills.
- $P_{spec}(t)$: The individual's training progress (from 0 to 1) in "firm-specific" skills.
- $\gamma_{gen}$: Weighting parameter for general skills.
- $\gamma_{spec}$: Weighting parameter for firm-specific skills (where $\gamma_{gen} > \gamma_{spec}$ to reward portable skills more heavily).

This factor directly influences the Idiosyncratic Risk, reflecting that continuous learning and skill acquisition, especially in portable skills, can significantly reduce an individual's vulnerability.

### Systematic Risk ($H_i$)
The Systematic Risk score is a dynamic index reflecting the macro-level automation hazard of an occupation, adjusted by broader environmental conditions. It is calculated using:
$$
H_i = H_{base}(t) \cdot (w_{econ} M_{econ} + w_{inno} IAI)
$$
Where:
- $H_i$: The final Systematic Risk score at time $t$.
- $H_{base}(t)$: The Base Occupational Hazard for the occupation.
- $M_{econ}$: Economic Climate Modifier, a composite index reflecting macroeconomic environment.
- $IAI$: AI Innovation Index, a momentum indicator reflecting the velocity of technological change.
- $w_{econ}$: Calibration weight for the economic modifier (e.g., 0.5).
- $w_{inno}$: Calibration weight for the AI innovation index (e.g., 0.5).

This formula quantifies the unavoidable hazard inherent to an entire occupation, dynamically adjusting it based on the prevailing economic climate and the pace of AI innovation.

### Time-to-Value (TTV) Modified Base Occupational Hazard ($H_{base}(k)$)
The Base Occupational Hazard for an occupation can change over time, especially during a career transition. The TTV modifier for realism during transition is calculated using:
$$
H_{base}(k) = \left(1 - \frac{k}{TTV}\right) H_{current} + \left(\frac{k}{TTV}\right) H_{target}
$$
Where:
- $H_{base}(k)$: The Base Occupational Hazard score after $k$ months of transition.
- $k$: The number of months that have elapsed since the completion of the transition pathway.
- $TTV$: The total number of months in the Time-to-Value period (e.g., 12 months).
- $H_{current}$: The Base Occupational Hazard score of the individual's original industry.
- $H_{target}$: The Base Occupational Hazard score of the new target industry.

This formula models the gradual reduction in systematic risk as an individual transitions to a lower-risk occupation. It showcases the concept of "Career Path Diversification" by demonstrating how systematic risk can be actively mitigated over time.

### Annual Claim Probability ($P_{claim}$)
The annual probability of a job displacement claim is modeled as the joint probability of a systemic event occurring in the individual's industry and that event leading to a loss for that specific individual. It is calculated using:
$$
P_{claim} = P_{systemic} \cdot P_{individual|systemic}
$$
Where:
- $P_{claim}$: The annual probability of a claim.
- $P_{systemic}$: The probability of a systemic event occurring in the individual's industry.
- $P_{individual|systemic}$: The conditional probability of individual job loss given a systemic event.

This formula is a core component of the risk calculation, translating the Idiosyncratic and Systematic Risk scores into a combined probability of job displacement for the individual in a given year.

### Systemic Event Base Probability ($P_{systemic}$)
The Systemic Event Base Probability converts the Systematic Risk score into a probability of a systemic displacement event occurring. It is calculated using:
$$
P_{systemic} = \frac{H_i}{100} \cdot \beta_{systemic}
$$
Where:
- $P_{systemic}$: The probability of a systemic displacement event affecting the individual's industry.
- $H_i$: The Systematic Risk Score.
- $\beta_{systemic}$: A calibrated actuarial parameter representing the base annual probability of a systemic displacement event in the highest-risk industry (e.g., 0.10).

This formula scales the systematic risk score into a concrete probability, anchoring it to a realistic baseline frequency for industry-wide displacement events.

### Individual Loss Base Probability ($P_{individual|systemic}$)
The Individual Loss Base Probability given a Systemic Event quantifies the conditional likelihood of an individual's job loss if a systemic event has occurred. It is calculated using:
$$
P_{individual|systemic} = \frac{V_i(t)}{100} \cdot \beta_{individual}
$$
Where:
- $P_{individual|systemic}$: The conditional probability of job loss for the individual, given a systemic event has occurred.
- $V_i(t)$: The Idiosyncratic Risk Score.
- $\beta_{individual}$: A calibrated actuarial parameter representing the base conditional probability of job loss for the most vulnerable person (e.g., 0.50).

This formula translates the individual's vulnerability score into a conditional probability of job loss, reflecting how personal factors influence the outcome during a systemic event.

### Annual Expected Loss ($E[Loss]$)
The Annual Expected Loss represents the total payout amount multiplied by the probability of a claim, providing a financial quantification of risk. It is calculated using:
$$
E[Loss] = P_{claim} \cdot L_{payout}
$$
Where:
- $E[Loss]$: The Annual Expected Financial Loss.
- $P_{claim}$: The Annual Claim Probability.
- $L_{payout}$: The Total Potential Payout Amount if a claim is triggered.

This formula is crucial for converting a probability of an event into a tangible financial impact, forming the basis for premium determination.

### Total Payout Amount ($L_{payout}$)
The Total Payout Amount represents the financial benefit defined by the policy terms that would be paid out if a claim is triggered. It is calculated using:
$$
L_{payout} = \left( \frac{\text{Annual Salary}}{12} \right) \cdot \text{Coverage Duration} \cdot \text{Coverage Percentage}
$$
Where:
- $L_{payout}$: The total financial benefit paid out in case of a claim.
- $\text{Annual Salary}$: The user's annual salary.
- $\text{Coverage Duration}$: The duration of coverage in months (e.g., 6 months).
- $\text{Coverage Percentage}$: The percentage of salary covered by the policy (e.g., 25%).

This formula determines the maximum financial benefit an individual would receive if job displacement occurs, directly impacting the scale of the potential loss.

### Monthly Insurance Premium ($P_{monthly}$)
The Monthly Insurance Premium is the final financial output, translating the expected loss into a periodic payment. It is calculated using:
$$
P_{monthly} = \max \left( \frac{E[Loss] \cdot \lambda}{12}, P_{min} \right)
$$
Where:
- $P_{monthly}$: The final Monthly Insurance Premium.
- $E[Loss]$: The Annual Expected Financial Loss.
- $\lambda$: Loading Factor, a standard insurance multiplier to cover administrative costs, operational expenses, and profit margin (e.g., 1.5).
- $P_{min}$: Minimum monthly premium to ensure policy viability (e.g., $20.00).

This formula ensures the premium covers the expected losses and operational costs, while also setting a floor to maintain policy viability, effectively operationalizing the "Education is Insurance" concept.

## Required Libraries and Dependencies

The Streamlit application will utilize the following Python libraries:

-   **`streamlit`**:
    *   **Role**: The core framework for building the interactive web application, handling UI components, layout, and reactivity.
    *   **Specific Functions/Modules Used**:
        *   `st.sidebar`, `st.columns`, `st.tabs`, `st.expander`: For structuring the layout and organizing inputs/outputs.
        *   `st.text_input`, `st.number_input`, `st.selectbox`, `st.slider`, `st.checkbox`: For user input widgets to collect career details, upskilling progress, and simulation parameters.
        *   `st.write`, `st.markdown`, `st.header`, `st.subheader`: For displaying text, titles, and formatted explanations of concepts and results.
        *   `st.metric`: For displaying key performance indicators like risk scores and premium values with clear labels.
        *   `st.plotly_chart`: For embedding interactive Plotly visualizations.
        *   `st.info`, `st.warning`, `st.success`: For conveying informative messages to the user.
        *   `st.session_state`: For managing the application's state across reruns, preserving user inputs and calculation results.
        *   `st.tooltip` (implicitly used by some widgets through `help` parameter) and `st.help`: For providing inline documentation and guidance.
    *   **Import Statement**: `import streamlit as st`

-   **`pandas`**:
    *   **Role**: Used for efficient data manipulation, especially for handling the synthetic datasets (e.g., O\*NET-like job data, factor lookup tables) and structuring them as DataFrames.
    *   **Specific Functions/Modules Used**:
        *   `pd.DataFrame`: To create and manage tabular data for synthetic job roles, their baseline hazard scores, and multipliers for human capital factors.
        *   `df.loc`, `df.query`: For looking up specific values (e.g., $H_{base}$ for a selected job role, $f_{role}$ for a given job title).
    *   **Import Statement**: `import pandas as pd`

-   **`numpy`**:
    *   **Role**: Provides numerical computing capabilities, particularly for mathematical operations like `min`, `max`, and general array operations that might be involved in calculations.
    *   **Specific Functions/Modules Used**:
        *   `np.min`, `np.max`: For normalizing risk scores as per the $V_i(t)$ formula.
        *   Other mathematical functions if needed (e.g., `np.power` for more complex exponential decay if $f_{exp}$ was different).
    *   **Import Statement**: `import numpy as np`

-   **`plotly.express`**:
    *   **Role**: For creating interactive and dynamic visualizations to display trends (e.g., risk score evolution during transition) and correlations.
    *   **Specific Functions/Modules Used**:
        *   `px.line`: To visualize the simulated reduction in systematic risk over the career transition period.
        *   `px.bar`: Potentially for comparing factor contributions or risk scores across different scenarios.
        *   `fig.update_layout`, `fig.update_traces`: For customizing chart appearance, adding annotations, and tooltips.
    *   **Import Statement**: `import plotly.express as px`

## Implementation Details

The application's internal structure will be organized into logical modules to promote maintainability and clarity.

### Module Structure

-   **`app.py`**:
    *   Main Streamlit application entry point.
    *   Handles UI layout, widget instantiation, and overall flow.
    *   Calls functions from `data_utils.py`, `calculations.py`, and `visualization.py`.
    *   Manages `st.session_state` for application-wide data.

-   **`data_utils.py`**:
    *   Contains functions for loading and preparing synthetic datasets and lookup tables.
    *   Example data structures will be defined here (e.g., dictionaries or Pandas DataFrames representing job roles, education multipliers, company types, and their associated risk factors).
    *   Provides helper functions to retrieve specific data points based on user selections.

-   **`calculations.py`**:
    *   Houses all the core mathematical functions corresponding to the formulas detailed in the "Core Concepts" section.
    *   Each formula (e.g., `calculate_fhc`, `calculate_idiosyncratic_risk`, `calculate_systematic_risk`, `calculate_premium`) will have its own dedicated function.
    *   Functions will take relevant input parameters and return the calculated result.

-   **`visualization.py`**:
    *   Contains functions responsible for generating the interactive charts using `plotly.express`.
    *   Functions will take processed data (e.g., risk scores over time for simulation) and return Plotly figure objects.
    *   Includes logic for annotations and tooltips on charts to provide detailed insights.

### Data Handling and Storage (Synthetic)

Given the `datasetType` is `Synthetic`, all data will be generated and stored within the application's code, likely as Python dictionaries and Pandas DataFrames.

-   **Lookup Tables:**
    *   `job_data`: A Pandas DataFrame mapping job titles to `f_role` multipliers and baseline $H_{base}$ scores.
    *   `education_data`: A dictionary or DataFrame for `f_level` and `f_field` multipliers based on education level and field of study.
    *   `school_tier_data`: A dictionary or DataFrame for `f_school` multipliers based on institution tier.
    *   `company_type_data`: A dictionary or DataFrame mapping company types (e.g., "Big firm", "Startup") to base $FCR$ values or their sub-components ($S_{senti}, S_{fin}, S_{growth}$).
-   **Default Parameters:** Constants for weights ($w_{CR}, w_{US}, w_{econ}, w_{inno}$), decay constants ($a$), actuarial base probabilities ($\beta_{systemic}, \beta_{individual}$), loading factor ($\lambda$), minimum premium ($P_{min}$), and TTV period.

### Calculation Flow

1.  **User Input Collection**: `app.py` collects user data via Streamlit widgets.
2.  **Factor Calculation**:
    *   `app.py` passes relevant user inputs to `calculations.py` functions to compute $FHC$, $FCR$, and $FUS$.
    *   Lookups for multipliers (e.g., $f_{role}, f_{level}$) are performed using data from `data_utils.py`.
3.  **Risk Score Calculation**:
    *   The computed factors are fed into `calculations.py` functions to determine $V_{raw}$ and then $V_i(t)$ (Idiosyncratic Risk).
    *   The base $H_{base}(t)$ for the current job is looked up. If a transition is simulated, `calculations.py` computes $H_{base}(k)$ over the TTV period.
    *   Environmental modifiers ($M_{econ}, IAI$) are either set by user inputs or default values, and then `calculations.py` computes $H_i$ (Systematic Risk).
4.  **Premium Calculation**:
    *   `calculations.py` computes $L_{payout}$ using user-defined actuarial parameters.
    *   $H_i$ and $V_i(t)$ are used by `calculations.py` to calculate $P_{systemic}$, $P_{individual|systemic}$, and finally $P_{claim}$.
    *   $E[Loss]$ is derived from $P_{claim}$ and $L_{payout}$.
    *   The final $P_{monthly}$ is calculated, incorporating the loading factor and minimum premium.
5.  **Output Display and Visualization**:
    *   `app.py` displays the calculated $V_i(t)$, $H_i$, and $P_{monthly}$ using `st.metric` and `st.write`.
    *   If a career transition simulation is active, `app.py` calls `visualization.py` to generate a Plotly line chart showing the change in $H_i$ over the TTV period, displayed with `st.plotly_chart`.
    *   Inline documentation (`st.markdown`, `st.expander`) is used to explain concepts and calculation steps alongside the results.

### State Management

`st.session_state` will be extensively used to store:
-   User-defined input parameters.
-   Intermediate calculation results (e.g., current $FHC$, $FCR$, $FUS$ values).
-   Simulation data (e.g., a list of $H_i$ values for each month during a career transition).
This ensures that the application's state persists across user interactions and re-runs.

## User Interface Components

The user interface will be intuitive and structured, guiding the user through the data exploration process with clear inputs and insightful outputs.

### Layout and Navigation

-   **Sidebar (`st.sidebar`)**: Will contain primary user inputs and navigation links.
    -   Sections for "Current Profile," "Upskilling Efforts," "Career Transition Simulation," and "Actuarial Parameters."
-   **Main Area**: Will display the calculated risk scores, insurance premium, and interactive visualizations.
    -   Organized into `st.tabs` (e.g., "Risk Profile," "Premium Details," "Transition Simulation") or `st.expander` sections for clarity.
    -   Detailed explanations and formula breakdowns (using `st.markdown` and `st.latex`) will accompany the results.

### Input Forms and Widgets

-   **Current Profile:**
    -   **Job Title**: `st.selectbox` or `st.text_input` (linked to `job_data` from `data_utils.py`).
    -   **Years of Experience**: `st.number_input` (for $Y_i$).
    -   **Education Level**: `st.selectbox` (e.g., "PhD", "Master's", "Bachelor's").
    -   **Education Field**: `st.selectbox` (e.g., "Tech/Engineering", "Liberal Arts").
    -   **Institution Tier**: `st.selectbox` (e.g., "Tier 1", "Tier 2", "Tier 3").
    -   **Company Type**: `st.selectbox` (e.g., "Big firm", "Mid-size firm", "Startup").

-   **Upskilling Efforts:**
    -   **General Skills Training Progress**: `st.slider(0, 100, 0, label="% General Skill Training Completed")` (for $P_{gen}(t)$).
    -   **Firm-Specific Skills Training Progress**: `st.slider(0, 100, 0, label="% Firm-Specific Skill Training Completed")` (for $P_{spec}(t)$).

-   **Career Transition Simulation:**
    -   **Simulate Transition**: `st.checkbox("Simulate Career Transition")`.
    -   **Target Career Path (Industry)**: `st.selectbox` (linked to industries from `job_data` for $H_{target}$).
    -   **Transition Time-to-Value (TTV)**: `st.number_input("Months for Transition (TTV)", value=12, min_value=1)`.
    -   **Months Elapsed Since Transition**: `st.slider("Months Since Transition Started", 0, TTV_value, 0)` (for $k$).

-   **Actuarial Parameters:**
    -   **Annual Salary**: `st.number_input("Annual Salary ($)", value=90000, min_value=0)`.
    -   **Coverage Percentage**: `st.slider("Coverage Percentage (%)", 0, 100, 25)`.
    -   **Coverage Duration (Months)**: `st.number_input("Coverage Duration (Months)", value=6, min_value=1)`.
    -   **Loading Factor ($\lambda$)**: `st.number_input("Loading Factor", value=1.5, min_value=0.0, step=0.1)`.
    -   **Minimum Premium ($P_{min}$)**: `st.number_input("Minimum Monthly Premium ($)", value=20.00, min_value=0.0)`.

-   **Environmental Modifiers (for $H_i$)**:
    -   **Economic Climate Modifier ($M_{econ}$)**: `st.slider("Economic Climate (0.8 = Recession, 1.2 = Boom)", 0.8, 1.2, 1.0, step=0.01)`.
    -   **AI Innovation Index ($IAI$)**: `st.slider("AI Innovation Index (0.8 = Slowdown, 1.2 = Rapid Breakthrough)", 0.8, 1.2, 1.0, step=0.01)`.

### Output Display and Visualizations

-   **Key Metrics Display**:
    -   `st.metric` cards to show the calculated `Idiosyncratic Risk ($V_i(t)$)`, `Systematic Risk ($H_i$)`, and `Monthly Premium ($P_{monthly}$)` prominently.
    -   Additional `st.write` or `st.info` blocks to show intermediate values like $FHC$, $FCR$, $FUS$, $P_{claim}$, $E[Loss]$.

-   **Interactive Charts (`st.plotly_chart`)**:
    -   **Risk Evolution During Transition**: A line chart showing the simulated $H_i$ value over the $TTV$ period as $k$ progresses, illustrating the effect of "Career Path Diversification".
        -   X-axis: Months Elapsed ($k$).
        -   Y-axis: Systematic Risk Score ($H_i$).
        -   Annotations and tooltips will show specific $H_i$ values at different months.
    -   **Factor Impact Bar Chart (Potential)**: A bar chart comparing the relative impact of $FHC$, $FCR$, and $FUS$ on $V_{raw}$, or the impact of $H_{base}$, $M_{econ}$, and $IAI$ on $H_i$.

-   **Explanatory Text and Inline Help**:
    -   `st.expander` sections will provide detailed explanations for each calculation step, including the LaTeX formula and description, enabling users to delve deeper into the model's mechanics.
    -   `st.markdown` will be used for overviews and concluding remarks, tying the application's functionality back to the core concept of "Systematic Risk Exposure Mitigation."
    -   Tooltips (via `help` parameter in widgets) will offer quick definitions for technical terms.

This structured approach ensures the application is robust, user-friendly, and effectively communicates the complex concepts of AI-driven job displacement risk and mitigation strategies.


### Appendix Code

```code
Vi(t) = f (FHC, FCR, FUS) (1)
Vraw = FHC (WCRFCR + WUS FUS)
FHC = frole flevel ffield fschool fexp (2)

FCR = W1 · Ssenti + W2. Sfin + W3. Sgrowth (3)
FUS = 1 - (γgen Pgen(t) + γspec Pspec(t)) (4)
Hi = Hbase (t) (Wecon Mecon + Winno. IAI) (5)
Hbase (k) = (1-k/TTV)·Hcurrent + (k/TTV)·Htarget (6)
Mecon = f(GDP Growth, Sector Employment, Interest Rates) (7)
IAI = f (VC Funding, R&D Spend, Public Salience) (8)

Pclaim Psystemic Pindividual|systemic (9)
Psystemic = (Hi/100) * Bsystemic (10)
Pindividual|systemic = (Vi(t)/100) * Bindividual (11)
Pmonthly = max(E[Loss] * λ / 12, Pmin) (12)

# Raw Score and Final Score Calculation
Raw Score: Vraw = FHC (WCRFCR+WUS. FUS)
Final Score: Vi(t) = min(100.0, max (5.0, Vraw - 50.0))
# Weights
WCR = 0.4
wus = 0.6
# Human Capital Factor Formula
FHC = frole · flevel · ffield · fschool · fexp

# Table 2: Human Capital Factor Calculation (Formulas/Lookups)
Role (frole): ROLE_MULTIPLIERS
Level (flevel): EDUCATION_LEVEL
Field (ffield): EDUCATION_FIELD
School (fschool): SCHOOL_TIER
Experience (fexp): 1-(0.015·min (Yrs, 20))
PRODUCT (FHC): (Multiply all above)

# Upskilling Factor Formula and Calculation
FUS = 1 - (0.7 Pidio (t))
Calculation (Both Personas): 1 - (0.7 * 0.0) = 1.0

# Persona A: Alex Chen (Paralegal) Idiosyncratic Risk Calculation
(1) Vraw = 1.262 * (0.4 * 0.95 + 0.6 * 1.0) = 1.237
(2) Vi(t) = min(100.0, max(5.0, 1.237 - 50.0)) = 61.85

# Persona B: Dr. Brenda Smith (Research Scientist) Idiosyncratic Risk Calculation
(1) Vraw = 0.192 * (0.4 * 1.00 + 0.6 * 1.0) = 0.192
(2) Vi(t) = min(100.0, max(5.0, 0.192 - 50.0)) = 9.6

# Illustrating the Impact of Upskilling (Alex completes training, Pidio = 0.5)
Alex's New FUS: 1 - (0.7 * 0.5) = 0.65
Alex's New Vraw: 1.262 * (0.4 * 0.95 + 0.6 * 0.65) = 0.972
Alex's New Final Score: min(100.0, max(5.0, 0.972-50.0)) = 48.6

# Systematic Risk Model Formula
Hi = Hbase(t)(Wecon Mecon+Winno IAI)
# Weights
Wecon = 0.5
winno = 0.5

# Initial Systematic Risk Calculation
Persona A: Alex Chen (Paralegal). H₁ = 65 * (0.5 * 1.0 + 0.5 * 1.0) = 65 * (1.0) = 65.0
Persona B: Dr. Brenda Smith (Research Scientist). H₁ = 30 * (0.5 * 1.0 + 0.5 * 1.0) = 30 * (1.0) = 30.0

# Illustrating the Impact of Career Path Diversification (Alex, k=6, Htarget=30)
Calculate Alex's new Hbase (t) to Healthcare:
Hbase (6) = (1-6/12)·65+(6/12)·30 = (0.5)·65+(0.5)·30 = 32.5+15 = 47.5
Calculate Alex's new Final Score (Hi):
H₁ = 47.5 * (1.0) = 47.5

# Alex's new Final Score (Hi) (k > 12)
H₁ = 30 * (1.0) = 30.0

# Policy and Actuarial Parameters (Assumed consistent parameters)
Annual Salary: $90,000
Coverage Percentage: 25%
Coverage Duration: 6 months
Systemic Event Base Probability (ẞsystemic): 0.10 (10%)
Individual Loss Base Probability (βindividual): 0.50 (50%)
Loading Factor (λ): 1.5
Minimum Premium (Pmin): $20.00

# Total Payout Amount (Lpayout) Formula and Calculation
Formula: Lpayout = ((Annual Salary / 12) * Coverage Duration * Coverage Percentage)
Calculation: ($90,000 / 12) * 6 * 0.25 = $7,500

# Annual Claim Probability (Pclaim) Formula and Calculation
Formula: pclaim = (Hi / 100 * Bsystemic) * (Vi / 100 * Bindividual)
Persona A: Alex Chen. Pclaim = (65.0 / 100 * 0.10) * (61.85 / 100 * 0.50) = (0.065) * (0.30925) = 0.0201 (or 2.01%)
Persona B: Dr. Brenda Smith. Pclaim = (30.0 / 100 * 0.10) * (9.6 / 100 * 0.50) = (0.03) * (0.048) = 0.00144 (or 0.144%)

# Annual Expected Loss (E[Loss]) Formula and Calculation
Formula: E[Loss] = Pclaim * Lpayout
Persona A: Alex Chen. E[Loss] = 0.0201 * $11, 250 = $226.13
Persona B: Dr. Brenda Smith. E[Loss] = 0.00144 * $11, 250 = $16.20

# Final Monthly Premium (Pmonthly) Formula and Calculation
Formula: Pmonthly = max((E[Loss] * λ / 12), Pmin)
Persona A: Alex Chen. Pmonthly = max($226.13 * 1.5 / 12, $20.00) = max($28.27, $20.00) = $28.27
Persona B: Dr. Brenda Smith. Pmonthly = max($16.20 * 1.5 / 12, $20.00) = max($2.03, $20.00) = $20.00
```