from logging import _STYLES
import dash
import pandas as pd
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash_labs.plugins import register_page


register_page(__name__, path="")

layout = dbc.Container(
    [
        html.Div([

            html.Div(children=[

            ], className="card", style={'width': '60%', 'display': 'inline-block'}
            )

            ,

            html.Div(children=[

            ], className="card", style={'width': '40%', 'display': 'inline-block'})

        ], className="card", style={'display': 'flex', 'flex-direction': 'row'}
        )
    ]
)
