
import plotly.express as px
import pandas as pd

def plot_systematic_risk_over_time(df_risk_over_time):
    # Plotly line chart for systematic risk over time during transition
    fig = px.line(df_risk_over_time, x='Months Elapsed', y='Systematic Risk ($H_i$)',
                  title='Projected Systematic Risk Reduction During Career Transition',
                  labels={'Systematic Risk ($H_i$)': 'Systematic Risk Score'},
                  line_shape="spline", render_mode="svg")

    fig.update_traces(mode='lines+markers', hovertemplate="<br>Months: %{x}<br>Risk: %{y:.2f}")
    fig.update_layout(hovermode="x unified",
                      xaxis_title="Months Elapsed Since Transition Started",
                      yaxis_title="Systematic Risk Score ($H_i$)",
                      template="plotly_white",
                      title_x=0.5)
    fig.update_yaxes(range=[0, 100]) # Assuming risk scores are 0-100

    return fig

def plot_factor_impact_bar_chart(fhc, fcr, fus):
    # Bar chart comparing the relative impact of FHC, FCR, and FUS on V_raw
    # For a simplified representation, we can just show their normalized values
    # or their contribution to V_raw. Let's show their values directly.
    data = {'Factor': ['Human Capital (FHC)', 'Company Risk (FCR)', 'Upskilling (FUS)'],
            'Value': [fhc, fcr, fus]}
    df = pd.DataFrame(data)

    fig = px.bar(df, x='Factor', y='Value',
                 title='Contribution of Factors to Idiosyncratic Risk',
                 labels={'Value': 'Factor Value (Lower is Better)', 'Factor': 'Risk Factor'},
                 color='Factor',
                 color_discrete_map={
                     'Human Capital (FHC)': 'blue',
                     'Company Risk (FCR)': 'green',
                     'Upskilling (FUS)': 'red'
                 })

    fig.update_layout(xaxis_title="",
                      yaxis_title="Factor Value (Lower is Better)",
                      template="plotly_white",
                      title_x=0.5,
                      yaxis_range=[0, 1.0]) # Factors are typically multipliers, so 0-1 range is appropriate

    fig.update_traces(hovertemplate="Factor: %{x}<br>Value: %{y:.2f}")

    return fig
