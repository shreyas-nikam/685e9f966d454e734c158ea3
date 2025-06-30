
# AI Risk Score - V4-2: Career Path Diversification Tool

## Overview

The "Career Path Diversification Tool" is a Streamlit application designed to help users understand and mitigate their exposure to systematic AI risk in their careers. Inspired by concepts from academic research on AI displacement risk, this tool allows users to explore how different career choices and personal development efforts influence their AI displacement risk profile and potential insurance premiums. It focuses on illustrating "Systematic Risk Exposure Mitigation" or "Career Path Diversification" by simulating the impact of career transitions and skill acquisition on an individual's overall risk score.

The application transforms raw synthetic data into interactive visualizations, providing detailed insights and explanations directly on the charts. Users can interact with input forms and widgets to experiment with various parameters and observe real-time updates, thereby gaining a clear understanding of key concepts such as Idiosyncratic Risk, Systematic Risk, and their implications for career resilience.

## Features

-   **Interactive Risk Assessment**: Input your current career details (job title, experience, education, company type) to get a real-time AI risk score.
-   **Upskilling Impact Simulation**: Adjust your general and firm-specific skill training progress to see how it affects your idiosyncratic risk.
-   **Career Transition Modeling**: Simulate a career change to a new industry and observe the projected reduction in systematic risk over time.
-   **Insurance Premium Calculation**: Understand how your risk profile translates into an estimated monthly insurance premium, based on user-defined actuarial parameters.
-   **Detailed Explanations**: Comprehensive inline explanations for all mathematical formulas and core concepts, helping users grasp the underlying logic.
-   **Interactive Visualizations**: Plotly charts illustrate risk evolution during career transitions and the impact of various factors.

## How to Run Locally

To run this Streamlit application on your local machine, follow these steps:

### Prerequisites

-   Python 3.9+
-   `pip` (Python package installer)
-   `git` (for cloning the repository)

### Steps

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/your-username/ai-risk-score-v4-2.git
    cd ai-risk-score-v4-2
    ```
    (Note: Replace `your-username/ai-risk-score-v4-2` with the actual repository path if different.)

2.  **Create a Virtual Environment (Recommended)**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Streamlit Application**:
    ```bash
    streamlit run app.py
    ```

    Your web browser should automatically open a new tab with the Streamlit application. If not, open your browser and navigate to `http://localhost:8501`.

## Project Structure

-   `app.py`: The main Streamlit application file, handles UI layout and overall application flow.
-   `application_pages/`: Directory containing individual page modules for the Streamlit app.
    -   `risk_profile_page.py`: Handles the display and calculations related to Idiosyncratic and Systematic Risk.
    -   `premium_calculator_page.py`: Manages the insurance premium calculations and display.
    -   `transition_simulation_page.py`: Implements the career transition simulation and visualization.
-   `calculations.py`: Contains all the core mathematical functions for risk and premium calculations.
-   `data_utils.py`: Functions for generating and loading synthetic datasets and lookup tables.
-   `visualization.py`: Functions for generating interactive Plotly charts.
-   `requirements.txt`: Lists all Python dependencies.
-   `Dockerfile`: For containerizing the application using Docker.

## Core Concepts Explained

The application is built upon several core mathematical models:

-   **Idiosyncratic Risk ($V_i(t)$)**: Individual-specific vulnerability.
    $$V_i(t) = \min(100.0, \max(5.0, V_{raw} - 50.0))$$
-   **Raw Idiosyncratic Risk ($V_{raw}$)**: Combines human capital, company, and upskilling factors.
    $$V_{raw} = FHC \cdot (w_{CR} FCR + w_{US} FUS)$$
-   **Human Capital Factor ($FHC$)**: Assesses foundational resilience.
    $$FHC = f_{role} \cdot f_{level} \cdot f_{field} \cdot f_{school} \cdot f_{exp}$$
-   **Experience Factor ($f_{exp}$)**: Models experience impact with diminishing returns.
    $$f_{exp} = 1 - (a \cdot \min(Y_i, Y_{cap}))$$
-   **Company Risk Factor ($FCR$)**: Quantifies employer stability.
    $$FCR = w_1 \cdot S_{senti} + w_2 \cdot S_{fin} + w_3 \cdot S_{growth}$$
-   **Upskilling Factor ($FUS$)**: Rewards proactive training.
    $$FUS = 1 - (\gamma_{gen} P_{gen}(t) + \gamma_{spec} P_{spec}(t))$$
-   **Systematic Risk ($H_i$)**: Macro-level automation hazard.
    $$H_i = H_{base}(t) \cdot (w_{econ} M_{econ} + w_{inno} IAI)$$
-   **Time-to-Value (TTV) Modified Base Occupational Hazard ($H_{base}(k)$)**: Models risk reduction during transition.
    $$H_{base}(k) = \left(1 - \frac{k}{TTV}\right) H_{current} + \left(\frac{k}{TTV}\right) H_{target}$$
-   **Annual Claim Probability ($P_{claim}$)**: Joint probability of systemic event and individual loss.
    $$P_{claim} = P_{systemic} \cdot P_{individual|systemic}$$
-   **Systemic Event Base Probability ($P_{systemic}$)**: Converts systematic risk to event probability.
    $$P_{systemic} = \frac{H_i}{100} \cdot \beta_{systemic}$$
-   **Individual Loss Base Probability ($P_{individual|systemic}$)**: Conditional likelihood of job loss given a systemic event.
    $$P_{individual|systemic} = \frac{V_i(t)}{100} \cdot \beta_{individual}$$
-   **Annual Expected Loss ($E[Loss]$)**: Financial quantification of risk.
    $$E[Loss] = P_{claim} \cdot L_{payout}$$
-   **Total Payout Amount ($L_{payout}$)**: Financial benefit from policy.
    $$L_{payout} = \left( \frac{\text{Annual Salary}}{12} \right) \cdot \text{Coverage Duration} \cdot \text{Coverage Percentage}$$
-   **Monthly Insurance Premium ($P_{monthly}$)**: Final periodic payment.
    $$P_{monthly} = \max \left( \frac{E[Loss] \cdot \lambda}{12}, P_{min} \right)$$

For detailed explanations of these formulas and their parameters, please refer to the application's inline documentation.

---

© 2025 QuantUniversity. All Rights Reserved.
