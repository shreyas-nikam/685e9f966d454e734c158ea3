id: 685e9f966d454e734c158ea3_user_guide
summary: AI Risk Score - V4-2 User Guide
feedback link: https://docs.google.com/forms/d/e/1FAIpQLSfWkOK-in_bMMoHSZfcIvAeO58PAH9wrDqcxnJABHaxiDqhSA/viewform?usp=sf_link
environments: Web
status: Published
# AI Risk Score - Career Path Diversification Tool: A User Guide

This codelab will guide you through the functionalities of the AI Risk Score application. This application is designed to help you understand and potentially mitigate your exposure to AI-driven job displacement. We will explore how different career choices, upskilling efforts, and external factors influence your AI displacement risk profile. This tool provides insights into potential insurance premiums, offering a comprehensive view of your career's risk landscape.

## Understanding AI Displacement Risk
Duration: 00:05

Before diving into the application, it's essential to understand the core concepts:

*   **Idiosyncratic Risk ($V_i(t)$):** This represents the part of your job security that you can control. It's influenced by your skills, education, experience, and the stability of your employer.

*   **Systematic Risk ($H_i$):** This reflects the broader, macro-level risk associated with your occupation and industry due to automation. It's affected by the economic climate and the rate of AI innovation.

This application helps you understand how these risks are calculated and how you can manage them.

## Navigating the Application Interface
Duration: 00:03

The application is divided into several key sections:

*   **Sidebar (Input Panel):** Located on the left, this area allows you to input your personal and professional details, simulate career transitions, and adjust environmental parameters.

*   **Risk Assessment Results:** The main area displays your calculated Idiosyncratic and Systematic Risk scores, along with an estimated monthly insurance premium.

*   **Tabs (Detailed Risk Factors, Actuarial Breakdown, Career Transition Simulation):** These tabs provide deeper insights into the factors contributing to your risk scores, the actuarial calculations behind the premium, and a simulation of career path diversification.

## Defining Your Current Profile
Duration: 00:07

Let's start by defining your current professional profile in the sidebar, inside the "Current Profile" expander.

1.  **Job Title:** Select your current job title from the dropdown menu. This selection influences your base AI hazard score and role multiplier.

2.  **Years of Experience:** Enter the number of years of professional experience you have. This affects the Human Capital Factor, assuming experience reduces vulnerability.

3.  **Education Level:** Choose your highest level of education. Higher education levels are generally associated with lower risk.

4.  **Education Field:** Select the field in which you received your education. Certain fields, like technology and engineering, may be less vulnerable to AI displacement.

5.  **Institution Tier:** Indicate the tier of the institution where you received your education. Higher-ranked institutions may provide more robust preparation for a changing job market.

6.  **Company Type:** Select the type of company you currently work for. Larger, more stable companies may present less risk than startups.

<aside class="positive">
 The selected <b>Job Title</b> will affect the  <b>Base Occupational Hazard</b>, while other factors affect your <b>Human Capital</b>
</aside>

## Evaluating Upskilling Efforts
Duration: 00:05

Next, expand the "Upskilling Efforts" section in the sidebar.

1.  **% General Skill Training Completed:** Use the slider to indicate the percentage of general, transferable skills training you have completed. These skills are broadly applicable across industries (e.g., programming, project management).

2.  **% Firm-Specific Skill Training Completed:** Use the slider to indicate the percentage of firm-specific skills training you have completed. These skills are highly specific to your current company or its unique processes.

The application differentiates between these skill types, rewarding general skills more heavily, as they increase your adaptability.

## Understanding Risk Assessment Results
Duration: 00:05

After entering your profile information and upskilling efforts, the "Risk Assessment Results" section will display your calculated risk scores:

*   **Idiosyncratic Risk ($V_i(t)$):** This metric reflects your individual vulnerability to job displacement. A lower score is better, indicating less risk. It is based on your Human Capital, Company Risk, and Upskilling efforts.

*   **Systematic Risk ($H_i$):** This represents the inherent risk of your occupation or industry. A lower score is better, indicating less risk. It is influenced by your job's base hazard, the economic climate, and the pace of AI innovation.

