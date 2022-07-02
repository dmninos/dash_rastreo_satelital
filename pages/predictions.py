from dash import html , dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
from dash_labs.plugins.pages import register_page
from datetime import date

from components.maps.mapcol_departamentos import mapcol_departamentos

from components.sampledf.model import df_maptest

mapa_colombia_departamentos = mapcol_departamentos('Mapa Departamentos Colombia', 'div_municipios_fig2',df_maptest)


register_page(__name__, path="predictions")


layout = dbc.Container(
    [
        dbc.Row([
            dbc.Col([
                 html.H4("Prediccion", className='title ml-2')
            ])
        ]),
        
        html.Div([
            
            html.Div(children=[
                html.H6("Filtros"),
                
                dbc.Row([
                    dcc.DatePickerRange(
                        id='date-picker-range',
                        start_date=date(2022, 1, 1),
                        end_date_placeholder_text='Select a date!'
                    ),
                ],className= "card"),
                
                dbc.Row([
                    dcc.Checklist(['Carro', 'Moto'],
                    ['Carro', 'Moto'], inline=False),
                ],className= "card"),
                
                dbc.Row([
                    dcc.Dropdown(
                            id="id_selector_municipio",
                            options=[
                                {"label": "TODOS", "value": "TODOS"},
                                {"label": "BOYACA", "value": "BOYACA"},
                                {"label": "CUNDINAMARCA", "value": "CUNDINAMARCA"},
                                {"label": "ANTIOQUIA", "value": "ANTIOQUIA"},
                                {"label": "SANTANDER", "value": "SANTANDER"},
                        ],value=['BOYACA', 'SANTANDER', 'CUNDINAMARCA', 'ANTIOQUIA'],multi = True),
                ], ),
                
                dbc.Row([
                    html.Button('Submit', id='button-example-1'),
                ],className= "card"),
                    
            ],className= "card", style={'width': '20%', 'display': 'inline-block'}
            )
                 
            ,
                
            html.Div(children=[
                
                html.Div([
                            mapa_colombia_departamentos.display()  
                        ],id="row_map", className= "card"),
                dcc.Textarea(
                    placeholder='Enter a value...',
                    value='Prediccion......',
                    style={'width': '100%'}, className= "card"
                )
                
            ],className= "card", style={'width': '80%', 'display': 'inline-block'})
            
                
        ],className= "card", style={'display': 'flex', 'flex-direction': 'row'}
        )
    ]
)


@callback(
        [Output("row_map", 'children')], 
        [State("id_selector_municipio", "value"), 
         State("slider-updatemode","value"),
         Input("id_filtrar", "n_clicks"),
                
        ],prevent_initial_call=True
    )
def update_map(selector_municipio,selector_year,nclicks):
        df_filtrado = mapa_colombia_departamentos.df[mapa_colombia_departamentos.df['DEPARTAMENTO'].isin(selector_municipio)]
        df_filtrado = df_filtrado[df_filtrado['COUNT']<(10**selector_year)]
        mapa_colombia_departamentos.df = df_filtrado
        nuevo_mapa = mapa_colombia_departamentos.display()
        #mapa_filtrado = mapcol_departamentos('Mapa Filtrado', 'id_filtrado', df_filtrado )
        #nuevo_mapa = mapa_filtrado.display()
        return [nuevo_mapa]