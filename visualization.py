
import plotly.express as px
import pandas as pd

def plot_risk_evolution(simulation_data):
    # simulation_data is expected to be a DataFrame with 'Month' and 'Systematic Risk (H_i)'
    fig = px.line(
        simulation_data,
        x='Month',
        y='Systematic Risk (H_i)',
        title='Systematic Risk Evolution During Career Transition',
        labels={'Systematic Risk (H_i)': 'Systematic Risk (H_i) Score'},
        markers=True
    )
    fig.update_traces(marker=dict(size=8))
    fig.update_layout(hovermode="x unified")
    fig.update_xaxes(title_text='Months Elapsed Since Transition Started')
    fig.update_yaxes(title_text='Systematic Risk Score (H_i)')

    # Add annotations for start and end points
    if not simulation_data.empty:
        # Start point
        fig.add_annotation(
            x=simulation_data['Month'].iloc[0],
            y=simulation_data['Systematic Risk (H_i)'].iloc[0],
            text=f"Start (H_i: {simulation_data['Systematic Risk (H_i)'].iloc[0]:.2f})",
            showarrow=True,
            arrowhead=2,
            ax=-50,
            ay=-30
        )
        # End point
        fig.add_annotation(
            x=simulation_data['Month'].iloc[-1],
            y=simulation_data['Systematic Risk (H_i)'].iloc[-1],
            text=f"End (H_i: {simulation_data['Systematic Risk (H_i)'].iloc[-1]:.2f})",
            showarrow=True,
            arrowhead=2,
            ax=50,
            ay=-30
        )

    return fig

def plot_factor_impact(fhc, fcr, fus):
    factors = pd.DataFrame({
        'Factor': ['Human Capital (FHC)', 'Company Risk (FCR)', 'Upskilling (FUS)'],
        'Value': [fhc, fcr, fus]
    })
    fig = px.bar(
        factors,
        x='Factor',
        y='Value',
        title='Impact of Idiosyncratic Risk Factors',
        labels={'Value': 'Factor Value'},
        color='Factor',
        template='plotly_white'
    )
    fig.update_layout(xaxis_title="Factor Type", yaxis_title="Calculated Factor Value")
    return fig

