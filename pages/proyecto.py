import dash 
from dash import html, dcc
import plotly.graph_objects as go
import numpy as np
from scipy.integrate import odeint

# 1. REGISTRO DE LA NUEVA PÁGINA
dash.register_page(__name__, path="/proyecto", name="Proyecto")

# --- Paleta de Colores (Neón) basada en tu imagen (Azul, Rojo, Verde) ---
COLOR_SUCEPTIBLES = '#00CFFF' # Azul Eléctrico
COLOR_INFECTADOS = '#FF4136'  # Rojo Neón
COLOR_RECUPERADOS = '#39FF14' # Verde Neón
COLOR_TITULO = '#d36bff'           # Púrpura Claro (del tema)
COLOR_TEXTO_SECUNDARIO = '#e0e0e0' # Texto claro
COLOR_FONDO_GRAFICO = '#0c162b'    # Fondo de tarjeta oscuro
COLOR_FONDO_PAPEL = '#0a101f'      # Fondo de página oscuro
COLOR_GRID = '#333'             # Grid oscuro
COLOR_ZEROLINE = '#b807ff'         # Púrpura (del tema)
# -----------------------------------------------------

# --- Definición del Modelo (BASADO EN EL CÓDIGO DE LA IMAGEN) ---
# El modelo de la imagen es dS/dt = -b*S*I (no -b*S*I/N)
def modelo_sir(y, t, b, g):
    S,I,R = y 
    if S < 0: S = 0
    if I < 0: I = 0
    
    # Modelo Mass Action (como en la imagen)
    dS_dt = -b*S*I
    dI_dt = b*S*I - g*I
    dR_dt = g*I
    
    return [dS_dt, dI_dt, dR_dt]

# --- Generación de Datos del Gráfico (BASADO EN EL CÓDIGO DE LA IMAGEN) ---
# Parámetros EXACTOS de las imágenes
N_texto = 7138.0
beta = 1.0 / 7138.0
gamma = 0.40

# --- CORRECCIÓN CLAVE ---
# El código de la imagen usa I0=10 (en y0=[SO, 10, RO]), no 1.
S0 = 7137.0
I0 = 1.0 # <-- Este es el valor del código de la simulación
R0 = 0.0
y0 = [S0, I0, R0]
N = S0 + I0 + R0 # N real es 7147

# Simular por 40 días
t = np.linspace(0, 40, 400) 

solucion = odeint(modelo_sir, y0, t, args=(beta, gamma))
S, I, R = solucion.T

# --- Cálculo de I(6) para verificar ---
t_6 = np.linspace(0, 6, 100)
sol_6 = odeint(modelo_sir, y0, t_6, args=(beta, gamma))
I_6 = sol_6.T[1]
valor_I_6 = I_6[-1] # Esto dará ≈ 36.12

# --- Creación de la Figura ---
fig = go.Figure()

# --- Trazas con Colores (Azul, Rojo, Verde) ---
fig.add_trace(go.Scatter(
    x=t, y=S, mode = 'lines', name = 'Susceptibles S(t)',
    line = dict(color=COLOR_SUCEPTIBLES, width=2.5),
    hovertemplate = "Día: %{x:.0f} <br> Susceptibles :%{y:.0f}<extra></extra>"
))
fig.add_trace(go.Scatter(
    x=t, y=I, mode = 'lines', name='Infectados I(t)',
    line = dict(color=COLOR_INFECTADOS, width=3), # Rojo
    fill='tozeroy',
    fillcolor='rgba(255, 65, 54, 0.3)', # Relleno Rojo
    hovertemplate = "Día: %{x:.0f} <br> Infectados :%{y:.0f}<extra></extra>"
))
fig.add_trace(go.Scatter(
    x=t, y=R, mode = 'lines', name='Recuperados R(t)',
    line = dict(color=COLOR_RECUPERADOS, width=2.5), # Verde
    hovertemplate = "Día: %{x:.0f} <br> Recuperados :%{y:.0f}<extra></extra>"
))

