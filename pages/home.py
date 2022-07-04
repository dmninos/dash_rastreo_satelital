from logging import _STYLES
import dash
import pandas as pd
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash_labs.plugins import register_page

from components.table.table import table
from components.maps.mapcol_departamentos import mapcol_departamentos
from components.sampledf.model import df_markers, df_maptest

mapa_colombia_departamentos = mapcol_departamentos('Mapa Trafico en la Bogotá D.C', 'div_municipios_fig2', df_maptest)

params1 = {
    'title': 'TOP Velocidades',
    'description': 'Tabla con los vehiculos mas rapidos',
    'columns': ['TYPE_VEHICULE', 'MONTH', 'PLACA', 'SPEED']
}

tabla_datos_departamentos = table(df_markers, params1)

register_page(__name__, path="")

layout = dbc.Container(
    [
        html.Div([

            html.Div(children=[
                html.H5("MES"),
                dbc.Row([
                    dcc.RangeSlider(
                        id='range_slider',
                        min=0,
                        max=12,
                        step=1,
                        value=[3, 5]
                    )
                ]),

                dcc.Dropdown(df_maptest.DEPARTAMENTO.unique(),
                             id='memory-countries',
                             multi=True),

                dbc.Row([
                    dbc.Col([
                        html.Div([
                            mapa_colombia_departamentos.display()
                        ], id="row_map")
                    ])
                ], ),

            ], className="card", style={'width': '60%', 'display': 'inline-block'}
            )

            ,

            html.Div(children=[

                html.Div([
                    tabla_datos_departamentos.display()
                ], id="row_tabla")

            ], className="card", style={'width': '40%', 'display': 'inline-block'})

        ], className="card", style={'display': 'flex', 'flex-direction': 'row'}
        )
    ]
)
