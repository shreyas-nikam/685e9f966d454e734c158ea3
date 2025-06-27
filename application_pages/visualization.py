
import plotly.express as px
import pandas as pd

def plot_systematic_risk_over_time(df_risk_over_time):
    """
    Generates a Plotly line chart showing the simulated Systematic Risk (H_i)
    value over the TTV period as k progresses.
    """
    fig = px.line(df_risk_over_time, x='Months Elapsed', y='Systematic Risk (H_i)',
                  title='Projected Systematic Risk Reduction During Career Transition',
                  labels={'Months Elapsed': 'Months Since Transition Started',
                          'Systematic Risk (H_i)': 'Systematic Risk Score (H_i)'},
                  markers=True)

    fig.update_layout(hovermode="x unified",
                      xaxis_title="Months Elapsed Since Transition Started (k)",
                      yaxis_title="Systematic Risk Score (H_i)",
                      template="plotly_white",
                      font=dict(size=12))
    fig.update_traces(hovertemplate='Months: %{x}<br>Systematic Risk: %{y:.2f}<extra></extra>')

    return fig

def plot_factor_impact_bar_chart(fhc, fcr, fus, h_base, m_econ, iai):
    """
    Generates a Plotly bar chart comparing the relative impact of FHC, FCR, and FUS
    on V_raw, and H_base, M_econ, IAI on H_i.
    This is a conceptual plot to visualize contributions, actual contribution logic
    would be more complex if factors were truly additive/percentage based.
    For simplicity, we show the values of the factors themselves.
    """
    # Idiosyncratic Risk Factors
    idiosyncratic_data = pd.DataFrame({
        'Factor': ['Human Capital (FHC)', 'Company Risk (FCR)', 'Upskilling (FUS)'],
        'Value': [fhc, fcr, fus]
    })
    fig_idiosyncratic = px.bar(idiosyncratic_data, x='Factor', y='Value',
                               title='Contribution to Idiosyncratic Risk Factors',
                               labels={'Value': 'Factor Value'},
                               color='Factor',
                               color_discrete_map={
                                   'Human Capital (FHC)': 'skyblue',
                                   'Company Risk (FCR)': 'lightcoral',
                                   'Upskilling (FUS)': 'lightgreen'
                               })
    fig_idiosyncratic.update_layout(yaxis_title="Factor Value", xaxis_title="", template="plotly_white", font=dict(size=12))

    # Systematic Risk Factors
    systematic_data = pd.DataFrame({
        'Modifier': ['Base Occupational Hazard (H_base)', 'Economic Climate (M_econ)', 'AI Innovation Index (IAI)'],
        'Value': [h_base, m_econ, iai]
    })
    fig_systematic = px.bar(systematic_data, x='Modifier', y='Value',
                            title='Contribution to Systematic Risk Modifiers',
                            labels={'Value': 'Modifier Value'},
                            color='Modifier',
                            color_discrete_map={
                                'Base Occupational Hazard (H_base)': 'skyblue',
                                'Economic Climate (M_econ)': 'lightcoral',
                                'AI Innovation Index (IAI)': 'lightgreen'
                            })
    fig_systematic.update_layout(yaxis_title="Modifier Value", xaxis_title="", template="plotly_white", font=dict(size=12))

    return fig_idiosyncratic, fig_systematic
