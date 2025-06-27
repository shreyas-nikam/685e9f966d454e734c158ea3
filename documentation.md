id: 685e9f966d454e734c158ea3_documentation
summary: AI Risk Score - V4-2 Documentation
feedback link: https://docs.google.com/forms/d/e/1FAIpQLSfWkOK-in_bMMoHSZfcIvAeO58PAH9wrDqcxnJABHaxiDqhSA/viewform?usp=sf_link
environments: Web
status: Published
# AI Displacement Risk Assessment and Career Path Diversification Tool Codelab

This codelab provides a comprehensive guide to understanding and using the AI Displacement Risk Assessment and Career Path Diversification Tool. This tool, built using Streamlit, is designed to help individuals assess their career's vulnerability to AI-driven job displacement and explore strategies to mitigate these risks through upskilling and career transitions.

## Introduction
Duration: 00:05

This application simulates the risk associated with AI-driven job displacement. It considers both individual factors (Idiosyncratic Risk) and broader economic/technological trends (Systematic Risk) to estimate an individual's vulnerability.  The application provides insights into how personal attributes, employer stability, and external economic forces affect career risk, as well as the financial implications of that risk. You'll also learn how strategic upskilling and career transitions can proactively reduce exposure to AI-driven systematic risk.

The core concepts explored include:

*   **Idiosyncratic Risk ($V_i(t)$):** Risk specific to the individual, influenced by human capital, company risk, and upskilling efforts.
*   **Systematic Risk ($H_i$):**  Risk related to the overall automation hazard of an occupation, influenced by economic climate and AI innovation.
*   **Time-to-Value (TTV):** The period required for a career transition to realize its full risk mitigation benefits.
*   **Insurance Premium Calculation:** Translating risk scores into a tangible financial representation, demonstrating the "insurance" benefit of career resilience.

This codelab will walk you through the application's functionalities, underlying calculations, and visualization components.

## Setting Up the Environment
Duration: 00:03

Before diving into the application's features, ensure you have the following prerequisites:

*   Python 3.7 or higher
*   Streamlit
*   Pandas
*   NumPy
*   Plotly

You can install the necessary packages using pip:

```bash
pip install streamlit pandas numpy plotly
```

Download all the python files, `data_utils.py`, `calculations.py`, `visualization.py`, `application_pages/home_page.py`, `application_pages/simulation_page.py`, and `app.py`. Make sure to create an `application_pages` folder and place the `home_page.py` and `simulation_page.py` files inside it. You also need to create a blank `__init__.py` file inside the `application_pages` folder for the application to function properly.

Once all the files are downloaded and the environment is set up, navigate to the directory containing `app.py` and run the application using the following command:

```bash
streamlit run app.py
```

This command will launch the Streamlit application in your web browser.

## Understanding the Application Architecture
Duration: 00:07

The application's architecture is designed for modularity and maintainability. Here's a breakdown of the key components:

*   **`app.py` (Main Application):**
    *   Serves as the entry point for the Streamlit application.
    *   Sets up the basic page configuration (title, layout).
    *   Includes a navigation sidebar to switch between different application pages.
    *   Hosts introductory information and business logic explanations.
    *   Handles page routing based on user selection.

*   **`application_pages/home_page.py` (Risk Profile Page):**
    *   Contains the UI and logic for the "Your Risk Profile" page.
    *   Collects user inputs for professional profile, upskilling efforts, and environmental modifiers.
    *   Performs calculations to determine idiosyncratic and systematic risk.
    *   Displays the AI risk assessment summary, including risk scores and estimated monthly premium.

*   **`application_pages/simulation_page.py` (Career Transition Simulation Page):**
    *   Implements the "Career Transition Simulation" page.
    *   Allows users to define a target career path and simulate the impact of transitioning on their systematic risk over time.
    *   Uses the Time-to-Value (TTV) concept to model the gradual reduction in risk.
    *   Visualizes the simulated systematic risk evolution using a Plotly chart.

*   **`data_utils.py`:**
    *   Loads and provides access to static data, such as job role information, education level details, and company type attributes.
    *   Includes functions to load job data, education data, school tier data, and company type data.
    *   Also contains default parameter settings used in various calculations.

*   **`calculations.py`:**
    *   Encapsulates all the calculation logic for determining risk scores and insurance premiums.
    *   Includes functions to calculate human capital factor, company risk factor, upskilling factor, idiosyncratic risk, systematic risk, and monthly premium.

*   **`visualization.py`:**
    *   Provides functions for creating visualizations, such as the risk evolution plot and factor impact plot.
    *   Uses Plotly to generate interactive charts.

<aside class="positive">
Good design!  Separating the UI, calculations, data loading, and visualizations makes the application easier to understand, modify, and test.
</aside>

## Exploring the Risk Profile Page
Duration: 00:15

The "Your Risk Profile" page allows users to input their professional details and environmental factors to calculate their current AI displacement risk.

