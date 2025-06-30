# AI Risk Score - V4-2: Career Path Diversification Tool

This Streamlit application, "Career Path Diversification Tool," helps users understand and mitigate their exposure to systematic AI risk in their careers. It's inspired by concepts from advanced risk modeling and allows users to explore how different career choices and personal development efforts influence their AI displacement risk profile and potential insurance premiums.

The tool focuses on illustrating "Systematic Risk Exposure Mitigation" or "Career Path Diversification" by simulating the impact of career transitions and skill acquisition on an individual's overall AI risk score. It transforms raw synthetic data into interactive visualizations, providing detailed insights and explanations directly on the charts.

## Features:
- **Interactive Input Forms**: Adjust career details, upskilling progress, and actuarial parameters.
- **Real-time Risk Calculation**: See immediate updates to Idiosyncratic Risk ($V_i(t)$), Systematic Risk ($H_i$), and Monthly Insurance Premium ($P_{monthly}$).
- **Career Transition Simulation**: Visualize the projected reduction in Systematic Risk when transitioning to a new career path over a defined Time-to-Value (TTV) period.
- **Detailed Explanations**: Understand the underlying mathematical models and core concepts through inline explanations and formulae.

## Core Concepts Explained:
- **Idiosyncratic Risk ($V_i(t)$)**: Individual-specific vulnerability factors.
- **Systematic Risk ($H_i$)**: Macro-level automation hazard of an occupation, adjusted by environmental conditions.
- **Human Capital Factor ($FHC$)**: Resilience based on education and professional background.
- **Company Risk Factor ($FCR$)**: Stability and growth prospects of the employer.
- **Upskilling Factor ($FUS$)**: Impact of proactive training efforts, distinguishing between general and firm-specific skills.
- **Time-to-Value (TTV)**: Modeling the gradual reduction in systematic risk during career transitions.
- **Actuarial Premium Calculation**: How risk scores translate into an annual claim probability and a monthly insurance premium.

## How to Run Locally:

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd <repository_name>
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv
    # On Windows
    .\venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Streamlit application:**
    ```bash
    streamlit run app.py
    ```

The application will open in your web browser, typically at `http://localhost:8501`.