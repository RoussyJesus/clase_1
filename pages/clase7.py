import dash 
from dash import html, dcc, callback, Input, Output, State
import numpy as np
import plotly.graph_objects as go
from scipy.integrate import odeint

dash.register_page(__name__, path="/SIR", name="Modelo SIR")


COLOR_SUCEPTIBLES = '#00CFFF' 
COLOR_INFECTADOS = '#FF007F'  
COLOR_RECUPERADOS = '#b807ff' 
COLOR_TITULO = '#d36bff'          
COLOR_TEXTO_SECUNDARIO = '#e0e0e0' 
COLOR_FONDO_GRAFICO = '#0c162b'    
COLOR_FONDO_PAPEL = '#0a101f'      
COLOR_GRID = '#333'            
COLOR_ZEROLINE = '#b807ff'        

def modelo_sir(y, t, b, g, N):
    S,I,R = y 
    

    if S < 0: S = 0
    if I < 0: I = 0
        
    dS_dt = -b*S*I/N
    dI_dt = b*S*I/N-g*I
    dR_dt = g*I

    return [dS_dt, dI_dt, dR_dt]


layout = html.Div([
    
    html.Div([
        html.H2("Modelo SIR - Epidemiología", className="title"),
        
     
        html.Div([
            html.Label("Población Total (N) = "),
            dcc.Input(id="input-n-sir", type = "number", value = 1000, className="input-field")
        ], className="input-group"),
        html.Div([
            html.Label("Tasa de transmisión (β) = "),
            dcc.Input(id="input-b-sir", type = "number", value = 0.3, step=0.01, className="input-field")
        ], className="input-group"),
        html.Div([
            html.Label("Tasa de recuperación (γ) = "),
            dcc.Input(id="input-g-sir", type = "number", value = 0.1, step=0.01, className="input-field")
        ], className="input-group"),
        html.Div([
            html.Label("Infectados iniciales (I₀)= "),
            dcc.Input(id="input-I0-sir", type = "number", value = 1, className="input-field")
        ], className="input-group"),
        html.Div([
            html.Label("Tiempo de simulación (días): "),
            dcc.Input(id="input-tiempo-sir", type = "number", value = 100, className="input-field")
        ], className="input-group"),
        
        
        html.Button("Generar Simulación", id = "btn-generar-sir", className="btn-generar"),

    ], className="content"), 
    
    html.Div([
        html.H2("Evolución de la Epidemia", className="title"),
        dcc.Graph(id="grafica-sir", style={"height":"450px","width":"100%"}),
    ], className="content")

], className="page-container")



@callback(
    Output("grafica-sir", "figure"),
    Input("btn-generar-sir", "n_clicks"),
    State("input-n-sir", "value"),
    State("input-b-sir", "value"),
    State("input-g-sir", "value"),
    State("input-I0-sir", "value"),
    State("input-tiempo-sir", "value"),
    prevent_initial_call=False
)
def simular_sir(n_clicks, n, beta, gamma, I0, tiempo_max):
    
    
    if n is None or beta is None or gamma is None or I0 is None or tiempo_max is None:
        n, beta, gamma, I0, tiempo_max = 1000, 0.3, 0.1, 1, 100
    if n <= 0: n = 1000
    if I0 <= 0: I0 = 1
    if tiempo_max <= 0: tiempo_max = 100
        
    S0 = n - I0 
    R0_inicial = 0
    y0 = [S0, I0, R0_inicial]
    t = np.linspace(0, tiempo_max, 200) 
    
    try:
        solucion = odeint(modelo_sir, y0, t, args=(beta, gamma, n))
        S, I, R = solucion.T
    except Exception as e:
        
        fig_error = go.Figure()
        fig_error.update_layout(
            title=f"Error en la simulación: {str(e)}",
            paper_bgcolor=COLOR_FONDO_PAPEL,
            plot_bgcolor=COLOR_FONDO_GRAFICO,
            font=dict(color=COLOR_TEXTO_SECUNDARIO),
            xaxis={'visible': False},
            yaxis={'visible': False}
        )
        return fig_error

    
    fig = go.Figure()

    
    fig.add_trace(go.Scatter(
        x=t, y=S,
        mode = 'lines',
        name = 'Susceptibles (S)',
        line = dict(color=COLOR_SUCEPTIBLES, width=2.5),
        hovertemplate = "Día: %{x:.0f} <br> Susceptibles :%{y:.0f}<extra></extra>"
    ))
    fig.add_trace(go.Scatter(
        x=t, y=I,
        mode = 'lines',
        name='Infectados (I)',
        line = dict(color=COLOR_INFECTADOS, width=3),
        fill='tozeroy',
        fillcolor='rgba(255, 0, 127, 0.3)', 
        hovertemplate = "Día: %{x:.0f} <br> Infectados :%{y:.0f}<extra></extra>"
    ))
    fig.add_trace(go.Scatter(
        x=t, y=R,
        mode = 'lines',
        name='Recuperados (R)',
        line = dict(color=COLOR_RECUPERADOS, width=2.5),
        hovertemplate = "Día: %{x:.0f} <br> Recuperados :%{y:.0f}<extra></extra>"
    ))

   
    fig.update_layout(
        title=dict(
            text = f"<b>Evolución del Modelo SIR (R₀ ≈ {beta/gamma:.2f})</b>",
            x=0.5, font=dict(size=16, color=COLOR_TITULO)
        ),
        xaxis_title = "Tiempo (días)",
        yaxis_title="Número de personas",
        paper_bgcolor=COLOR_FONDO_PAPEL,
        plot_bgcolor=COLOR_FONDO_GRAFICO,
        font=dict(color=COLOR_TEXTO_SECUNDARIO),
        legend=dict(
            orientation='h', yanchor='bottom',y=1.02,
            xanchor='center', x=.5,
            bgcolor='rgba(0,0,0,0)',
            font=dict(color=COLOR_TEXTO_SECUNDARIO)
        )
    )
    fig.update_xaxes(
        showgrid=True, gridwidth=1, gridcolor = COLOR_GRID,
        zeroline=True, zerolinewidth=2, zerolinecolor=COLOR_ZEROLINE,
        showline=True, linecolor=COLOR_TEXTO_SECUNDARIO, linewidth=1, mirror=True,
    )
    fig.update_yaxes(
        showgrid=True, gridwidth=1, gridcolor = COLOR_GRID,
        zeroline=True, zerolinewidth=2, zerolinecolor=COLOR_ZEROLINE,
        showline=True, linecolor=COLOR_TEXTO_SECUNDARIO, linewidth=1, mirror=True,
    )

    return fig