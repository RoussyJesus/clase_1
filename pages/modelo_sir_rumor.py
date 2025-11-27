import dash 
from dash import html, dcc
import plotly.graph_objects as go
import numpy as np
from scipy.integrate import odeint

dash.register_page(__name__, path="/Proyecto/modelo_sir_rumor", name="Modelo SIR de Rumor")

COLOR_SUCEPTIBLES = '#00CFFF'
COLOR_INFECTADOS = '#FF4136'
COLOR_RACIONALES = '#39FF14'
COLOR_TITULO = '#d36bff'
COLOR_TEXTO_SECUNDARIO = '#e0e0e0'
COLOR_FONDO_GRAFICO = '#0c162b'
COLOR_FONDO_PAPEL = '#0a101f'
COLOR_GRID = '#333'
COLOR_ZEROLINE = '#b807ff'

def modelo_rumor(y, t, b, k):
    S, I, R = y
    dS_dt = -b * S * I
    dI_dt = (b * S * I) - (k * I * R)
    dR_dt = k * I * R
    return [dS_dt, dI_dt, dR_dt]

S0 = 266.0
I0 = 1.0
R0 = 8.0
y0 = [S0, I0, R0]
N = S0 + I0 + R0

b = 0.004
t = np.linspace(0, 15, 150)

k1 = 0.01
sol1 = odeint(modelo_rumor, y0, t, args=(b, k1))
S1, I1, R1 = sol1.T

k2 = 0.02
sol2 = odeint(modelo_rumor, y0, t, args=(b, k2))
S2, I2, R2 = sol2.T

def crear_grafico(tiempo, s_data, i_data, r_data, titulo_k):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=tiempo, y=s_data, mode='lines', name='Susceptibles (S)',
                             line=dict(color=COLOR_SUCEPTIBLES, width=2.5)))
    fig.add_trace(go.Scatter(x=tiempo, y=i_data, mode='lines', name='Infectados (I)',
                             line=dict(color=COLOR_INFECTADOS, width=3),
                             fill='tozeroy', fillcolor='rgba(255, 65, 54, 0.2)'))
    fig.add_trace(go.Scatter(x=tiempo, y=r_data, mode='lines', name='Racionalizados (R)',
                             line=dict(color=COLOR_RACIONALES, width=2.5)))

    fig.update_layout(
        title=dict(text=f"<b>Evolución del Rumor ({titulo_k})</b>", x=0.5,
                   font=dict(size=16, color=COLOR_TITULO)),
        xaxis_title="Tiempo (días)",
        yaxis_title="Número de personas",
        paper_bgcolor=COLOR_FONDO_PAPEL,
        plot_bgcolor=COLOR_FONDO_GRAFICO,
        font=dict(color=COLOR_TEXTO_SECUNDARIO),
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        margin=dict(l=40, r=40, t=60, b=40),
        height=400
    )
    
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor=COLOR_GRID,
                     zeroline=True, zerolinewidth=2, zerolinecolor=COLOR_ZEROLINE,
                     range=[0, 15])
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor=COLOR_GRID,
                     range=[0, N * 1.05])
    return fig

fig_k1 = crear_grafico(t, S1, I1, R1, "Escenario k = 1")
fig_k2 = crear_grafico(t, S2, I2, R2, "Escenario k = 2")

texto_ecuaciones = r"""
**Modelo Matemático del Rumor:**

$$ \frac{dS}{dt} = -bSI $$

$$ \frac{dI}{dt} = bSI - kIR $$

$$ \frac{dR}{dt} = kIR $$

Donde $I(t)$ interactúa con $R(t)$ para detener el rumor.
"""

texto_parametros = f"""
**Parámetros:**
* $S_0 = {int(S0)}$ (Alumnos)
* $I_0 = {int(I0)}$ (Propagador)
* $R_0 = {int(R0)}$ (Docentes Racionales)
* $b = {b}$ (Tasa transmisión)
* Escenario 1: $k = 0.01$ (Factor Escala "1")
* Escenario 2: $k = 0.02$ (Factor Escala "2")
"""

layout = html.Div([
    html.H1("Dinámica de Propagación de Rumores (Derecho Penal I)", 
            style={'textAlign': 'center', 'color': COLOR_TITULO, 'padding': '20px 0'}),

    html.Div([
        html.Div([
            dcc.Graph(figure=fig_k1),
            dcc.Graph(figure=fig_k2)
        ], style={'flex': '2', 'display': 'flex', 'flexDirection': 'column', 'gap': '20px'}),
        
        html.Div([
            html.H3("Definición del Problema", className="title",
                    style={'color': COLOR_SUCEPTIBLES, 'marginTop': '0'}),
            dcc.Markdown(texto_ecuaciones, mathjax=True,
                         style={'color': COLOR_TEXTO_SECUNDARIO}),
            html.Hr(style={'borderColor': COLOR_GRID}),
            dcc.Markdown(texto_parametros, mathjax=True,
                         style={'color': COLOR_TEXTO_SECUNDARIO}),
            html.Div([
                html.P(
                    "Nota: El factor 'k' representa la efectividad de los individuos racionales para convencer a los infectados de que el rumor es falso.", 
                    style={'fontStyle': 'italic', 'fontSize': '0.9em', 'color': '#aaa'}
                )
            ], style={'marginTop': '30px', 'padding': '10px',
                      'border': '1px solid #333', 'borderRadius': '5px'})
        ], style={'flex': '1', 'paddingLeft': '20px', 'display': 'flex',
                  'flexDirection': 'column'})

    ], style={'display': 'flex', 'flex': '1', 'padding': '20px',
              'alignItems': 'flex-start'})

], style={
    'backgroundColor': COLOR_FONDO_PAPEL,
    'minHeight': '100vh',
    'display': 'flex',
    'flexDirection': 'column'
})
