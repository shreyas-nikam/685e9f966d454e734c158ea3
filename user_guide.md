id: 685e9f966d454e734c158ea3_user_guide
summary: AI Risk Score - V4-2 User Guide
feedback link: https://docs.google.com/forms/d/e/1FAIpQLSfWkOK-in_bMMoHSZfcIvAeO58PAH9wrDqcxnJABHaxiDqhSA/viewform?usp=sf_link
environments: Web
status: Published
# Understanding Your AI Job Displacement Risk

This codelab guides you through a Streamlit application designed to help you understand and manage your career's exposure to AI-driven job displacement risk. You'll learn how various factors influence your risk profile and how strategic career decisions, like upskilling and career transitions, can mitigate these risks. The application calculates an AI risk score, and translates it into an estimated monthly insurance premium, providing a tangible financial representation of your overall risk.

## Exploring Your Risk Profile

Duration: 00:10

This step will guide you through the "Your Risk Profile" page, where you can input your professional details and see an immediate assessment of your AI displacement risk.

1.  **Navigate to the "Your Risk Profile" page:** Use the navigation sidebar on the left to select "Your Risk Profile".
2.  **Professional Profile:** In the "Your Professional Profile" section, fill in the following details:
    *   **Job Title:** Select your current job title from the dropdown menu. This determines your base role vulnerability.
    *   **Years of Experience:** Enter your total years of professional experience. More experience can potentially reduce your risk score.
    *   **Highest Education Level:** Choose your highest academic qualification.
    *   **Education Field:** Select your primary field of study. Certain fields offer more transferable skills, which can lower your risk.
    *   **Institution Tier:** Choose the tier that best represents your educational institution. This acts as a proxy for the quality of training you received.
    *   **Company Type:** Select the type of company you currently work for. This influences company risk factors.
3.  **Upskilling Efforts:** In the "Your Upskilling Efforts" section:
    *   **General Skills Training Progress (%):** Use the slider to indicate your progress in acquiring general or portable skills, such as coding, data analysis, or project management.
    *   **Firm-Specific Skills Training Progress (%):** Use the slider to indicate your progress in acquiring skills specific to your current company or industry.
4.  **Environmental Modifiers:**  Adjust the sliders in the "Environmental Modifiers" section:
    *   **Economic Climate Modifier:** Reflects the overall economic environment. Values less than 1.0 indicate a recession, while values greater than 1.0 indicate a boom.
    *   **AI Innovation Index:**  Indicates the momentum of AI technological change. Values less than 1.0 indicate a slowdown, while values greater than 1.0 indicate rapid breakthroughs.
5.  **Actuarial Parameters:**  Adjust the values in the "Actuarial Parameters" section:
    *   **Annual Salary ($):** Your current annual salary. Used to calculate potential payout.
    *   **Coverage Percentage (%):** Percentage of your monthly salary covered by the policy.
    *   **Coverage Duration (Months):** Duration in months for which the salary will be paid out if a claim is triggered.
    *   **Loading Factor:** An insurance multiplier to cover administrative costs and profit margin.
    *   **Minimum Monthly Premium ($):** The minimum monthly premium to ensure policy viability.
6.  **Review Your AI Risk Assessment Summary:** After entering your information, the application will display your AI Risk Assessment Summary, including:
    *   **Idiosyncratic Risk:** A measure of your personal vulnerability to AI displacement.
    *   **Systematic Risk:** A measure of the macro-level automation hazard of your occupation.
    *   **Estimated Monthly Premium:** The estimated cost of insurance against job displacement.
7.  **Detailed Calculation Breakdown:** Expand the "Detailed Calculation Breakdown" section to see a more in-depth explanation of how each risk factor is calculated.
8.  **Factor Impact Visualization:**  Observe the bar chart visualizing the impact of Human Capital (FHC), Company Risk (FCR), and Upskilling (FUS) on your idiosyncratic risk.

<aside class="positive">
Experiment with different values to see how your risk profile changes. For example, increasing your "General Skills Training Progress" should decrease your Idiosyncratic Risk.
</aside>

## Simulating Career Transition

Duration: 00:15

This step walks you through the "Career Transition Simulation" page, where you can explore how transitioning to a different career path can mitigate your exposure to Systematic AI Risk over time.

1.  **Navigate to the "Career Transition Simulation" page:** Use the navigation sidebar to select "Career Transition Simulation".
2.  **Current Career Context:**  If you completed the "Your Risk Profile" page, the application will display your current job title and base occupational hazard. If not, you will see a default job title.
3.  **Target Career Path:** Select your target career path (the job you are considering transitioning to) from the "Target Career Path (Job Title)" dropdown menu.  Choose a job with a lower base occupational hazard to see the diversification effect.
4.  **Simulation Parameters:** Adjust the following simulation parameters:
    *   **Time-to-Value (TTV) Period (Months):**  Enter the number of months required for the full benefit of the career transition to be realized.
    *   **Months Elapsed Since Transition Started:** Use the slider to see the progressive reduction in Systematic Risk over the transition period.
    *   **Economic Climate Modifier:** Adjust the economic climate during the simulation.
    *   **AI Innovation Index:** Adjust the AI innovation pace during the simulation.
5.  **Simulated Systematic Risk Over Time:** The application will display the simulated Systematic Risk at the specified month, along with a chart showing the evolution of Systematic Risk over the entire TTV period.
6.  **Understanding the TTV Simulation:** Expand the "Understanding the TTV Simulation" section to see a detailed explanation of the calculations used in the simulation.

<aside class="negative">
Note that the simulation assumes a linear transition between your current and target occupational hazards. In reality, the transition may not be so smooth.
</aside>

## Understanding the Key Concepts

Duration: 00:05

This application uses the following key concepts to model AI displacement risk:

*   **Idiosyncratic Risk (Vi(t)):** This reflects your personal vulnerability, influenced by factors within your control such as your human capital, the stability of your company, and your upskilling efforts.
*   **Systematic Risk (Hi):** This represents the unavoidable macro-level automation hazard of your occupation, adjusted by broader environmental conditions like the economic climate and the pace of AI innovation.
*   **Time-to-Value (TTV):** This is the time it takes to fully realize the benefits of a career transition.

By understanding these concepts and using the application, you can gain valuable insights into your career's exposure to AI-driven job displacement risk and make informed decisions about how to mitigate those risks.