1.  **Professional Profile:**

    *   **Job Title:** Select your current job title from a predefined list. This determines the base occupational hazard score ($H_{base}$).
    *   **Years of Experience:** Enter your years of professional experience. More experience can reduce your idiosyncratic risk.
    *   **Education Level & Field:** Choose your highest education level and field of study.  These factors influence your human capital factor ($FHC$).
    *   **Institution Tier:** Select the tier of your educational institution, which serves as a proxy for the quality of training.
    *   **Company Type:** Choose the type of company you work for. This affects the company risk factor ($FCR$).

2.  **Upskilling Efforts:**

    *   **General Skills Training Progress:** Indicate the percentage of progress in acquiring general, portable skills like coding or data analysis.  This contributes to the upskilling factor ($FUS$).
    *   **Firm-Specific Skills Training Progress:** Indicate the percentage of progress in acquiring skills specific to your current firm or industry.

3.  **Environmental Modifiers:**

    *   **Economic Climate Modifier ($M_{econ}$):**  Adjust this slider to reflect the overall economic environment. Values less than 1.0 indicate a recession, while values greater than 1.0 indicate a boom. This affects systematic risk.
    *   **AI Innovation Index ($IAI$):**  Adjust this slider to reflect the pace of AI technological change. Values less than 1.0 indicate a slowdown, while values greater than 1.0 indicate rapid breakthrough. This also affects systematic risk.

4.  **Actuarial Parameters:**

    *   **Annual Salary:**  Enter your annual salary. This is used to calculate the potential payout in case of job displacement.
    *   **Coverage Percentage:** Specify the percentage of your monthly salary that would be covered by the insurance policy.
    *   **Coverage Duration:**  Specify the duration (in months) for which the salary will be paid out if a claim is triggered.
    *   **Loading Factor ($\lambda$):**  An insurance multiplier to cover administrative costs and profit margin.
    *   **Minimum Monthly Premium ($P_{min}$):** The minimum monthly premium to ensure policy viability.

5.  **Risk Assessment Summary:**

    *   Displays the calculated **Idiosyncratic Risk ($V_i(t)$)**, **Systematic Risk ($H_i$)**, and **Estimated Monthly Premium ($P_{monthly}$)** based on your inputs.

    *   An information box provides context about the risk scores.

    *   An expander section provides a detailed breakdown of the calculations.

6.  **Factor Impact Visualization:**

    *   A bar chart visualizes the impact of the Human Capital Factor (FHC), Company Risk Factor (FCR), and Upskilling Factor (FUS) on the overall idiosyncratic risk.

## Diving into the Calculations
Duration: 00:20

The application uses several formulas to calculate the risk scores and insurance premium. Here's a breakdown of the key calculations (found in `calculations.py`):

1.  **Human Capital Factor (FHC):**

    ```python
    def calculate_fhc(job_title, education_level, education_field, school_tier, years_experience):
        f_role = JOB_DATA[JOB_DATA['Job Title'] == job_title]['f_role'].iloc[0]
        f_level = EDU_DATA[education_level]['f_level']
        f_field = EDU_DATA[education_field]['f_field']
        f_school = SCHOOL_DATA[school_tier]['f_school']
        f_exp = calculate_f_exp(years_experience)
        return f_role * f_level * f_field * f_school * f_exp
    ```

    *   Combines factors related to the individual's skills, education, and experience.
    *   `f_role`:  Base vulnerability score derived from the job title.
    *   `f_level`, `f_field`, `f_school`:  Factors based on education level, field, and school tier, respectively.
    *   `f_exp`:  Experience factor, calculated using an exponential decay function.

2.  **Company Risk Factor (FCR):**

    ```python
    def calculate_fcr(company_type):
        company_info = COMPANY_DATA[company_type]
        S_senti = company_info['S_senti']
        S_fin = company_info['S_fin']
        S_growth = company_info['S_growth']

        w1, w2, w3 = 1/3, 1/3, 1/3
        return (w1 * S_senti) + (w2 * S_fin) + (w3 * S_growth)
    ```

    *   Assesses the risk associated with the individual's employer.
    *   `S_senti`, `S_fin`, `S_growth`:  Scores representing the company's sentiment, financial stability, and growth potential, respectively.
    *   Calculated as a weighted average of these scores.

3.  **Upskilling Factor (FUS):**

    ```python
    def calculate_fus(p_gen, p_spec):
        gamma_gen = PARAMS['gamma_gen']
        gamma_spec = PARAMS['gamma_spec']
        return 1 - (gamma_gen * p_gen + gamma_spec * p_spec)
    ```

    *   Rewards continuous learning and skill development.
    *   `p_gen`:  Progress in general skills training (e.g., coding, data analysis).
    *   `p_spec`:  Progress in firm-specific skills training.
    *   `gamma_gen`, `gamma_spec`:  Weights reflecting the relative importance of general and specific skills.

