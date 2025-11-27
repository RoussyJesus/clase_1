import dash 
from dash import html, dcc
import plotly.graph_objects as go
import numpy as np
from scipy.integrate import odeint

dash.register_page(__name__, path="/Proyecto/comparacion_de_las_curvas", name="Resultados: Comparación I(t)")

COLOR_BASELINE = '#00CFFF'
COLOR_BETA_HIGH = '#FF9F1C'
COLOR_GAMMA_HIGH = '#39FF14'
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
I_base = sol1[:, 1] 

beta_double = beta_base * 2
sol2 = odeint(modelo_sir, y0, t, args=(beta_double, gamma_base))
I_beta = sol2[:, 1]

gamma_double = gamma_base * 2
sol3 = odeint(modelo_sir, y0, t, args=(beta_base, gamma_double))
I_gamma = sol3[:, 1]

def crear_grafico_comparativo(tiempo, i_base, i_beta, i_gamma):
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=tiempo, y=i_base, mode='lines', 
        name='baseline',
        line=dict(color=COLOR_BASELINE, width=2.5)
    ))

    fig.add_trace(go.Scatter(
        x=tiempo, y=i_beta, mode='lines', 
        name='b_double',
        line=dict(color=COLOR_BETA_HIGH, width=2.5)
    ))

    fig.add_trace(go.Scatter(
        x=tiempo, y=i_gamma, mode='lines', 
        name='k_double',
        line=dict(color=COLOR_GAMMA_HIGH, width=2.5)
    ))

    fig.update_layout(
        title=dict(
            text="<b>Comparación I(t) entre escenarios</b>",
            x=0.5, font=dict(size=18, color=COLOR_TITULO)
        ),
        xaxis_title="Días",
        yaxis_title="Personas",
        paper_bgcolor=COLOR_FONDO_PAPEL,
        plot_bgcolor=COLOR_FONDO_GRAFICO,
        font=dict(color=COLOR_TEXTO_SECUNDARIO, size=12),
        margin=dict(l=50, r=40, t=70, b=50),
        height=450, 
        legend=dict(
            orientation="v",
            yanchor="top",
            y=0.99,
            xanchor="right",
            x=0.99,
            bgcolor="rgba(0,0,0,0.5)"
        )
    )
    
    fig.update_xaxes(
        showgrid=True, gridwidth=1, gridcolor=COLOR_GRID, griddash='dot',
        zeroline=False, linecolor=COLOR_TEXTO_SECUNDARIO, mirror=True
    )
    fig.update_yaxes(
        showgrid=True, gridwidth=1, gridcolor=COLOR_GRID, griddash='dot',
        zeroline=False, linecolor=COLOR_TEXTO_SECUNDARIO, mirror=True
    )
    
    return fig

fig_comparacion = crear_grafico_comparativo(t, I_base, I_beta, I_gamma)

layout = html.Div([
    
    html.H1("Comparación de Dinámicas de Difusión", 
            style={'textAlign': 'center', 'color': COLOR_TITULO, 'paddingBottom': '20px', 'fontSize': '28px'}),

    html.Div([
        dcc.Graph(figure=fig_comparacion, config={'displayModeBar': False})
    ], style={
        'backgroundColor': COLOR_FONDO_GRAFICO, 
        'borderRadius': '15px', 
        'padding': '20px', 
        'boxShadow': '0 0 20px rgba(0,0,0,0.3)',
        'maxWidth': '900px',
        'margin': '0 auto'
    }),

    html.Div([
        html.H3("Análisis de Sensibilidad de Parámetros", style={'color': COLOR_BASELINE, 'marginTop': '30px'}),
        
        dcc.Markdown(r'''
        El gráfico compara la evolución de los **Promotores Activos** $I(t)$ bajo tres condiciones distintas, ilustrando el efecto de variar los parámetros $\beta$ y $\gamma$:

        1.  **<span style="color:#00CFFF">Baseline (Línea Azul):</span>** Escenario base ($R_0 \approx 2.5$). Muestra un pico moderado alrededor del día 25.
        
        2.  **<span style="color:#FF9F1C">b_double (Línea Naranja):</span>** Al duplicar la **tasa de contacto ($\beta$)**, se observa una aceleración drástica. La difusión se amplifica, alcanzando un pico mucho más alto (casi 5000 personas) y mucho más temprano (día 10-12).
        
        3.  **<span style="color:#39FF14">k_double (Línea Verde):</span>** Al duplicar la **tasa de desinterés/recuperación ($\gamma$)**, la adopción global se reduce significativamente. La curva se aplana, retrasando y disminuyendo el número máximo de usuarios activos simultáneos.
        ''', mathjax=True, dangerously_allow_html=True, style={'color': COLOR_TEXTO_SECUNDARIO, 'lineHeight': '1.6', 'fontSize': '16px'})
        
    ], style={'maxWidth': '900px', 'margin': '0 auto', 'padding': '0 20px'})

], style={
    'backgroundColor': COLOR_FONDO_PAPEL, 
    'minHeight': '100vh', 
    'padding': '30px',
    'fontFamily': 'sans-serif'
})
