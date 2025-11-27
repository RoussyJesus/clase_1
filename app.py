import dash
from dash import html, dcc

app = dash.Dash(__name__, use_pages=True)

orden_principal = [
    "Inicio", 
    "Página", 
    "Tarea", 
    "Pagina1", 
    "Crecimiento_Poblacion", 
    "Campo_Vectorial", 
    "Modelo SIR"
]

orden_proyecto = [
    "Proyecto Modelo SIR", 
    "Modelo SIR de Rumor",
    "Resultados: Susceptibles S(t)",
    "Resultados: Evolución Promotores Activos",
    "Resultados:Adoptantes Pasivos R(t)",
    "Resultados: Comparación I(t)"
]

def get_menu_items():

    main_links = []
    project_links = []

    for page in dash.page_registry.values():
        path = page["relative_path"]
        if path.lower().startswith("/proyecto"):
            project_links.append(page)
        else:
            main_links.append(page)

    def sort_pages(pages_list, order_list):
        return sorted(
            pages_list, 
            key=lambda x: order_list.index(x["name"]) if x["name"] in order_list else 999
        )

    main_links = sort_pages(main_links, orden_principal)
    project_links = sort_pages(project_links, orden_proyecto)

    menu_html = []

    for page in main_links:
        menu_html.append(
            dcc.Link(
                page["name"],
                href=page["relative_path"],
                className='nav-link'
            )
        )

    if project_links:
        dropdown_html = html.Div([
            html.Div([
                "Proyecto",
                html.Span(" ▼", className="dropdown-arrow") 
            ], className='nav-link dropdown-trigger'),

            html.Div([
                dcc.Link(
                    subpage["name"],
                    href=subpage["relative_path"],
                    className='dropdown-item'
                ) for subpage in project_links
            ], className='dropdown-content')
        ], className='dropdown')
        
        menu_html.append(dropdown_html)

    return menu_html

app.layout = html.Div([
    html.H1("Técnicas de Modelamiento Matemático", className='app-header'),

    html.Div([
        html.Div(
            get_menu_items(), 
            className='nav-links'
        )
    ], className='navigation'),

    dash.page_container
], className='app-container')

if __name__ == '__main__':
    app.run(debug=True)
