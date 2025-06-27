id: 685e9f966d454e734c158ea3_user_guide
summary: AI Risk Score - V4-2 User Guide
feedback link: https://docs.google.com/forms/d/e/1FAIpQLSfWkOK-in_bMMoHSZfcIvAeO58PAH9wrDqcxnJABHaxiDqhSA/viewform?usp=sf_link
environments: Web
status: Published
# AI Risk Score Codelab: Navigating Career Resilience in the Age of AI

This codelab provides a comprehensive guide to the AI Risk Score application, a tool designed to help you understand and manage your career risk in the face of increasing automation. The application allows you to assess your vulnerability to AI-driven job displacement and explore strategies to enhance your career resilience.

## Understanding the Core Concepts
Duration: 00:05

Before diving into the application, let's define the core concepts behind the AI Risk Score:

*   **Idiosyncratic Risk ($V_i(t)$):** This represents *your* individual vulnerability to job displacement. It's influenced by factors within your control, such as your skills, education, experience, and proactive upskilling efforts. Think of it as the risk that is specific to you as an individual.
*   **Systematic Risk ($H_i$):** This reflects the broader automation hazard inherent to your occupation or industry. It's influenced by external factors like the overall economic climate and the pace of AI innovation. This is the risk that affects *everyone* in your field, regardless of individual merit.
*   **"Education is Insurance":** Continuous learning and strategic career planning can act as "career insurance" against AI displacement. Investing in new skills or transitioning to a less vulnerable career path can reduce your risk profile and, conceptually, your "insurance premium".

<aside class="positive">
<b>Tip:</b> Understanding these concepts is crucial for effectively using the application and interpreting the results.
</aside>

## Navigating the Application
Duration: 00:02

The application consists of three main sections, accessible via the sidebar on the left:

1.  **Home:** Provides an overview of the AI Risk Score and its key concepts.
2.  **Risk & Premium Calculator:** Allows you to input your details and calculate your risk scores and estimated insurance premium.
3.  **Career Transition Simulator:** Enables you to explore how changing career paths can mitigate your systematic risk over time.

## Using the Risk & Premium Calculator
Duration: 00:15

The **Risk & Premium Calculator** is the core of the application. It allows you to assess your current risk profile based on various factors. Let's walk through the process:

1.  **Current Profile:** In the first column, you'll find several input fields related to your current professional situation:

    *   **Job Title:** Select your current job role from the dropdown menu. This influences your base occupational hazard.
    *   **Years of Experience:** Enter your total years of professional experience. Generally, more experience reduces idiosyncratic risk.
    *   **Highest Education Level:** Choose your highest educational attainment. Higher education levels can reduce idiosyncratic risk.
    *   **Education Field:** Select the field of your education. Fields with in-demand skills can reduce risk.
    *   **Institution Tier:** Choose the tier of your educational institution, serving as a proxy for training quality.
    *   **Company Type:** Select the type of company you work for, influencing company risk.

2.  **Upskilling Efforts:** In the second column, you'll find sliders to represent your investment in upskilling:

    *   **% General Skill Training Completed:** Indicates your progress in acquiring general, portable skills like coding or project management.
    *   **% Firm-Specific Skill Training Completed:** Shows your progress in skills specific to your current firm or tools.

3.  **Environmental Modifiers:** This section allows you to adjust the impact of external factors:

    *   **Economic Climate Modifier ($M_{econ}$):** Reflects the overall macroeconomic environment (e.g., 0.8 for recession, 1.2 for boom).
    *   **AI Innovation Index ($IAI$):** Reflects the velocity of technological change in AI (e.g., 0.8 for slowdown, 1.2 for rapid breakthrough).

4.  **Actuarial Parameters:** Finally, you can adjust the financial parameters used to calculate your estimated premium:

    *   **Annual Salary ($):** Your current annual salary.
    *   **Coverage Percentage (%):** The percentage of your salary covered in case of a claim.
    *   **Coverage Duration (Months):** The duration for which the payout would be made.
    *   **Loading Factor ($\lambda$):** An insurance multiplier to cover administrative costs and profit margin.
    *   **Minimum Monthly Premium ($P_{min}$):** The minimum monthly premium charged to ensure policy viability.

5.  **Calculated Risk Scores & Premium:** Once you've entered all the information, the application calculates and displays your:

    *   **Idiosyncratic Risk ($V_i(t)$)**
    *   **Systematic Risk ($H_i$)**
    *   **Monthly Premium ($P_{monthly}$)**

<aside class="positive">
<b>Best Practice:</b> Experiment with different input values to see how they affect your risk scores and premium. This will help you understand the factors that contribute to your career resilience.
</aside>

## Interpreting the Risk Scores and Premium
Duration: 00:10

The calculated risk scores and premium provide a quantitative assessment of your career risk:

*   **Idiosyncratic Risk ($V_i(t)$):** A lower score indicates a lower individual vulnerability to job displacement. Factors that contribute to a lower score include higher education, more experience, and proactive upskilling.
*   **Systematic Risk ($H_i$):** A lower score indicates a lower automation hazard for your occupation or industry. This score is influenced by the base hazard of your job title, the economic climate, and the pace of AI innovation.
*   **Monthly Premium ($P_{monthly}$):** This represents the estimated monthly insurance premium based on your risk profile. A lower risk profile translates to a lower premium.

<aside class="negative">
<b>Important:</b> The premium is calculated solely for educational purposes and is based on a simplified model. It should not be interpreted as an actual insurance quote.
</aside>

## Exploring Intermediate Calculations
Duration: 00:05

The **Risk & Premium Calculator** also provides detailed explanations of the intermediate calculations used to arrive at the final risk scores and premium. Expand the "Intermediate Calculations & Explanations" sections to understand the formulas and factors involved. This transparency allows you to gain deeper insights into the risk assessment process.

## Using the Career Transition Simulator
Duration: 00:10

The **Career Transition Simulator** allows you to explore how changing career paths can mitigate your systematic risk over time. This section is particularly useful for understanding the "Education is Insurance" concept.

1.  **Current & Target Career Paths:** In the first section, select your current and target job titles from the dropdown menus. The application will display the base occupational hazard ($H_{base}$) for each role.

2.  **Transition Parameters:** This section defines the parameters of your career transition:

    *   **Time-to-Value (TTV) Period (Months):** The total number of months required for the transition to be fully effective, meaning your risk profile aligns with the new career.
    *   **Months Elapsed Since Transition Started ($k$):** The number of months passed since you began your transition.

3.  **Environmental Modifiers (for simulation):** Adjust the economic climate and AI innovation index to see how they affect systematic risk during your transition.

4.  **Simulation Results: Systematic Risk Evolution:** The application calculates and displays your projected Systematic Risk ($H_i$) at the specified number of months elapsed. It also presents a line chart illustrating how your Systematic Risk is projected to change as you progress through your career transition.

<aside class="positive">
<b>Experiment:</b> Try different target career paths and TTV periods to see how they impact your systematic risk. This will help you identify career paths that offer greater resilience in the face of automation.
</aside>

## Interpreting the Career Transition Simulation
Duration: 00:03

The line chart in the **Career Transition Simulator** shows how your Systematic Risk ($H_i$) is projected to decrease as you transition to a new career path with a lower base occupational hazard. The speed of this reduction depends on the TTV period you specify. This demonstrates the power of career path diversification as a strategy to mitigate long-term AI-driven displacement risk.

By understanding and utilizing the features of the AI Risk Score application, you can gain valuable insights into your career risk and develop effective strategies to enhance your career resilience in the age of AI.
