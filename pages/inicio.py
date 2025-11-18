import dash
from dash import html, dcc, Input,Output,State,callback
import plotly.graph_objects as go
import numpy as np


dash.register_page(__name__, path='/inicio', name='Inicio')

# --- Paleta de Colores "Neón Rosa" (Basada en tu CSS) ---
COLOR_DATOS_PRINCIPAL = "#AC00E0"  # Magenta/Púrpura Neón
COLOR_SECUNDARIO = "#0CE7C3"       # Rosa Neón Acento
COLOR_TITULO = "#0D59E6"           # Rosa Neón Título
COLOR_TEXTO_SECUNDARIO = '#e0e0e0' # Texto claro
COLOR_FONDO_GRAFICO = '#0c162b'    # Fondo de tarjeta oscuro
COLOR_FONDO_PAPEL = "#020711"      # Fondo de página oscuro
COLOR_GRID = '#333'             # Grid oscuro
# -----------------------------------------------------

# --- Gráficos se crearán dinámicamente en el callback ---

layout = html.Div([
 
    # Títulos con clases de CSS, sin estilos en línea
    html.H1(" ¡Bienvenido al Curso de Técnicas de Modelamiento Matemático!",
            className="welcome-title"),

    
    html.H3("Soy Roussy Jesús Aguilar. En esta página de bienvenida, exploraremos cómo conectar las matemáticas con el mundo real a través de ejemplos dinámicos.",
            className="welcome-subtitle"), # Texto actualizado

    
    # Contenedor 1: Imagen y Lista (dentro de una tarjeta .content)
    html.Div([
        html.Div([
            html.Img(
                src="assets/imagenes/imagen1.jpg",
                className="intro-image"
            ),
            html.Div([
                html.H2("¿Qué aprenderás en este curso?", className="title"), # Reutilizamos la clase .title
                html.Ul([
                    html.Li("Modelar fenómenos reales mediante ecuaciones diferenciales."),
                    html.Li("Interpretar el comportamiento de sistemas dinámicos."),
                    html.Li("Aplicar técnicas de optimización y simulación."),
                    html.Li("Usar herramientas gráficas para visualizar resultados."),
                    html.Li("Desarrollar pensamiento analítico y crítico a través de la matemática aplicada."),
                ])
            ], className="intro-list")
        ], className="intro-container")
    ], className="content"), # Usamos la clase .content para el fondo oscuro y borde neón

    
    # Contenedor 2: Fundamentos Y GRÁFICO 3D (dentro de una tarjeta .content)
    html.Div([
        html.Div([
            html.Div([
                # --- TÍTULO ACTUALIZADO con nueva clase de animación ---
                html.H2("¿Para qué sirve un Modelo Matemático?", className="title section-title-animated"),
                
                # --- PÁRRAFO CON OBJETIVO DETALLADO ---
                html.P(
                    className="intro-text" # Esta clase ahora será animada por CSS
                ),
                
                # --- LISTA ACTUALIZADA con nueva clase de animación ---
                html.Ul([
                    html.Li("Predicción: Anticipar el futuro, desde el clima hasta epidemias o mercados financieros."),
                    html.Li("Optimización: Encontrar la mejor solución posible, como rutas de logística o carteras de inversión."),
                    html.Li("Comprensión: Simular sistemas complejos (física, biología, economía) para entender cómo funcionan."),
                    html.Li("Control: Diseñar y automatizar sistemas, como el piloto automático de un avión o un robot."),
                ], className="intro-list-animated") # Clase añadida para animar los 'li'
            ], className="intro-list"),
            
            # --- GRÁFICO 3D MOVIDO AQUÍ ---
            html.Div([
                dcc.Graph(id='spiral-graph', style={'height': '400px', 'width': '100%'})
            ], className="intro-graph-item") # Nueva clase CSS

        ], className="intro-container")
    ], className="content"),

    
    # Contenedor 3: Gráficos 2D (dentro de una tarjeta .content)
    html.Div([
        html.H3("Visualización Dinámica de Funciones", 
                className="graph-title"), # Título actualizado
        
        # --- LAYOUT DE GRÁFICOS ACTUALIZADO (2 MEDIOS) ---
        html.Div([
            # Gráfico 1: Mitad
            html.Div([
                dcc.Graph(id='sine-cosine-graph', style={'height': '400px', 'width': '100%'})
            ], className="graph-item-half"),
            
            # Gráfico 2: Mitad
            html.Div([
                dcc.Graph(id='lissajous-graph', style={'height': '400px', 'width': '100%'})
            ], className="graph-item-half"),
            
        ], className="graph-container"),

        dcc.Interval(
            id='animation-interval',
            interval=50,  # Actualiza cada 50 milisegundos para una animación fluida
            n_intervals=0
        )
    ], className="content"), # Usamos la clase .content de nuevo

 
    # Contenedor 4: Texto de Cierre (dentro de una tarjeta .content)
    html.Div([
        html.H3("La matemática es el lenguaje con el que comprendemos el universo.",
                className="closing-title"), # Clase nueva
        html.P("En este curso aprenderás a usarla para modelar, analizar y predecir fenómenos reales, "
               "de una forma práctica y visual. ",
               className="closing-text") # Clase nueva
    ], className="content")
    
], className="page-container") # Usamos la clase .page-container existente


