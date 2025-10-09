import dash
from dash import html, dcc
import plotly.graph_objects as go
import numpy as np


dash.register_page(__name__, path='/inicio', name='Inicio')


x = np.linspace(0, 2*np.pi, 100)
y1 = np.sin(x)
y2 = np.cos(x)

fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=y1, mode='lines', name='Seno', line=dict(color='royalblue', width=3)))
fig.add_trace(go.Scatter(x=x, y=y2, mode='lines', name='Coseno', line=dict(color='crimson', width=3, dash='dot')))

fig.update_layout(
    title=dict(text="<b>Funciones Seno y Coseno</b>", x=0.5, font=dict(size=18, color='darkblue')),
    xaxis_title='x',
    yaxis_title='f(x)',
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family='Outfit', size=12),
    legend=dict(x=0.8, y=1),
    margin=dict(l=40, r=40, t=60, b=40)
)


layout = html.Div([
  
    html.H1(" ¡Bienvenido al Curso de Técnicas de Modelamiento Matemático!",
            style={'textAlign': 'center', 'color': '#0020aa', 'marginTop': '20px'}),

   
    html.H3("Soy Roussy Jesús Aguilar y aquí aprenderemos a conectar las matemáticas con el mundo real.",
            style={
                'textAlign': 'center',
                'color': 'gray',
                'fontStyle': 'italic',
                'marginTop': '5px',
                'marginBottom': '25px'
            }),

    
    html.Div([
        html.Img(
            src="assets/imagenes/imagen1.jpg",
            style={
                'width': '35%',
                'borderRadius': '12px',
                'boxShadow': '0 0 15px rgba(0,0,0,0.25)',
                'transition': 'transform 0.3s',
            }
        ),
        html.Div([
            html.H2(" ¿Qué aprenderás en este curso?", style={'color': '#0020aa', 'marginBottom': '10px'}),
            html.Ul([
                html.Li("Modelar fenómenos reales mediante ecuaciones diferenciales."),
                html.Li("Interpretar el comportamiento de sistemas dinámicos."),
                html.Li("Aplicar técnicas de optimización y simulación."),
                html.Li("Usar herramientas gráficas para visualizar resultados."),
                html.Li("Desarrollar pensamiento analítico y crítico a través de la matemática aplicada."),
            ], style={'textAlign': 'left', 'fontSize': '18px', 'lineHeight': '1.6'})
        ], style={'width': '55%', 'padding': '20px'})
    ], style={
        'display': 'flex',
        'justifyContent': 'center',
        'alignItems': 'center',
        'gap': '25px',
        'marginTop': '30px',
        'flexWrap': 'wrap'
    }),

   
    html.Div([
        html.H3(" Visualización de funciones matemáticas:", 
                style={'textAlign': 'center', 'color': '#0040ff', 'marginBottom': '10px'}),
        dcc.Graph(figure=fig, style={'height': '400px', 'width': '85%', 'margin': 'auto'})
    ], style={'marginTop': '40px'}),

  
    html.Div([
        
        html.H3(" La matemática es el lenguaje con el que comprendemos el universo.",
                style={'color': '#0020aa', 'marginBottom': '10px'}),
        html.P("En este curso aprenderás a usarla para modelar, analizar y predecir fenómenos reales, "
               "de una forma práctica y visual. ",
               style={'fontSize': '18px', 'textAlign': 'center', 'maxWidth': '750px', 'margin': 'auto'})
    ], style={
        'textAlign': 'center',
        'marginTop': '50px',
        'marginBottom': '60px'
    })
])
