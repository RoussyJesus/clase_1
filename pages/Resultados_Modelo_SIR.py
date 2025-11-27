import dash 
from dash import html, dcc
import plotly.graph_objects as go
import numpy as np
from scipy.integrate import odeint

dash.register_page(__name__, path="/Proyecto/evolucion_susceptibles", name="Resultados: Susceptibles S(t)")

COLOR_LINEA_PRINCIPAL = '#00CFFF' 
COLOR_TITULO = '#d36bff'      
COLOR_TEXTO_SECUNDARIO = '#e0e0e0' 
COLOR_FONDO_GRAFICO = '#0c162b'    
COLOR_FONDO_PAPEL = '#0a101f'      
COLOR_GRID = '#333'             

def modelo_sir(y, t, b, g):
    S, I, R = y
    dS_dt = -b * S * I
    dI_dt = b * S * I - g * I
    dR_dt = g * I
    return [dS_dt, dI_dt, dR_dt]

N = 10000.0
I0 = 10.0 
S0 = N - I0
R0_init = 0.0
y0 = [S0, I0, R0_init]
t = np.linspace(0, 100, 100)

gamma_base = 0.25
R0_base = 2.5
beta_base = R0_base * gamma_base / N

sol1 = odeint(modelo_sir, y0, t, args=(beta_base, gamma_base))
S1 = sol1[:, 0]

beta_double = beta_base * 2
sol2 = odeint(modelo_sir, y0, t, args=(beta_double, gamma_base))
S2 = sol2[:, 0]

gamma_double = gamma_base * 2
sol3 = odeint(modelo_sir, y0, t, args=(beta_base, gamma_double))
S3 = sol3[:, 0]

def crear_grafico_susceptibles(tiempo, datos_s, titulo, y_range=None):
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=tiempo, y=datos_s, mode='lines', 
        name='S(t)',
        line=dict(color=COLOR_LINEA_PRINCIPAL, width=2.5)
    ))

    fig.update_layout(
        title=dict(text=f"<b>{titulo}</b>", x=0.5, font=dict(size=14, color=COLOR_TITULO)),
        xaxis_title="Dias",
        yaxis_title="Personas",
        paper_bgcolor=COLOR_FONDO_PAPEL,
        plot_bgcolor=COLOR_FONDO_GRAFICO,
        font=dict(color=COLOR_TEXTO_SECUNDARIO, size=10),
        margin=dict(l=40, r=20, t=50, b=40),
        height=300
    )
    
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor=COLOR_GRID, griddash='dot', zeroline=False, linecolor=COLOR_TEXTO_SECUNDARIO, mirror=True)
    
    yaxis_config = dict(showgrid=True, gridwidth=1, gridcolor=COLOR_GRID, griddash='dot', zeroline=False, linecolor=COLOR_TEXTO_SECUNDARIO, mirror=True)
    if y_range:
        yaxis_config['range'] = y_range
        
    fig.update_yaxes(yaxis_config)
    
    return fig

fig_base = crear_grafico_susceptibles(t, S1, "S(t) - baseline (escenario)", y_range=[0, 10500])
fig_b_double = crear_grafico_susceptibles(t, S2, "S(t) - b_double (escenario)", y_range=[0, 10500])
fig_k_double = crear_grafico_susceptibles(t, S3, "S(t) - k_double (escenario)", y_range=[6000, 10200])

layout = html.Div([
    html.H1("Evolución de Susceptibles S(t)", 
            style={'textAlign': 'center', 'color': COLOR_TITULO, 'paddingBottom': '20px', 'fontSize': '24px'}),

    html.Div([
        html.Div([
            html.Div([dcc.Graph(figure=fig_base, config={'displayModeBar': False})],
                     style={'flex': '1', 'minWidth': '300px', 'padding': '10px'}),
            html.Div([dcc.Graph(figure=fig_b_double, config={'displayModeBar': False})],
                     style={'flex': '1', 'minWidth': '300px', 'padding': '10px'}),
        ], style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'center', 'width': '100%'}),

        html.Div([
            html.Div([
                dcc.Graph(figure=fig_k_double, config={'displayModeBar': False})
            ], style={'width': '60%', 'minWidth': '300px', 'margin': '0 auto', 'padding': '10px'})
        ], style={'width': '100%', 'marginTop': '10px'}),

    ], style={'backgroundColor': COLOR_FONDO_GRAFICO, 'borderRadius': '15px', 'padding': '20px', 'boxShadow': '0 0 15px rgba(0,0,0,0.5)'}),

    html.Div([
        html.H4("Interpretación: Agotamiento de Susceptibles", style={'color': COLOR_LINEA_PRINCIPAL}),
        dcc.Markdown(r'''
        Los gráficos muestran cómo disminuye la población de **Susceptibles** $S(t)$:

        1. **Baseline:** La población susceptible cae hasta quedar ~1000 personas.
        2. **b_double:** El agotamiento es casi total y muy rápido.
        3. **k_double:** La curva termina en ~6300 personas; la epidemia se extingue pronto.
        ''', mathjax=True, style={'color': COLOR_TEXTO_SECUNDARIO})
    ], style={'marginTop': '30px', 'maxWidth': '800px', 'marginLeft': 'auto', 'marginRight': 'auto'})

], style={
    'backgroundColor': COLOR_FONDO_PAPEL, 
    'minHeight': '100vh', 
    'padding': '20px',
    'fontFamily': 'sans-serif'
})
