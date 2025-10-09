import dash
from dash import html, dcc
import plotly.graph_objects as go
import numpy as np


P0 = 10        
r = 0.2        
K = 150        
t = np.linspace(0, 60, 300)  # tiempo


A = (K - P0) / P0
P = K / (1 + A * np.exp(-r * t))


trace_logistica = go.Scatter(
    x=t,
    y=P,
    mode='lines',
    line=dict(color='blue', width=2),
    name='Ecuación Logística'
)


trace_capacidad = go.Scatter(
    x=t,
    y=[K]*len(t),
    mode='lines',
    line=dict(color='red', width=3, dash='dash'),
    name='Capacidad de carga'
)


fig = go.Figure(data=[trace_logistica, trace_capacidad])

fig.update_layout(
    title=dict(
        text='<b>Campo de vectores de dP/dt = rP(1 - P/k)</b>',
        font=dict(size=18, color='darkblue'),
        x=0.5
    ),
    xaxis_title='Tiempo (t)',
    yaxis_title='Población (P)',
    paper_bgcolor='white',
    plot_bgcolor='white',
    font=dict(family='Outfit', size=12, color='black'),
    margin=dict(l=40, r=40, t=60, b=40),
    legend=dict(
        x=0.02, y=0.95,
        bgcolor='rgba(255,255,255,0.7)',
        bordercolor='black',
        borderwidth=1
    )
)


fig.update_xaxes(
    showgrid=True,
    gridwidth=1,
    gridcolor='lightgray',
    zeroline=True,
    zerolinewidth=2,
    zerolinecolor='green',
    linecolor='green',
    linewidth=2
)

fig.update_yaxes(
    showgrid=True,
    gridwidth=1,
    gridcolor='lightgray',
    zeroline=True,
    zerolinewidth=2,
    zerolinecolor='green',
    linecolor='green',
    linewidth=2
)

dash.register_page(__name__, path='/Tarea', name='Tarea')

layout = html.Div(children=[
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
        """, mathjax=True)
    ], className="content left"),
    
    html.Div(children=[
        html.H2("Gráfica del Modelo Logístico", className="title"),
        dcc.Graph(
            figure=fig,
            style={'height': '400px', 'width': '100%'}
        )
    ], className="content right")
], className="page-container")
