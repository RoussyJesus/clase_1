import dash
from dash import html, dcc, Input, Output, State, callback
import plotly.graph_objects as go
import numpy as np

# Registro de la página
dash.register_page(__name__, path='/Crecimiento_poblacion', name='Crecimiento_poblacion')

# ------------------------------------------------------------------------------
# FUNCIONES DE LÓGICA (REUTILIZABLES)
# ------------------------------------------------------------------------------

def calcular_crecimiento_logistico(P0, r, K, t_max, num_puntos=200):
    """
    Calcula los puntos de la curva de crecimiento logístico.
    """
    t = np.linspace(0, t_max, num_puntos)
    
    if K == 0:
        return t, np.full(num_puntos, P0)
    
    denominador = (K - P0) + P0 * np.exp(r * t)
    
    if np.any(denominador == 0):
        return t, np.zeros(num_puntos) 

    numerador = P0 * K * np.exp(r * t)
    P = numerador / denominador
    
    return t, P

# ------------------------------------------------------------------------------
# FUNCIONES DE PRESENTACIÓN (COMPONENTES REUTILIZABLES)
# ------------------------------------------------------------------------------

def crear_grupo_input(label_text, input_id, value, min_val=0, step=1, tipo="number"):
    """
    Crea un componente de grupo de input (Label + Input) reutilizable.
    """
    return html.Div([
        html.Label(label_text),
        dcc.Input(
            id=input_id,
            type=tipo,
            value=value,
            min=min_val,
            step=step,
            className="input-field"
        )
    ], className="input-group")

def crear_figura_logistica(t, P, K, t_max):
    """
    Crea y estila la figura de Plotly con los datos logísticos.
    """
    # --- Paleta de Colores "Synthwave" (Azul/Morado/Rosa) ---
    COLOR_DATOS_PRINCIPAL = "#EC8B0C"  # Morado/Magenta
    COLOR_LIMITE = "#27FC43"           # Rosa Neón
    COLOR_FONDO_GRAFICO = '#0c162b'    # Fondo de tarjeta oscuro
    COLOR_FONDO_PAPEL = '#0a101f'      # Fondo de página oscuro
    COLOR_TEXTO_PRINCIPAL = "#0077FF"  # Rosa Claro (para títulos)
    COLOR_TEXTO_SECUNDARIO = '#e0e0e0' # Texto claro
    COLOR_GRID = '#333'             # Grid oscuro
    COLOR_ZEROLINE = '#00CFFF'         # Azul Eléctrico
    # -------------------------------------
    
    fig = go.Figure()

    # Trace de la población
    fig.add_trace(go.Scatter(
        x=t,
        y=P,
        mode='lines',
        name='Población P(t)',
        line=dict(color=COLOR_DATOS_PRINCIPAL, width=2.5), # Color de datos
        hovertemplate='t: %{x:.2f}<br>P(t):%{y:.2f}<extra></extra>'
    ))
    
    # Trace de la capacidad de carga
    fig.add_trace(go.Scatter(
        x=[0, t_max],
        y=[K, K],
        mode='lines',
        name='Capacidad de Carga (K)',
        line=dict(color=COLOR_LIMITE, width=2, dash='dash'), # Color de límite
        hovertemplate='K: %{y:.2f}<extra></extra>'
    ))

    # Aplicar el layout (estilos)
    fig.update_layout(
        title=dict(
            text='<b>Modelo Logístico de Crecimiento de la Población</b>',
            font=dict(size=20, color=COLOR_TEXTO_PRINCIPAL), # Color de título
            x=0.5,
            y=0.95
        ),
        xaxis_title='Tiempo (t)',
        yaxis_title='Población P(t)',
        margin=dict(l=40, r=40, t=70, b=40),
        paper_bgcolor=COLOR_FONDO_PAPEL,  # Fondo exterior
        plot_bgcolor=COLOR_FONDO_GRAFICO, # Fondo del gráfico
        font=dict(family='Arial, sans-serif', size=12, color=COLOR_TEXTO_SECUNDARIO), # Fuente
        legend=dict(orientation='h', yanchor='bottom', y=1.02, bgcolor='rgba(0,0,0,0)',
                   font=dict(color=COLOR_TEXTO_SECUNDARIO)) # Fuente de leyenda
    )
    
    # Configurar ejes
    fig.update_xaxes(
        showgrid=True, gridwidth=1, gridcolor=COLOR_GRID,
        zeroline=True, zerolinewidth=2, zerolinecolor=COLOR_ZEROLINE,
        showline=True, linecolor=COLOR_TEXTO_SECUNDARIO, linewidth=1, mirror=True,
        range=[0, t_max]
    )
    
    # Rango Y dinámico
    y_max = max(K, np.max(P)) * 1.1 if len(P) > 0 else K * 1.1
    if y_max == 0: y_max = 10
        
    fig.update_yaxes(
        showgrid=True, gridwidth=1, gridcolor=COLOR_GRID,
        zeroline=True, zerolinewidth=2, zerolinecolor=COLOR_ZEROLINE,
        showline=True, linecolor=COLOR_TEXTO_SECUNDARIO, linewidth=1, mirror=True,
        range=[0, y_max]
    )
    
    return fig

