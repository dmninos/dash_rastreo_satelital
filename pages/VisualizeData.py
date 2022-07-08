import numpy as np
import os

import vaex
import dash
from dash import html, dcc, Output, Input, callback, State
import dash_bootstrap_components as dbc
from dash_labs.plugins import register_page
import dash_labs as dl

from flask_caching import Cache
from flask import Flask

import plotly.graph_objs as go
import plotly.express as px

from components.table.table import table
from components.sampledf.model import df_table_speed

register_page(__name__, path="analysis", title="Dashboard")

params1 = {
    'title': 'TOP Speed',
    'description': 'Table with the fastest vehicles',
    'columns': ['TYPE_VEHICULE', 'MONTH', 'PLACA', 'SPEED']
}

tabla_datos_departamentos = table(df_table_speed, params1)

app = Flask(__name__)
cache = Cache(config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': 'cache-directory'
})
cache.init_app(app)

CACHE_TIMEOUT = int(os.environ.get('DASH_CACHE_TIMEOUT', '50'))

limits_amount = [0, 50]
limits_duration = [0, 50]
bins = 25
n_largest = 5
resolution_initial = 100


heatmap_limits_initial = [[-74.235907, -73.996207], [4.570205, 4.766625]]
fig_layout_defaults = dict(
    plot_bgcolor="#F9F9F9",
    paper_bgcolor="#F9F9F9",
)

df_original = vaex.read_csv('./data/dfsample/df_test.csv')
# Make sure the data is cached locally
used_columns = ['DATE_TIME',
                'LATITUDE',
                'LONGITUDE',
                'ADDRESS',
                'SPEED',
                'MILEAGE',
                'ID',
                'VELOCIDAD',
                'IGNICION',
                'CURSO',
                'BATERIA_VEHICULO',
                'ENG_EFF_ON_FUELCONSMATH',
                'ALTITUD',
                'PLACA',
                'YEAR',
                'MONTH',
                'DAY',
                'HOUR'
                ]
df_original.categorize(df_original.DAY, labels=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'], inplace=True)

for col in used_columns:
    print(f'Making sure column "{col}" is cached...')
    df_original.nop(col, progress=True)


def create_selection(days, hours):
    df = vaex.read_csv('./data/dfsample/df_test.csv')
    selection = None
    if hours:
        hour_min, hour_max = hours
        if hour_min > 0:
            df.select((hour_min <= df.HOUR), mode='and')
            selection = True
        if hour_max < 23:
            df.select((df.HOUR <= hour_max), mode='and')
            selection = True
    if (len(days) > 0) & (len(days) < 7):
        df.select(df.DAY.isin(days), mode='and')
        selection = True
    return df, selection

@cache.memoize(timeout=CACHE_TIMEOUT)
def compute_heatmap_data(days, hours, heatmap_limits):
    df, selection = create_selection(days, hours)
    heatmap_data_array = df.count(binby=[df.LONGITUDE, df.LATITUDE],
                                  selection=selection,
                                  limits=heatmap_limits,
                                  shape=256,
                                  array_type="xarray")
    return heatmap_data_array

heatmap_data_initial = compute_heatmap_data([], [0, 23], heatmap_limits_initial)


def create_figure_heatmap(data_array, heatmap_limits):
    # Set up the layout of the figure
    legend = go.layout.Legend(orientation='h',
                              x=0.0,
                              y=-0.05,
                              font={'color': 'AliceBlue'},
                              bgcolor='royalblue',
                              itemclick=False,
                              itemdoubleclick=False)
    margin = go.layout.Margin(l=0, r=0, b=0, t=30)
    # if we don't explicitly set the width, we get a lot of autoresize events
    layout = go.Layout(height=700,
                       title=None,
                       margin=margin,
                       legend=legend,
                       xaxis=go.layout.XAxis(title='Longitude', range=heatmap_limits[0]),
                       yaxis=go.layout.YAxis(title='Latitude', range=heatmap_limits[1]),
                       **fig_layout_defaults)

    # add the heatmap
    fig = px.imshow(np.log1p(data_array.T), origin='lower',color_continuous_scale="dense")
    fig.layout = layout
    
    counts = data_array.data
    (xmin, xmax), (ymin, ymax) = heatmap_limits
    dx = (xmax - xmin) / counts.shape[0]
    dy = (ymax - ymin) / counts.shape[1]

    fig.add_trace(go.Heatmap(z=np.log10(counts.T+1),
                             colorscale='plasma',
                             zmin=None, zmax=None,
                             x0=xmin, dx=(dx),
                             y0=ymin, dy=(dy),
                             showscale=False,
                             hoverinfo=['x', 'y', 'z']))

    return fig


layout = dbc.Container(
    [
        html.Div([
            # Stores
            dcc.Store(id='map_clicks', data=0),
            dcc.Store(id='heatmap_limits', data=heatmap_limits_initial),

            html.Div(children=[
                html.Div(className="row", id='control-panel', children=[
                html.Div(className="four columns pretty_container", children=[
                    html.Label('Select pick-up hours'),
                    dcc.RangeSlider(id='hours',
                                    value=[0, 23],
                                    min=0, max=23,
                                    marks={i: str(i) for i in range(0, 24, 3)})
                ]),
                html.Div(className="four columns pretty_container", children=[
                    html.Label('Select pick-up days'),
                    dcc.Dropdown(id='days',
                                placeholder='Select a day of week',
                                options=[{'label': 'Monday', 'value': 0},
                                        {'label': 'Tuesday', 'value': 1},
                                        {'label': 'Wednesday', 'value': 2},
                                        {'label': 'Thursday', 'value': 3},
                                        {'label': 'Friday', 'value': 4},
                                        {'label': 'Saturday', 'value': 5},
                                        {'label': 'Sunday', 'value': 6}],
                                value=[],
                                multi=True),
                ]),
            ]),

            # Visuals
            html.Div(className="row", children=[
                    html.Div(className="seven columns pretty_container", children=[
                        dcc.Markdown(children='_Click on the map to select trip start and destination._'),
                        dcc.Graph(id='heatmap_figure',
                                figure=create_figure_heatmap(heatmap_data_initial,
                                                            heatmap_limits_initial,
                                                            ))
                    ])
            ]),

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

@callback(Output('heatmap_figure', 'figure'),
              [Input('days', 'value'),
               Input('hours', 'value'),
               Input('heatmap_limits', 'data')],
              prevent_initial_call=True)
def update_heatmap_figure(days, hours, heatmap_limits):
    data_array = compute_heatmap_data(days, hours, heatmap_limits)
    return create_figure_heatmap(data_array, heatmap_limits)
