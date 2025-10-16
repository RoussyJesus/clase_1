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
        html.Button("Generar gréfico", id="btn-generar", className="btn-generar")
    ], className="content left"),
    
    html.Div([
        html.H2("Grafica", className="title"),
        
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
    t =np.linspace(0, t_max,20)
    P = (P0 * K * np.exp(r * t))/((K -  P0) + P0 * np.exp(r * t))
    trace_poblacion=go.Scatter(
        x=t,
        y=P,
        mode='lines+markers',
        name='Población P(t)',
        line=dict(
            color='black',
            width=2
        ),
        marker=dict(
            size=6,
            color='blue',
            symbol='circle'
        ),
        hovertemplate='t: %{x:.2f}<br>P(t):%{y:.2f}<extra></extra>'
        
    )
    
    trace_capacidad= go.Scatter(
        x=[0, t_max],
        y=[K, K],
        mode='lines',
        name='Capacidad de Carga (K)',
        line=dict(
            color='red',
            width=2,
            dash='dash'
        ),
        hovertemplate='K: %{y:.2f}<extra></extra>'
    )
    fig=go.Figure(data=(trace_poblacion, trace_capacidad))
    
    fig.update_layout(
    title=dict(
        text='<b>Modelo Logistico de Crecimiento de la población</b>',
        font=dict(
            size=20,
            color='green'
        ),
        x=0.5,
        y=0.95
    ),
    xaxis_title='Tiempo (t)',
    yaxis_title='Población P(t)',
    margin=dict(l=40, r=40, t=70, b=40),
    paper_bgcolor='lightblue',
    plot_bgcolor='white',
    font=dict(
        family='Outfit',
        size=11,
        color='black'
    ),
    legend=dict(
    orientation='h',
    yanchor='bottom',
    y=1.02
    )
)
    fig.update_xaxes(
    showgrid=True, gridwidth=1, gridcolor='lightpink',
    zeroline=True, zerolinewidth=2, zerolinecolor='red',
    showline=True, linecolor='black', linewidth=2, mirror=True,
    range =[0, t_max]
    )
    fig.update_yaxes(
        showgrid=True, gridwidth=1, gridcolor='lightpink',
        zeroline=True, zerolinewidth=2, zerolinecolor='red',
        showline=True, linecolor='black', linewidth=2, mirror=True,
        range=[0, K + K*0.1]
    )
    return fig