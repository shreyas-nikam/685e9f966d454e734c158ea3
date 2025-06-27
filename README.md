
# AI Risk Score - V4-2: Career Path Diversification Tool

This Streamlit application helps users understand and mitigate their exposure to systematic AI risk in their careers. Inspired by the concept of "Systematic Risk Exposure Mitigation" or "Career Path Diversification," it simulates how different career choices and personal development efforts influence an individual's AI displacement risk profile and potential insurance premiums.

## Overview

The tool transforms raw synthetic data into interactive visualizations, providing detailed insights and explanations directly on the charts. Users can interact with input forms and widgets to experiment with various parameters and observe real-time updates, thereby gaining a clear understanding of key concepts such as Idiosyncratic Risk, Systematic Risk, and their implications for career resilience.

## Features

*   **Interactive Input Forms**: Adjust career details, upskilling progress, and actuarial parameters.
*   **Real-time Risk Assessment**: Instantly view calculated Idiosyncratic Risk, Systematic Risk, and Monthly Insurance Premiums.
*   **Career Transition Simulation**: Model the impact of transitioning to a new career path on your Systematic Risk over time.
*   **Detailed Explanations**: Understand the underlying mathematical formulas and core concepts through inline documentation.
*   **Interactive Visualizations**: Plotly charts illustrate trends and relationships between inputs and risk outputs.

## Setup and Run

To set up and run the application locally, follow these steps:

1.  **Clone the Repository**:
    ```bash
    git clone <repository-url>
    cd ai-risk-score-v4-2
    ```

2.  **Create a Virtual Environment (Recommended)**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: `venv\Scripts\activate`
    ```

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Streamlit Application**:
    ```bash
    streamlit run app.py
    ```

    The application will open in your default web browser (usually at `http://localhost:8501`).

## Docker Deployment

You can also run this application using Docker:

1.  **Build the Docker Image**:
    ```bash
    docker build -t ai-risk-app .
    ```

2.  **Run the Docker Container**:
    ```bash
    docker run -p 8501:8501 ai-risk-app
    ```

    Access the application in your browser at `http://localhost:8501`.

## Project Structure

*   `app.py`: Main Streamlit application entry point.
*   `requirements.txt`: Python dependencies.
*   `Dockerfile`: Docker configuration for deployment.
*   `README.md`: Project description and setup instructions.
*   `application_pages/`: Directory containing individual Streamlit page modules.
    *   `data_utils.py`: Functions for generating and loading synthetic data.
    *   `calculations.py`: Core mathematical functions for risk and premium calculations.
    *   `visualization.py`: Functions for generating Plotly charts.
    *   `home_page.py`: Contains the home page content and introduction.
    *   `risk_premium_calculator.py`: Contains the main calculator logic.
    *   `transition_simulator.py`: Contains the career transition simulation logic.

## License

© 2025 QuantUniversity. All Rights Reserved.

The purpose of this demonstration is solely for educational use and illustration. Any reproduction of this demonstration requires prior written consent from QuantUniversity. This lab was generated using the QuCreate platform. QuCreate relies on AI models for generating code, which may contain inaccuracies or errors.