4.  **Raw Idiosyncratic Risk (V_raw):**

    ```python
    def calculate_v_raw(fhc, fcr, fus):
        w_CR = PARAMS['w_CR']
        w_US = PARAMS['w_US']
        return fhc * (w_CR * fcr + w_US * fus)
    ```

    *   Combines the human capital, company risk, and upskilling factors.
    *   `w_CR`, `w_US`: Weights representing the relative importance of company risk and upskilling.

5.  **Idiosyncratic Risk ($V_i(t)$):**

    ```python
    def calculate_idiosyncratic_risk(v_raw):
        return min(100.0, max(5.0, v_raw - 50.0))
    ```

    *   Scales the raw idiosyncratic risk to a range between 5 and 100.

6.  **Systematic Risk ($H_i$):**

    ```python
    def calculate_systematic_risk(h_base_t, m_econ, iai):
        w_econ = PARAMS['w_econ']
        w_inno = PARAMS['w_inno']
        return h_base_t * (w_econ * m_econ + w_inno * iai)
    ```

    *   Calculates the overall automation hazard based on the job's base hazard and environmental conditions.
    *   `h_base_t`: Base occupational hazard score (derived from the job title).
    *   `m_econ`: Economic climate modifier.
    *   `iai`: AI innovation index.
    *   `w_econ`, `w_inno`: Weights representing the relative importance of economic climate and AI innovation.

7.  **Monthly Insurance Premium ($P_{monthly}$):**

    ```python
    def calculate_p_monthly(e_loss):
        loading_factor = PARAMS['loading_factor']
        min_premium = PARAMS['min_premium']
        return max((e_loss * loading_factor) / 12, min_premium)
    ```

    *   Calculated from the expected loss, loading factor, and minimum premium.

<aside class="negative">
It's important to note that the specific formulas and weights used in this application are simplified representations for illustrative purposes. Real-world risk assessment models would likely be more complex and data-driven.
</aside>

## Simulating Career Transitions
Duration: 00:15

The "Career Transition Simulation" page allows users to explore how transitioning to a different career path can mitigate their exposure to systematic AI risk over time.

1.  **Current Career Context:**

    *   Displays your current job title and base occupational hazard score ($H_{current}$) based on the information entered on the "Your Risk Profile" page. If no information is available, it displays a default job title and prompts the user to set up their current career details.

2.  **Define Your Target Career Path:**

    *   **Target Career Path (Job Title):**  Select a new job title that you are considering transitioning into. Choose one with a lower $H_{base}$ to see the diversification effect.
    *   Displays the target job title and its base occupational hazard score ($H_{target}$).

3.  **Simulation Parameters:**

    *   **Time-to-Value (TTV) Period (Months):** Enter the total number of months required for the full benefit of the career transition to be realized.
    *   **Months Elapsed Since Transition Started ($k$):** Slide this to see the progressive reduction in systematic risk over the transition period.
    *   **Economic Climate Modifier ($M_{econ}$):** Adjust the economic climate during the simulation.
    *   **AI Innovation Index ($IAI$):** Adjust the AI innovation pace during the simulation.

4.  **Simulated Systematic Risk Over Time:**

    *   Displays the simulated systematic risk ($H_i$) at the current month ($k$).
    *   A line chart visualizes the evolution of systematic risk over the entire TTV period.

The key calculation in this simulation is the Time-to-Value (TTV) Modified Base Occupational Hazard ($H_{base}(k)$), which is calculated as a linear interpolation between your current and target job's base hazards:

```
H_{base}(k) = (1 - k/TTV) * H_{current} + (k/TTV) * H_{target}
```

Where:

*   $H_{current}$: Your original job's base hazard.
*   $H_{target}$: Your target job's base hazard.
*   $TTV$: Total transition period in months.
*   $k$: Months elapsed since transition started.

This formula shows how your base hazard shifts from $H_{current}$ to $H_{target}$ as $k$ approaches $TTV$, reflecting a successful career path diversification.

## Customizing the Application
Duration: 00:10

The modular design of the application makes it relatively easy to customize and extend. Here are a few potential modifications:

*   **Adding New Job Roles:** Modify the `load_job_data` function in `data_utils.py` to include additional job titles and their corresponding `f_role` and `H_base` values.
*   **Incorporating More Granular Economic Data:** Replace the simple `m_econ` slider with a more sophisticated data source that provides real-time economic indicators.
*   **Implementing a Machine Learning Model:** Train a machine learning model to predict company risk scores (`S_senti`, `S_fin`, `S_growth`) based on various company attributes.
*   **Adding New Visualizations:** Create additional charts and graphs in `visualization.py` to provide more insights into the risk factors and their impact.
*   **Refining Actuarial Calculations:** Enhance the premium calculation logic with more sophisticated actuarial models.

## Conclusion
Duration: 00:05

This codelab has provided a comprehensive overview of the AI Displacement Risk Assessment and Career Path Diversification Tool. By understanding the application's architecture, calculations, and functionalities, you can effectively use it to assess your career's vulnerability to AI-driven job displacement and explore strategies to mitigate these risks.  Remember that this application is a simplified model for educational purposes, and real-world risk assessment may require more complex models and data sources.
