import dash 
from dash import html, dcc, callback, Input, Output, State
import numpy as np
import plotly.graph_objects as go
import plotly.figure_factory as ff 

dash.register_page(__name__, path="/Campo_Vectorial", name="Campo_Vectorial")


COLOR_DATOS_PRINCIPAL = '#E000CF'  
COLOR_DATOS_SECUNDARIO = '#00CFFF' 
COLOR_TITULO = '#d36bff'           
COLOR_TEXTO_SECUNDARIO = '#e0e0e0' 
COLOR_FONDO_GRAFICO = '#0c162b'    
COLOR_FONDO_PAPEL = '#0a101f'     
COLOR_GRID = '#333'            
COLOR_ZEROLINE = '#b807ff'         


layout = html.Div([
   
    html.Div([
        html.H2("Campo Vectorial", className="title"),
        
        
        html.Div([
            html.Label("Ecuación dx/dt = "),
            dcc.Input(id="input-fx-c5", type = "text", value = "y", className="input-field")
        ], className="input-group"),
        html.Div([
            html.Label("Ecuación dy/dt = "),
            dcc.Input(id="input-fy-c5", type = "text", value = "-x", className="input-field")
        ], className="input-group"),
        html.Div([
            html.Label("Rango del Eje X = "),
            dcc.Input(id="input-xmax-c5", type = "number", value = 5, className="input-field")
        ], className="input-group"),
        html.Div([
            html.Label("Rango del Eje Y = "),
            dcc.Input(id="input-ymax-c5", type = "number", value = 5, className="input-field")
        ], className="input-group"),
        html.Div([
            html.Label("Mallado (n)= "),
            dcc.Input(id="input-n-c5", type = "number", value = 15, className="input-field")
        ], className="input-group"),
        
        
        html.Button("Generar campo", id = "btn-generar-c5", className="btn-generar"),
        
        
        html.Div([
            html.H3("Ejemplos para probar:", style={'color': COLOR_TITULO, 'marginTop': '20px'}),
            html.P("dx/dt=x, dy/dt=y (Fuente)"),
            html.P("dx/dt=-x, dy/dt=-y (Sumidero)"),
            html.P("dx/dt=y, dy/dt=-x (Centro)"),
            html.P("dx/dt=-y, dy/dt=np.cos(x)"),
        ], className="text-content-examples")

    ], className="content"), 
    
   
    html.Div([
        html.H2("Visualización del Campo Vectorial", className="title"),
        dcc.Graph(id="grafica-campo-c5", style={"height":"450px","width":"100%"}),
        html.Div(id="info-campo-c5", className="info-message") 
    ], className="content") 

], className="page-container")

@callback(
    [Output("grafica-campo-c5", "figure"),
     Output("info-campo-c5", "children")],
     Input("btn-generar-c5", "n_clicks"),
     State("input-fx-c5", "value"),
     State("input-fy-c5", "value"),
     State("input-xmax-c5", "value"),
     State("input-ymax-c5", "value"),
     State("input-n-c5", "value"),
     prevent_initial_call=False
)
def generar_campo(n_clicks, fx_str, fy_str, xmax, ymax, n):
    
    
    if n > 50:
        n = 50
    if n < 5:
        n = 5
        
    x = np.linspace(-xmax, xmax, n)
    y = np.linspace(-ymax, ymax, n)
    X, Y = np.meshgrid(x, y)
    info_mensaje = ""
    
    try:
        diccionario = {
            "x": X, "y": Y, "np": np,
            "sin": np.sin, "cos": np.cos, "tan": np.tan,
            "exp": np.exp, 'sqrt': np.sqrt, 'pi': np.pi, 'e': np.e 
        }
        fx = eval(fx_str, {}, diccionario)
        fy = eval(fy_str, {}, diccionario)
        
       
        mag = np.sqrt(fx**2 + fy**2)
        mag[mag == 0] = 1.0 
        fx = fx / mag
        fy = fy / mag
        
        mag_max = np.max(mag)
        mag_min = np.min(mag)
        info_mensaje = f"Magnitud: min ={mag_min:.2f}, max = {mag_max:.2f}"
        
    except Exception as error: 
        
        fig_error = go.Figure()
        fig_error.update_layout(
            title=f"Error en la expresión: {str(error)}",
            paper_bgcolor=COLOR_FONDO_PAPEL,
            plot_bgcolor=COLOR_FONDO_GRAFICO,
            font=dict(color=COLOR_TEXTO_SECUNDARIO),
            xaxis={'visible': False},
            yaxis={'visible': False}
        )
        return fig_error, f"Error en las expresiones: {str(error)}"

    
    fig = ff.create_quiver(X, Y, fx, fy,
                           scale=1.5 / n, 
                           arrow_scale=0.3, 
                           line=dict(color=COLOR_DATOS_SECUNDARIO, width=1.5), 
                           name='Vectores')

    fig.update_layout(
        title=dict(
            text = f"<b>Campo: dx/dt = {fx_str}, dy/dt = {fy_str}</b>",
            x=0.5,
            font=dict(color=COLOR_TITULO, size=16)
        ),
        xaxis_title = "x",
        yaxis_title="y",
        paper_bgcolor=COLOR_FONDO_PAPEL,
        plot_bgcolor=COLOR_FONDO_GRAFICO,
        font=dict(color=COLOR_TEXTO_SECUNDARIO),
        legend=dict(font=dict(color=COLOR_TEXTO_SECUNDARIO), bgcolor='rgba(0,0,0,0)')
    )
    
    fig.update_xaxes(
        showgrid=True, gridwidth=1, gridcolor = COLOR_GRID,
        zeroline=True, zerolinewidth=2, zerolinecolor=COLOR_ZEROLINE,
        showline=True, linecolor=COLOR_TEXTO_SECUNDARIO, linewidth=1, mirror=True,
        range=[-xmax*1.1, xmax*1.1]
    )
    fig.update_yaxes(
        showgrid=True, gridwidth=1, gridcolor = COLOR_GRID,
        zeroline=True, zerolinewidth=2, zerolinecolor=COLOR_ZEROLINE,
        showline=True, linecolor=COLOR_TEXTO_SECUNDARIO, linewidth=1, mirror=True,
        range=[-ymax*1.1, ymax*1.1]
    )
    
    return fig, info_mensaje