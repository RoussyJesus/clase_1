import dash 
from dash import html, dcc
import plotly.graph_objects as go
import numpy as np
from scipy.integrate import odeint

dash.register_page(__name__, path="/Proyecto/Proyecto", name="Proyecto Modelo SIR")

COLOR_SUCEPTIBLES = '#00CFFF'
COLOR_INFECTADOS = '#FF4136'
COLOR_RECUPERADOS = '#39FF14'
COLOR_TITULO = '#d36bff'
COLOR_TEXTO_SECUNDARIO = '#e0e0e0'
COLOR_FONDO_GRAFICO = '#0c162b'
COLOR_FONDO_PAPEL = '#0a101f'
COLOR_GRID = '#333'
COLOR_ZEROLINE = '#b807ff'

def modelo_sir(y, t, b, g):
    S, I, R = y 
    if S < 0: S = 0
    if I < 0: I = 0
    dS_dt = -b*S*I
    dI_dt = b*S*I - g*I
    dR_dt = g*I
    return [dS_dt, dI_dt, dR_dt]

N_texto = 7138.0
beta = 1.0 / 7138.0
gamma = 0.40
S0 = 7137.0
I0 = 1.0
R0 = 0.0
y0 = [S0, I0, R0]
N = S0 + I0 + R0 
t = np.linspace(0, 40, 400) 

solucion = odeint(modelo_sir, y0, t, args=(beta, gamma))
S, I, R = solucion.T

t_6 = np.linspace(0, 6, 100)
sol_6 = odeint(modelo_sir, y0, t_6, args=(beta, gamma))
I_6 = sol_6.T[1]
valor_I_6 = I_6[-1]

fig = go.Figure()
fig.add_trace(go.Scatter(x=t, y=S, mode='lines', name='Susceptibles S(t)', line=dict(color=COLOR_SUCEPTIBLES, width=2.5)))
fig.add_trace(go.Scatter(x=t, y=I, mode='lines', name='Infectados I(t)', line=dict(color=COLOR_INFECTADOS, width=3), fill='tozeroy', fillcolor='rgba(255, 65, 54, 0.3)'))
fig.add_trace(go.Scatter(x=t, y=R, mode='lines', name='Recuperados R(t)', line=dict(color=COLOR_RECUPERADOS, width=2.5)))

fig.update_layout(
    title=dict(text="<b>Modelo SIR - Universidad de San Marcos</b>", x=0.5, font=dict(size=16, color=COLOR_TITULO)),
    xaxis_title="Tiempo (días)",
    yaxis_title="Número de personas",
    paper_bgcolor=COLOR_FONDO_PAPEL,
    plot_bgcolor=COLOR_FONDO_GRAFICO,
    font=dict(color=COLOR_TEXTO_SECUNDARIO),
    legend=dict(orientation='v', y=0.95, x=0.95, bgcolor='rgba(12, 22, 43, 0.7)', bordercolor=COLOR_ZEROLINE),
    margin=dict(l=40, r=40, t=60, b=60)
)

fig.update_xaxes(showgrid=True, gridcolor=COLOR_GRID, zerolinecolor=COLOR_ZEROLINE, linecolor=COLOR_TEXTO_SECUNDARIO, range=[0, 40])
fig.update_yaxes(showgrid=True, gridcolor=COLOR_GRID, zerolinecolor=COLOR_ZEROLINE, linecolor=COLOR_TEXTO_SECUNDARIO, range=[0, N * 1.01])

texto_intro = r"$$ \frac{dS}{dt} = -\beta S I $$ $$ \frac{dI}{dt} = \beta S I - \gamma I $$ $$ \frac{dR}{dt} = \gamma I $$"
texto_condiciones = f"**Condiciones:** $S_0={S0}, I_0={I0}, R_0={R0}, \\beta=1/7138, \\gamma=0.40$"
texto_pregunta_5 = f"**5. Infectados día 6:** $I(6) \\approx {valor_I_6:.2f}$"

layout = html.Div([
    html.Div([
        html.H2("Proyecto: Modelo SIR (U. de San Marcos)", className="title"),
        dcc.Graph(figure=fig, style={"height": "550px", "width": "100%"}),
    ], className="content-graph"),
    html.Div([
        html.H2("Datos del Modelo", className="title"),
        dcc.Markdown(texto_intro, className="text-content", mathjax=True),
        dcc.Markdown(texto_condiciones, className="text-content", mathjax=True),
        dcc.Markdown(texto_pregunta_5, className="text-content", mathjax=True)
    ], className="content-sidebar")
], className="page-container-grid")
