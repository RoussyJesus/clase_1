import dash
from dash import html, dcc
import plotly.graph_objects as go
import numpy as np

COLOR_DATOS_PRINCIPAL = "#51E751"
COLOR_SECUNDARIO = "#EB358A"
COLOR_TITULO = "#4671FF"
COLOR_TEXTO_SECUNDARIO = '#e0e0e0'
COLOR_FONDO_GRAFICO = '#0c162b'
COLOR_FONDO_PAPEL = '#0a101f'
COLOR_GRID = '#333'

P0 = 100
r = 0.03
t = np.linspace(0, 100, 200)
P = P0 * np.exp(r * t)

trace = go.Scatter(
    x=t,
    y=P,
    mode='lines',
    line=dict(
        color=COLOR_DATOS_PRINCIPAL,
        width=3
    ),
    name='P(t) = P0 * e^(rt)',
    hovertemplate='t: %{x:.2f}<br>P(t): %{y:.2f}<extra></extra>'
)

fig = go.Figure(data=trace)

fig.update_layout(
    title=dict(
        text='<b>Crecimiento Exponencial de la Población</b>',
        font=dict(
            size=20,
            color=COLOR_TITULO
        ),
        x=0.5,
        y=0.93
    ),
    xaxis_title='Tiempo (t)',
    yaxis_title='Población P(t)',
    margin=dict(l=40, r=40, t=50, b=40),
    paper_bgcolor=COLOR_FONDO_PAPEL,
    plot_bgcolor=COLOR_FONDO_GRAFICO,
    font=dict(
        family='Outfit',
        size=11,
        color=COLOR_TEXTO_SECUNDARIO
    ),
    legend=dict(font=dict(color=COLOR_TEXTO_SECUNDARIO), bgcolor='rgba(0,0,0,0)')
)

fig.update_xaxes(
    showgrid=True, gridwidth=1, gridcolor=COLOR_GRID,
    zeroline=True, zerolinewidth=2, zerolinecolor=COLOR_SECUNDARIO,
    showline=True, linecolor=COLOR_TEXTO_SECUNDARIO, linewidth=1, mirror=True,
)
fig.update_yaxes(
    showgrid=True, gridwidth=1, gridcolor=COLOR_GRID,
    zeroline=True, zerolinewidth=2, zerolinecolor=COLOR_SECUNDARIO,
    showline=True, linecolor=COLOR_TEXTO_SECUNDARIO, linewidth=1, mirror=True,
)

dash.register_page(__name__, path='/pagina', name='Página')

layout = html.Div(children=[
    html.Div(children=[
        html.H2("Crecimiento de la población y capacidad de carga", className="title"),
        
        dcc.Markdown("""
        Para modelar el crecimiento de la población mediante una ecuación diferencial, primero 
        tenemos que introducir algunas variables y términos relevantes. La variable $t$
        representará el tiempo. Las unidades de tiempo pueden ser horas, días, semanas, 
        meses o incluso años. La variable $P$
        representará a la población. Como la población varía con el tiempo, utilizamos la notación $P(t)$
        para la población en función del tiempo. Si $P(t)$
        es una función diferenciable, entonces la primera derivada $\\dfrac{dP}{dt}$
        representa la tasa instantánea de cambio de la población en función del tiempo.
        """,
        mathjax=True,
        className="text-content"),

        dcc.Markdown("""
        Un ejemplo de función de crecimiento exponencial es $P(t)=P_0e^{rt}$.
        En esta función, $P(t)$
        representa la población en el momento $t$, $P_0$
        representa la población inicial (población en el tiempo $t=0$),
        y la constante $r>0$
        se denomina tasa de crecimiento. Aquí $P_0=100$ y $r=0.03$.
        """,
        mathjax=True,
        className="text-content")
    ], className="content"),
    
    html.Div(children=[
        html.H2("Gráfica Exponencial P(t)", className="title"),
        dcc.Graph(
            figure=fig,
            style={'height': '400px', 'width': '100%'}
        )
    ], className="content")
], className="page-container")
