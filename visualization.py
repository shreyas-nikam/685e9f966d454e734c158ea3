import plotly.express as px
import pandas as pd

def plot_systematic_risk_evolution(simulation_data):
    """
    Generates a Plotly line chart showing the simulated Systematic Risk evolution
    over a career transition period.

    Args:
        simulation_data (pd.DataFrame): DataFrame with 'Month' and 'Systematic Risk' columns.
    """
    fig = px.line(
        simulation_data,
        x="Month",
        y="Systematic Risk",
        title="Systematic Risk Evolution During Career Transition",
        labels={"Month": "Months Elapsed Since Transition Start", "Systematic Risk": "Systematic Risk Score ($H_i$)"},
        markers=True,
        line_shape="linear"
    )

    fig.update_layout(
        hovermode="x unified",
        xaxis_title="Months Elapsed Since Transition Started ($k$)",
        yaxis_title="Systematic Risk Score ($H_i$)"
    )

    fig.update_traces(
        hovertemplate="""<b>Month:</b> %{x}<br>
<b>Systematic Risk ($H_i$):</b> %{y:.2f}
<extra></extra>"""
    )
    return fig

def plot_factor_contributions_v_raw(FHC, FCR, FUS, w_CR, w_US):
    """
    Generates a Plotly bar chart showing contributions of FHC, FCR, FUS to V_raw.
    """
    # V_raw = FHC * (w_CR * FCR + w_US * FUS)
    # To represent contributions, we can show relative impact or just the weighted components.
    # For a simplified visualization of relative impact, let's consider the components
    # that form the sum inside the parenthesis, scaled by FHC.
    
    data = {
        'Factor Component': ['Human Capital (FHC)', 'Company Risk (FCR)', 'Upskilling (FUS)'],
        'Value': [FHC, FCR * FHC, FUS * FHC] # Scaling by FHC to show their multiplicative effect
    }
    df = pd.DataFrame(data)

    fig = px.bar(df, x='Factor Component', y='Value',
                 title='Relative Contribution of Factors to Raw Idiosyncratic Risk (Scaled)',
                 labels={'Value': 'Contribution Value', 'Factor Component': 'Risk Factor'},
                 color='Factor Component') # Differentiate bars by color
    
    fig.update_layout(
        yaxis_title="Scaled Factor Value (Higher = More Risk)"
    )
    
    return fig

def plot_factor_contributions_hi(H_base, M_econ, IAI, w_econ, w_inno):
    """
    Generates a Plotly bar chart showing contributions of H_base, M_econ, IAI to H_i.
    """
    # H_i = H_base * (w_econ * M_econ + w_inno * IAI)
    # We can show the H_base and then the weighted modifiers' impact.
    
    data = {
        'Component': [r'Base Hazard ($H_{base}$)', r'Economic Modifier ($M_{econ}$)', r'AI Innovation ($IAI$)'],
        'Value': [H_base, H_base * w_econ * M_econ, H_base * w_inno * IAI]
    }
    df = pd.DataFrame(data)

    fig = px.bar(df, x='Component', y='Value',
                 title=r'Relative Contribution to Systematic Risk ($H_i$) Components',
                 labels={'Value': 'Contribution Value', 'Component': 'Systematic Risk Component'},
                 color='Component')
    
    fig.update_layout(
        yaxis_title="Scaled Component Value (Higher = More Risk)"
    )

    return fig