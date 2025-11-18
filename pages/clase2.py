import dash
from dash import html, dcc, Input,Output,State,callback
import plotly.graph_objects as go
import numpy as np


dash.register_page(__name__, path='/Pagina1', name='Página 1')




layout = html.Div([
    html.Div([
        html.H2("Parámetros del modelo", className="title"),
        html.Div([
            html.Label("Población inicial P(0):"),
            dcc.Input(id="input-p0", type="number", value=200,className="input-field")
        ], className="input-group"),
        html.Div([
            html.Label("Tasa de crecimiento (r):"),
            dcc.Input(id="input-r", type="number", value=0.04, className="input-field")
        ], className="input-group"),
        html.Div([
            html.Label("Capacidad de Carga (k):"),
            dcc.Input(id="input-k", type="number", value=750, className="input-field")
        ], className="input-group"),
         html.Div([
            html.Label("Tiempo máximo (t):"),
            dcc.Input(id="input-t", type="number", value=100, className="input-field")
        ], className="input-group"),
        html.Button("Generar gráfico", id="btn-generar", className="btn-generar")
    ], className="content left"),
    
    html.Div([
        html.H2("Gráfica", className="title"),
        
        dcc.Graph(
        id='grafica-poblacion',
        style={'height':'350px', 'width':'100%'},
    )
    ], className="content right"),
    
    
], className="page-container")

@callback(
    Output('grafica-poblacion', 'figure'),
    Input('btn-generar','n_clicks'),
    State('input-p0','value'),
    State('input-r','value'),
    State('input-k','value'),
    State('input-t','value'),
    prevent_initial_call=False
)
def actualizar_grafica(n_clicks,P0,r,K,t_max):

    # --- Paleta de Colores "Neón Rosa" (Basada en tu CSS) ---
    COLOR_DATOS_PRINCIPAL = "#E93232"  # Magenta/Púrpura Neón (del botón)
    COLOR_LIMITE = "#37BE49"           # Rosa Neón Acento (del borde)
    COLOR_TITULO = "#2F5FFF"           # Rosa Neón Título (de .title)
    COLOR_TEXTO_SECUNDARIO = '#e0e0e0' # Texto claro (de body)
    COLOR_FONDO_GRAFICO = '#0c162b'    # Fondo de tarjeta oscuro (de .content)
    COLOR_FONDO_PAPEL = '#0a101f'      # Fondo de página oscuro (de body)
    COLOR_GRID = '#333'             # Grid oscuro (como el borde de nav-link)
    COLOR_ZEROLINE = "#F3471C"         # Línea de cero coincide con el acento
    # -----------------------------------------------------

    # Validación de inputs (igual que en Crecimiento_poblacion.py)
    if any(v is None for v in [P0, r, K, t_max]) or K <= 0 or t_max <= 0 or P0 < 0:
        fig_empty = go.Figure()
        fig_empty.update_layout(
            title="Por favor, ingrese valores válidos (K > 0, t_max > 0, P0 >= 0)",
            paper_bgcolor=COLOR_FONDO_PAPEL, # Fondo de error coincide con el tema
            plot_bgcolor=COLOR_FONDO_GRAFICO,
            font=dict(color=COLOR_TEXTO_SECUNDARIO), # Texto de error claro
            xaxis={'visible': False},
            yaxis={'visible': False}
        )
        return fig_empty

    # Usamos 200 puntos para una curva más suave
    t = np.linspace(0, t_max, 200)
    
    # Manejo de casos límite
    if K == 0:
        P = np.full(200, P0)
    else:
        denominador = (K - P0) + P0 * np.exp(r * t)
        if np.any(denominador == 0):
            P = np.zeros(200)
        else:
            numerador = P0 * K * np.exp(r * t)
            P = numerador / denominador

    trace_poblacion=go.Scatter(
        x=t,
        y=P,
        mode='lines', # 'lines' es más limpio que 'lines+markers' con 200 puntos
        name='Población P(t)',
        line=dict(
            color=COLOR_DATOS_PRINCIPAL, # Color Neón
            width=2.5
        ),
        hovertemplate='t: %{x:.2f}<br>P(t):%{y:.2f}<extra></extra>'
        
    )
    
    trace_capacidad= go.Scatter(
        x=[0, t_max],
        y=[K, K],
        mode='lines',
        name='Capacidad de Carga (K)',
        line=dict(
            color=COLOR_LIMITE, # Color Neón
            width=2,
            dash='dash'
        ),
        hovertemplate='K: %{y:.2f}<extra></extra>'
    )
    fig=go.Figure(data=(trace_poblacion, trace_capacidad))
    
    fig.update_layout(
    title=dict(
        text='<b>Modelo Logístico de Crecimiento de la Población</b>',
        font=dict(
            size=20,
            color=COLOR_TITULO # Color Neón
        ),
        x=0.5,
        y=0.95
    ),
    xaxis_title='Tiempo (t)',
    yaxis_title='Población P(t)',
    margin=dict(l=40, r=40, t=70, b=40),
    paper_bgcolor=COLOR_FONDO_PAPEL,  # Color Neón
    plot_bgcolor=COLOR_FONDO_GRAFICO, # Color Neón
    font=dict(
        family='Outfit',
        size=12,
        color=COLOR_TEXTO_SECUNDARIO # Color Neón
    ),
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=1.02,
        bgcolor='rgba(0,0,0,0)',
        font=dict(color=COLOR_TEXTO_SECUNDARIO) # Color Neón
    )
)
    fig.update_xaxes(
        showgrid=True, gridwidth=1, gridcolor=COLOR_GRID, # Color Neón
        zeroline=True, zerolinewidth=2, zerolinecolor=COLOR_ZEROLINE, # Color Neón
        showline=True, linecolor=COLOR_TEXTO_SECUNDARIO, linewidth=1, mirror=True, # Color Neón
        range =[0, t_max]
    )
    
    # Rango Y dinámico
    y_max = max(K, np.max(P)) * 1.1 if len(P) > 0 else K * 1.1
    if y_max == 0: y_max = 10

    fig.update_yaxes(
        showgrid=True, gridwidth=1, gridcolor=COLOR_GRID, # Color Neón
        zeroline=True, zerolinewidth=2, zerolinecolor=COLOR_ZEROLINE, # Color Neón
        showline=True, linecolor=COLOR_TEXTO_SECUNDARIO, linewidth=1, mirror=True, # Color Neón
        range=[0, y_max]
    )
    return fig