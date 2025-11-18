import dash
from dash import html, dcc
import plotly.graph_objects as go
import numpy as np

# --- Paleta de Colores "Neón Rosa" (Basada en tu CSS) ---
COLOR_DATOS_PRINCIPAL = "#EB5F02"  # Magenta/Púrpura Neón
COLOR_SECUNDARIO = "#00FF2A"       # Rosa Neón Acento
COLOR_TITULO = "#397EFF"           # Rosa Neón Título
COLOR_TEXTO_SECUNDARIO = '#e0e0e0' # Texto claro
COLOR_FONDO_GRAFICO = '#0c162b'    # Fondo de tarjeta oscuro
COLOR_FONDO_PAPEL = '#0a101f'      # Fondo de página oscuro
COLOR_GRID = '#333'             # Grid oscuro
# -----------------------------------------------------

# --- Definición del Gráfico ---

P0 = 10
r = 0.2
K = 150
t = np.linspace(0, 60, 300)  # tiempo

A = (K - P0) / P0
P = K / (1 + A * np.exp(-r * t))

# --- Trazas del Gráfico ---
trace_logistica = go.Scatter(
    x=t,
    y=P,
    mode='lines',
    line=dict(color=COLOR_DATOS_PRINCIPAL, width=2.5), # MEJORA: Color Neón
    name='Ecuación Logística',
    hovertemplate='t: %{x:.2f}<br>P(t):%{y:.2f}<extra></extra>'
)

trace_capacidad = go.Scatter(
    x=t,
    y=[K]*len(t),
    mode='lines',
    line=dict(color=COLOR_SECUNDARIO, width=2, dash='dash'), # MEJORA: Color Neón
    name='Capacidad de carga',
    hovertemplate='K: %{y:.2f}<extra></extra>'
)

fig = go.Figure(data=[trace_logistica, trace_capacidad])

# --- Estilo del Gráfico ---
fig.update_layout(
    title=dict(
        text='<b>Modelo Logístico de Crecimiento Poblacional</b>', # Título actualizado
        font=dict(size=18, color=COLOR_TITULO), # MEJORA: Color Neón
        x=0.5
    ),
    xaxis_title='Tiempo (t)',
    yaxis_title='Población (P)',
    paper_bgcolor=COLOR_FONDO_PAPEL,   # MEJORA: Color Neón
    plot_bgcolor=COLOR_FONDO_GRAFICO, # MEJORA: Color Neón
    font=dict(family='Outfit', size=12, color=COLOR_TEXTO_SECUNDARIO), # MEJORA: Color Neón
    margin=dict(l=40, r=40, t=60, b=40),
    legend=dict(
        x=0.02, y=0.95,
        bgcolor='rgba(0,0,0,0)', # MEJORA: Fondo transparente
        font=dict(color=COLOR_TEXTO_SECUNDARIO) # MEJORA: Color Neón
    )
)

fig.update_xaxes(
    showgrid=True, gridwidth=1, gridcolor=COLOR_GRID, # MEJORA: Color Neón
    zeroline=True, zerolinewidth=2, zerolinecolor=COLOR_SECUNDARIO, # MEJORA: Color Neón
    linecolor=COLOR_TEXTO_SECUNDARIO, linewidth=1 # MEJORA: Color Neón
)

fig.update_yaxes(
    showgrid=True, gridwidth=1, gridcolor=COLOR_GRID, # MEJORA: Color Neón
    zeroline=True, zerolinewidth=2, zerolinecolor=COLOR_SECUNDARIO, # MEJORA: Color Neón
    linecolor=COLOR_TEXTO_SECUNDARIO, linewidth=1 # MEJORA: Color Neón
)

# --- Registro de la Página ---
dash.register_page(__name__, path='/Tarea', name='Tarea')

# --- Layout de la Página (REDISTRIBUIDO) ---
layout = html.Div(children=[
    
    # MEJORA: Tarjeta 1 - Explicación
    html.Div(children=[
        html.H2("Modelo Logístico de Crecimiento Poblacional", className="title"),
        
        dcc.Markdown("""
        La ecuación logística describe cómo una población crece rápidamente al inicio,
        pero su crecimiento se desacelera a medida que se aproxima a la **capacidad de carga (K)**.
        La forma general es:
        
        $$
        P(t) = \\frac{K}{1 + A e^{-r t}}
        $$
        
        donde:
        - $P_0$: población inicial  
        - $r$: tasa de crecimiento  
        - $K$: capacidad de carga  
        """, 
        mathjax=True,
        className="text-content" # MEJORA: Aplicar clase para estilo neón
        )
    ], className="content"), # Se elimina .left, se usa .content
    
    # MEJORA: Tarjeta 2 - Gráfico
    html.Div(children=[
        html.H2("Gráfica del Modelo Logístico", className="title"),
        dcc.Graph(
            figure=fig,
            style={'height': '400px', 'width': '100%'}
        )
    ], className="content") # Se elimina .right, se usa .content

], className="page-container")