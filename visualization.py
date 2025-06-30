
import plotly.express as px
import pandas as pd

def plot_systematic_risk_evolution(df_risk_evolution, current_month):
    """
    Generates a Plotly line chart showing the simulated H_i value over the TTV period.
    """
    fig = px.line(df_risk_evolution, x='Month', y='Systematic Risk (H_i)',
                  title='Systematic Risk Evolution During Career Transition',
                  labels={'Month': 'Months Since Transition Started', 'Systematic Risk (H_i)': 'Systematic Risk Score (H_i)'},
                  markers=True)

    fig.add_vline(x=current_month, line_width=2, line_dash="dash", line_color="red",
                  annotation_text=f"Current Month: {int(current_month)}",
                  annotation_position="top right")

    fig.update_layout(hovermode="x unified")
    fig.update_traces(hovertemplate="<br>".join([
        "Month: %{x}",
        "Systematic Risk (H_i): %{y:.2f}"
    ]))

    return fig

def plot_risk_factor_contributions(idiosyncratic_factors, systematic_factors):
    """
    Generates bar charts for Idiosyncratic and Systematic Risk factor contributions.
    """

    # Idiosyncratic Risk Factors
    id_df = pd.DataFrame(list(idiosyncratic_factors.items()), columns=['Factor', 'Value'])
    fig_id = px.bar(id_df, x='Factor', y='Value',
                    title='Idiosyncratic Risk Factor Contributions',
                    labels={'Value': 'Factor Value'},
                    text='Value')
    fig_id.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    fig_id.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')

    # Systematic Risk Factors (weights * values)
    sys_df = pd.DataFrame(list(systematic_factors.items()), columns=['Factor', 'Value'])
    fig_sys = px.bar(sys_df, x='Factor', y='Value',
                     title='Systematic Risk Factor Contributions',
                     labels={'Value': 'Factor Value'},
                     text='Value')
    fig_sys.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    fig_sys.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')

    return fig_id, fig_sys