*   **Estimated Monthly Premium ($P_{monthly}$):** This is a hypothetical insurance premium reflecting the financial quantification of your combined risk. A lower premium is better, indicating less overall risk.

These metrics provide a high-level overview of your AI displacement risk profile.

## Exploring Detailed Risk Factors
Duration: 00:10

Click on the "Detailed Risk Factors" tab to gain a deeper understanding of the factors contributing to your risk scores.

This tab breaks down the key components of both Idiosyncratic and Systematic Risk:

*   **Idiosyncratic Risk Factors:**
    *   **Human Capital Factor ($FHC$):** Details about how your foundational resilience (education, experience, institution) is factored in.
    *   **Company Risk Factor ($FCR$):** Information on how your employer's stability and AI adoption influence your risk.
    *   **Upskilling Factor ($FUS$):** Insights into how your proactive efforts in general and firm-specific training affect your risk.
    A bar chart visually represents the relative contribution of each factor to your Raw Idiosyncratic Risk.

*   **Systematic Risk Factors:**
    *   **Base Occupational Hazard ($H_{base}$):** The inherent risk associated with your job role.
    *   **Economic Climate Modifier ($M_{econ}$):** Reflects the impact of macroeconomic conditions.
    *   **AI Innovation Index ($IAI$):** Represents the pace of technological change.
    A bar chart illustrates the relative contribution of each component to your Systematic Risk.

## Analyzing Actuarial Breakdown
Duration: 00:07

Click on the "Actuarial Breakdown" tab to see how your risk scores are translated into a potential monthly insurance premium.

This tab presents a step-by-step breakdown of the calculations:

1.  **Total Payout Amount ($L_{payout}$):** The total potential payout if a claim is triggered, based on your annual salary, coverage percentage, and coverage duration.

2.  **Annual Claim Probability ($P_{claim}$):** The likelihood of a job displacement claim in a year, calculated as the joint probability of a systemic event and an individual loss given that event. This is based on probability of systematic event and conditional probability of individual loss.

3.  **Annual Expected Loss ($E[Loss]$):** The expected financial loss per year, calculated as the product of the annual claim probability and the total payout amount.

4.  **Monthly Insurance Premium ($P_{monthly}$):** Your final estimated monthly premium, calculated based on the annual expected loss and a loading factor, with a minimum premium applied.

This section provides transparency into the actuarial calculations driving the premium.

## Simulating Career Path Diversification
Duration: 00:10

Click on the "Career Transition Simulation" tab to explore how career path diversification can mitigate your Systematic Risk over time.

1.  **Check "Simulate Career Transition" in the Sidebar:** This activates the simulation, allowing you to select a target career path.

2.  **Select Target Career Path:** Choose a career path with a lower inherent AI hazard ($H_{target}$) from the dropdown menu.

3.  **Transition Time-to-Value (TTV) in Months:** Enter the number of months it will take to fully transition to the target career path.

4.  **Months Elapsed Since Transition Started:** Use the slider to simulate the progression of your career transition.

A line chart visualizes the projected decrease in Systematic Risk ($H_i$) as you transition to the target career path. As the slider advances, you can observe the impact of career diversification on your overall risk profile.

<aside class="positive">
    This <b>Career Transition Simulation</b> shows the importance of adapting and gaining new skills to be ready for the job market of the future!
</aside>

## Adjusting Environmental Modifiers
Duration: 00:05

The "Environmental Modifiers" section in the sidebar allows you to simulate different macroeconomic conditions and AI innovation paces.

*   **Economic Climate Modifier ($M_{econ}$):** Adjust this slider to reflect different economic conditions. 0.8 represents a recession, 1.0 represents a normal economy, and 1.2 represents a boom.

*   **AI Innovation Index ($IAI$):** Adjust this slider to reflect the pace of technological change. 0.8 represents a slowdown in AI innovation, 1.0 represents a normal pace, and 1.2 represents rapid breakthroughs.

These sliders affect your Systematic Risk ($H_i$), demonstrating the impact of external factors on your job security.

<aside class="negative">
    Please note that QuCreate relies on AI models for generating code, which may contain inaccuracies or errors.
</aside>