# --- Callback para TRES gráficos animados ---
@callback(
    Output('sine-cosine-graph', 'figure'),
    Output('lissajous-graph', 'figure'),
    Output('spiral-graph', 'figure'), # Salida del gráfico 3D
    Input('animation-interval', 'n_intervals')
)
def update_graphs(n_intervals):
    
    # --- Gráfico 1: Seno/Coseno ---
    x_sine = np.linspace(0, 4*np.pi, 200) 
    step_sine = n_intervals * 0.05
    
    y1 = np.sin(x_sine - step_sine)
    y2 = np.cos(x_sine - step_sine)

    fig_sine = go.Figure()
    fig_sine.add_trace(go.Scatter(
        x=x_sine, y=y1, mode='lines', name='Seno', 
        line=dict(color=COLOR_DATOS_PRINCIPAL, width=3)
    ))
    fig_sine.add_trace(go.Scatter(
        x=x_sine, y=y2, mode='lines', name='Coseno', 
        line=dict(color=COLOR_SECUNDARIO, width=3, dash='dot')
    ))

    fig_sine.update_layout(
        title=dict(text="<b>Ondas (Seno/Coseno)</b>", x=0.5, font=dict(size=18, color=COLOR_TITULO)),
        xaxis_title='x',
        yaxis_title='f(x)',
        plot_bgcolor=COLOR_FONDO_GRAFICO,
        paper_bgcolor=COLOR_FONDO_GRAFICO,
        font=dict(family='Outfit', size=12, color=COLOR_TEXTO_SECUNDARIO),
        legend=dict(x=0.05, y=1, font=dict(color=COLOR_TEXTO_SECUNDARIO), bgcolor='rgba(0,0,0,0)'),
        margin=dict(l=40, r=40, t=60, b=40),
        xaxis=dict(gridcolor=COLOR_GRID, linecolor=COLOR_TEXTO_SECUNDARIO, zerolinecolor=COLOR_SECUNDARIO, range=[0, 4*np.pi]),
        yaxis=dict(gridcolor=COLOR_GRID, linecolor=COLOR_TEXTO_SECUNDARIO, zerolinecolor=COLOR_SECUNDARIO, range=[-1.1, 1.1])
    )

    # --- Gráfico 2: Curva de Lissajous ---
    t = np.linspace(0, 2 * np.pi, 300)
    step_lissajous = n_intervals * 0.02
    
    a = 3  # Frecuencia X
    b = 2  # Frecuencia Y
    delta = step_lissajous # Fase animada
    
    x_lissajous = np.sin(a * t + delta)
    y_lissajous = np.sin(b * t)
    
    fig_lissajous = go.Figure()
    fig_lissajous.add_trace(go.Scatter(
        x=x_lissajous, y=y_lissajous, mode='lines', name='Lissajous',
        line=dict(color=COLOR_SECUNDARIO, width=3) # Color secundario para variar
    ))

    fig_lissajous.update_layout(
        title=dict(text="<b>Curva de Lissajous (a=3, b=2)</b>", x=0.5, font=dict(size=18, color=COLOR_TITULO)),
        xaxis_title='sin(3t + δ)',
        yaxis_title='sin(2t)',
        plot_bgcolor=COLOR_FONDO_GRAFICO,
        paper_bgcolor=COLOR_FONDO_GRAFICO,
        font=dict(family='Outfit', size=12, color=COLOR_TEXTO_SECUNDARIO),
        legend=dict(x=0.05, y=1, font=dict(color=COLOR_TEXTO_SECUNDARIO), bgcolor='rgba(0,0,0,0)'),
        margin=dict(l=40, r=40, t=60, b=40),
        xaxis=dict(gridcolor=COLOR_GRID, linecolor=COLOR_TEXTO_SECUNDARIO, zerolinecolor=COLOR_SECUNDARIO, range=[-1.1, 1.1]),
        yaxis=dict(gridcolor=COLOR_GRID, linecolor=COLOR_TEXTO_SECUNDARIO, zerolinecolor=COLOR_SECUNDARIO, range=[-1.1, 1.1])
    )
    
    # --- Gráfico 3: Espiral 3D ---
    t_spiral = np.linspace(-4 * np.pi, 4 * np.pi, 250)
    step_spiral = n_intervals * 0.03
    
    x_spiral = t_spiral * np.cos(t_spiral + step_spiral)
    y_spiral = t_spiral * np.sin(t_spiral + step_spiral)
    z_spiral = t_spiral / 2  # Crea el efecto de "cono"
    
    fig_spiral = go.Figure()
    fig_spiral.add_trace(go.Scatter3d(
        x=x_spiral, y=y_spiral, z=z_spiral,
        mode='lines',
        name='Espiral',
        line=dict(color=COLOR_DATOS_PRINCIPAL, width=4),
        marker=dict(size=0) # Sin marcadores
    ))
    fig_spiral.update_layout(
        title=dict(text="<b>Espiral Paramétrica 3D</b>", x=0.5, font=dict(size=18, color=COLOR_TITULO)),
        scene=dict(
            bgcolor=COLOR_FONDO_GRAFICO,
            xaxis=dict(title='X', showgrid=True, gridcolor=COLOR_GRID, backgroundcolor=COLOR_FONDO_PAPEL, linecolor=COLOR_TEXTO_SECUNDARIO, zerolinecolor=COLOR_SECUNDARIO, range=[-40, 40]),
            yaxis=dict(title='Y', showgrid=True, gridcolor=COLOR_GRID, backgroundcolor=COLOR_FONDO_PAPEL, linecolor=COLOR_TEXTO_SECUNDARIO, zerolinecolor=COLOR_SECUNDARIO, range=[-40, 40]),
            zaxis=dict(title='Z', showgrid=True, gridcolor=COLOR_GRID, backgroundcolor=COLOR_FONDO_PAPEL, linecolor=COLOR_TEXTO_SECUNDARIO, zerolinecolor=COLOR_SECUNDARIO, range=[-20, 20]),
        ),
        paper_bgcolor=COLOR_FONDO_GRAFICO,
        font=dict(family='Outfit', size=12, color=COLOR_TEXTO_SECUNDARIO),
        margin=dict(l=20, r=20, t=60, b=20)
    )

    return fig_sine, fig_lissajous, fig_spiral