# --- Layout con Tema Oscuro ---
fig.update_layout(
    title=dict(
        text = "<b>Modelo SIR - Universidad de San Marcos</b>",
        x=0.5, font=dict(size=16, color=COLOR_TITULO)
    ),
    xaxis_title = "Tiempo (días)",
    yaxis_title="Número de personas",
    paper_bgcolor=COLOR_FONDO_PAPEL,
    plot_bgcolor=COLOR_FONDO_GRAFICO,
    font=dict(color=COLOR_TEXTO_SECUNDARIO),
    legend=dict(
        orientation='v', yanchor='top',y=0.95,
        xanchor='right', x=0.95,
        bgcolor='rgba(12, 22, 43, 0.7)', # Fondo de leyenda semi-transparente
        bordercolor=COLOR_ZEROLINE,
        borderwidth=1,
        font=dict(color=COLOR_TEXTO_SECUNDARIO)
    ),
    # MEJORA: Aumentamos el margen inferior para que no se corte
    margin=dict(l=40, r=40, t=60, b=60) 
)
fig.update_xaxes(
    showgrid=True, gridwidth=1, gridcolor = COLOR_GRID,
    zeroline=True, zerolinewidth=2, zerolinecolor=COLOR_ZEROLINE,
    showline=True, linecolor=COLOR_TEXTO_SECUNDARIO, linewidth=1, mirror=True,
    range=[0, 40]
)
fig.update_yaxes(
    showgrid=True, gridwidth=1, gridcolor = COLOR_GRID,
    zeroline=True, zerolinewidth=2, zerolinecolor=COLOR_ZEROLINE,
    showline=True, linecolor=COLOR_TEXTO_SECUNDARIO, linewidth=1, mirror=True,
    range=[0, N * 1.01] # Rango Y basado en N
)

# --- Texto de la Imagen (INTRO) ---
texto_intro = """
**Sistema de Ecuaciones Diferenciales:**

$$
\\frac{dS}{dt} = -\\beta S I
$$
$$
\\frac{dI}{dt} = \\beta S I - \gamma I
$$
$$
\\frac{dR}{dt} = \gamma I
$$
"""

# --- Texto de la Imagen (Condiciones) CORREGIDO ---
texto_condiciones = f"""
**Condiciones Iniciales y Parámetros:**

* $S(0) = S_0 = {S0}$
* $I(0) = I_0 = {I0}$
* $R(0) = R_0 = {R0}$
* $N(t) = S(t) + I(t) + R(t) = {N}$
* $\\beta = 1/7138$
* $\gamma = 0.40$
"""

# --- Texto de la Imagen (Pregunta 5) ---
texto_pregunta_5 = f"""
**5. ¿Cuántas personas están infectadas al día 6?**

Usando la simulación numérica (odeint) con $I_0 = 1$, se encuentra que:

$I(6) \approx {valor_I_6:.2f}$
"""

# --- Layout de la Página (NUEVA DISTRIBUCIÓN) ---
layout = html.Div([
    
    # Contenedor 1: Gráfico Grande
    html.Div([
        html.H2("Proyecto: Modelo SIR (U. de San Marcos)", className="title"),
        dcc.Graph(
            figure=fig, 
            # MEJORA: Gráfico más alto
            style={"height":"550px","width":"100%"}
        ), 
    ], className="content-graph"), # Clase para el gráfico (70%)
    
    # Contenedor 2: Barra Lateral de Datos
    html.Div([
        html.H2("Datos del Modelo", className="title"),
        dcc.Markdown(texto_intro, className="text-content", mathjax=True),
        dcc.Markdown(texto_condiciones, className="text-content", mathjax=True),
        dcc.Markdown(texto_pregunta_5, className="text-content", mathjax=True)
    ], className="content-sidebar") # Clase para los datos (30%)

], className="page-container-grid") # Clase de layout especial