# ------------------------------------------------------------------------------
# LAYOUT DE LA PÁGINA (REDISTRIBUIDO)
# ------------------------------------------------------------------------------

layout = html.Div([
    # MEJORA: Tarjeta 1 - Controles (sin .left)
    html.Div([
        html.H2("Parámetros del modelo", className="title"),
        
        crear_grupo_input("Población inicial P(0):", "input-p0", value=200, step=1),
        crear_grupo_input("Tasa de crecimiento (r):", "input-r", value=0.04, step=0.01),
        crear_grupo_input("Capacidad de Carga (k):", "input-k", value=750, step=10),
        crear_grupo_input("Tiempo máximo (t):", "input-t", value=100, step=5),
        
        html.Button("Generar gráfico", id="btn-generar", className="btn-generar")
    ], className="content"), # Se usa solo "content"
    
    # MEJORA: Tarjeta 2 - Gráfico (sin .right)
    html.Div([
        html.H2("Gráfica", className="title"),
        dcc.Graph(
            id='grafica-poblacion_2',
            style={'height': '450px', 'width': '100%'}
        )
    ], className="content"), # Se usa solo "content"
], className="page-container")

# ------------------------------------------------------------------------------
# CALLBACK
# ------------------------------------------------------------------------------

@callback(
    Output('grafica-poblacion_2', 'figure'),
    Input('btn-generar', 'n_clicks'),
    State('input-p0', 'value'),
    State('input-r', 'value'),
    State('input-k', 'value'),
    State('input-t', 'value'),
    prevent_initial_call=False  # Mantenemos esto para que cargue el gráfico inicial
)
def actualizar_grafica(n_clicks, P0, r, K, t_max):
    
    # --- Paleta de Colores "Synthwave" (para el error) ---
    COLOR_FONDO_GRAFICO = '#0c162b'
    COLOR_FONDO_PAPEL = '#0a101f'
    COLOR_TEXTO_SECUNDARIO = '#e0e0e0'
    # -------------------------------------

    # Validación de inputs
    if any(v is None for v in [P0, r, K, t_max]) or K <= 0 or t_max <= 0 or P0 < 0:
        fig_empty = go.Figure()
        fig_empty.update_layout(
            title="Por favor, ingrese valores válidos (K > 0, t_max > 0, P0 >= 0)",
            paper_bgcolor=COLOR_FONDO_PAPEL,   # MEJORA: Fondo Neón
            plot_bgcolor=COLOR_FONDO_GRAFICO, # MEJORA: Fondo Neón
            font=dict(color=COLOR_TEXTO_SECUNDARIO), # MEJORA: Texto Neón
            xaxis={'visible': False},
            yaxis={'visible': False}
        )
        return fig_empty
            
    # 1. Calcular la lógica
    t, P = calcular_crecimiento_logistico(P0, r, K, t_max)
    
    # 2. Crear la presentación
    fig = crear_figura_logistica(t, P, K, t_max)
    
    return fig