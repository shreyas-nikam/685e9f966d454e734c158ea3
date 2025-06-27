
# AI Risk Score - V4-2: Career Path Diversification Tool

## Overview

The "Career Path Diversification Tool" is a Streamlit application designed to help users understand and mitigate their exposure to systematic AI risk in their careers. Inspired by concepts from recent advancements in AI, this tool allows users to explore how different career choices and personal development efforts influence their AI displacement risk profile and potential insurance premiums. It focuses on illustrating "Systematic Risk Exposure Mitigation" or "Career Path Diversification" by simulating the impact of career transitions and skill acquisition on an individual's overall risk score.

This application transforms raw synthetic data into interactive visualizations, providing detailed insights and explanations directly on the charts. Users can interact with input forms and widgets to experiment with various parameters and observe real-time updates, thereby gaining a clear understanding of key concepts such as Idiosyncratic Risk, Systematic Risk, and their implications for career resilience.

## Core Concepts and Mathematical Foundations

This section details the fundamental mathematical models and concepts implemented in the application.

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

## Setup and Usage

To run this Streamlit application locally, follow these steps:

1.  **Clone the repository:**
    \`\`\`bash
    git clone [repository-url]
    cd [repository-name]
    \`\`\`
2.  **Create a virtual environment (recommended):**
    \`\`\`bash
    python -m venv venv
    source venv/bin/activate  # On Windows: .\venv\Scripts\activate
    \`\`\`
3.  **Install the dependencies:**
    \`\`\`bash
    pip install -r requirements.txt
    \`\`\`
4.  **Run the Streamlit application:**
    \`\`\`bash
    streamlit run app.py
    \`\`\`

The application will open in your default web browser.

## Project Structure

\`\`\`
.
├── app.py
├── requirements.txt
├── Dockerfile
├── README.md
├── application_pages/
│   ├── __init__.py
│   ├── home_page.py
│   └── simulation_page.py
├── data_utils.py
├── calculations.py
└── visualization.py
\`\`\`

## Contact

For any questions or feedback, please contact QuantUniversity.
