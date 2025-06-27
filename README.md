
# AI Risk Score - V4-2: Career Path Diversification Tool

## Overview

The "Career Path Diversification Tool" is a Streamlit application designed to help users understand and mitigate their exposure to systematic AI risk in their careers. Inspired by concepts from a detailed document, the application allows users to explore how different career choices and personal development efforts influence their AI displacement risk profile and potential insurance premiums. It focuses on illustrating "Systematic Risk Exposure Mitigation" or "Career Path Diversification" by simulating the impact of career transitions and skill acquisition on an individual's overall risk score.

This tool transforms raw synthetic data into interactive visualizations, providing detailed insights and explanations directly on the charts. Users can interact with input forms and widgets to experiment with various parameters and observe real-time updates, thereby gaining a clear understanding of key concepts such as Idiosyncratic Risk, Systematic Risk, and their implications for career resilience.

## Features

*   **Interactive Input Forms**: Adjust various parameters like job title, experience, education, upskilling progress, and actuarial parameters to see their real-time impact.
*   **Dynamic Risk Score Calculation**: Instantly view your Idiosyncratic Risk ($V_i(t)$) and Systematic Risk ($H_i$) scores based on your inputs.
*   **Insurance Premium Estimation**: Get an estimated monthly insurance premium ($P_{monthly}$) based on your risk profile.
*   **Career Transition Simulation**: Simulate the reduction in Systematic Risk over time as you transition to a new career path, visualizing the "Time-to-Value (TTV)" concept with interactive charts.
*   **Detailed Explanations**: Understand the underlying mathematical models and concepts with inline explanations and LaTeX formulas for each calculation.
*   **Plotly Visualizations**: Engage with interactive charts that show trends and correlations in risk scores.

## Mathematical Concepts Explained

The application is built upon several core mathematical models, including:

*   **Idiosyncratic Risk ($V_i(t)$)**: Quantifies an individual's specific vulnerability to job displacement.
*   **Raw Idiosyncratic Risk ($V_{raw}$)**: Combines Human Capital, Company Risk, and Upskilling factors.
*   **Human Capital Factor ($FHC$)**: Assesses foundational resilience based on educational and professional background.
*   **Experience Factor ($f_{exp}$)**: Models how years of experience influence vulnerability with diminishing returns.
*   **Company Risk Factor ($FCR$)**: Quantifies employer stability and growth prospects.
*   **Upskilling Factor ($FUS$)**: Rewards proactive training efforts, especially portable skills.
*   **Systematic Risk ($H_i$)**: Reflects macro-level automation hazard adjusted by environmental conditions.
*   **Time-to-Value (TTV) Modified Base Occupational Hazard ($H_{base}(k)$)**: Models gradual reduction in systematic risk during career transition.
*   **Annual Claim Probability ($P_{claim}$)**: Joint probability of a systemic event and individual loss.
*   **Systemic Event Base Probability ($P_{systemic}$)**: Converts Systematic Risk into a probability of a systemic event.
*   **Individual Loss Base Probability ($P_{individual|systemic}$)**: Quantifies conditional likelihood of job loss given a systemic event.
*   **Annual Expected Loss ($E[Loss]$)**: Financial quantification of risk.
*   **Total Payout Amount ($L_{payout}$)**: Financial benefit defined by policy terms.
*   **Monthly Insurance Premium ($P_{monthly}$)**: Final financial output, translating expected loss into a periodic payment.

Each concept is explained within the application, often accompanied by its mathematical formula for complete transparency.

## How to Run the Application

### Prerequisites

*   Python 3.9+
*   Docker (optional, for containerized deployment)

### Local Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd ai-risk-score-v4-2
    ```
2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: `venv\Scripts\activate`
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run the Streamlit application:**
    ```bash
    streamlit run app.py
    ```
    The application will open in your default web browser (usually at `http://localhost:8501`).

### Docker Deployment

1.  **Build the Docker image:**
    ```bash
    docker build -t ai-risk-score-v4-2 .
    ```
2.  **Run the Docker container:**
    ```bash
    docker run -p 8501:8501 ai-risk-score-v4-2
    ```
    The application will be accessible at `http://localhost:8501`.

## Project Structure

```
.
├── app.py                      # Main Streamlit application entry point
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker build instructions
├── README.md                   # Project overview and instructions
└── application_pages/
    ├── __init__.py
    ├── calculations.py         # Core mathematical functions for risk and premium calculation
    ├── data_utils.py           # Functions for synthetic data generation and lookup
    └── visualization.py        # Functions for generating Plotly charts
```

## Disclaimer

The purpose of this demonstration is solely for educational use and illustration. Any reproduction of this demonstration requires prior written consent from QuantUniversity. This lab was generated using the QuCreate platform. QuCreate relies on AI models for generating code, which may contain inaccuracies or errors.
