import numpy as np
import os

import vaex
import dash
from dash import html, dcc, Output, Input, callback, State
import dash_bootstrap_components as dbc
from dash_labs.plugins import register_page
from flask_caching import Cache
import plotly.graph_objs as go
import plotly.express as px
from app import app

register_page(__name__, path="vaex")

cache = Cache(app.server, config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': 'cache-directory'
})
CACHE_TIMEOUT = int(os.environ.get('DASH_CACHE_TIMEOUT', '60'))
limits_amount = [0, 50]
limits_duration = [0, 50]
bins = 25
n_largest = 5
resolution_initial = 75
trip_start_initial = -74.193628, 4.581517
trip_end_initial = -74.093633, 4.665334
heatmap_limits_initial = [[-74.160504, -74.039473], [4.562066, 4.772624]]
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

def create_figure_empty():
    layout = go.Layout(plot_bgcolor='white', width=10, height=10,
                       xaxis=go.layout.XAxis(visible=False),
                       yaxis=go.layout.YAxis(visible=False))
    return go.Figure(layout=layout)

def create_figure_histogram(x, counts, title=None, xlabel=None, ylabel=None):

    # settings
    color = 'royalblue'

    # list of traces
    traces = []

    # Create the figure
    line = go.scatter.Line(color=color, width=2)
    hist = go.Scatter(x=x, y=counts, mode='lines', line_shape='hv', line=line, name=title, fill='tozerox')
    traces.append(hist)

    # Layout
    title = go.layout.Title(text=title, x=0.5, y=1, font={'color': 'black'})
    margin = go.layout.Margin(l=0, r=0, b=0, t=30)
    legend = go.layout.Legend(orientation='h',
                              bgcolor='rgba(0,0,0,0)',
                              x=0.5,
                              y=1,
                              itemclick=False,
                              itemdoubleclick=False)
    layout = go.Layout(height=230,
                       margin=margin,
                       legend=legend,
                       title=title,
                       xaxis=go.layout.XAxis(title=xlabel),
                       yaxis=go.layout.YAxis(title=ylabel),
                       **fig_layout_defaults)

    # Now calculate the most likely value (peak of the histogram)
    peak = np.round(x[np.argmax(counts)], 2)

    return go.Figure(data=traces, layout=layout), peak


def create_selection(days, hours):
    df = vaex.read_csv('./data/dfsample/df_test.csv')
    selection = None
    if hours:
        hour_min, hour_max = hours
        if hour_min > 0:
            df.select((hour_min <= df.HOUR), mode='and')
            selection = True
        if hour_max < 23:
            df.select((df.DAY <= hour_max), mode='and')
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


@cache.memoize(timeout=CACHE_TIMEOUT)
def compute_trip_details(days, hours, trip_start, trip_end):
    df, selection = create_selection(days, hours)
    # Filter the dataframe
    r = 0.0145 / 20 * 3  # One mile is ~0.0145 deg and 20 blocks per mile.
    pickup_long, pickup_lat = trip_start
    dropoff_long, dropoff_lat = trip_end

    selection_pickup = (df.pickup_longitude - pickup_long)**2 + (df.pickup_latitude - pickup_lat)**2 <= r**2
    selection_dropoff = (df.dropoff_longitude - dropoff_long)**2 + (df.dropoff_latitude - dropoff_lat)**2 <= r**2
    df.select(selection_pickup & selection_dropoff, mode='and')
    selection = True  # after this the selection is always True

    return {
        'counts': df.count(selection=selection),
        'counts_total': df.count(binby=[df.total_amount], limits=[limits_amount], shape=bins, selection=selection),
        'counts_duration': df.count(binby=[df.trip_duration_min], limits=[limits_duration], shape=bins, selection=selection),
    }

def create_figure_heatmap(data_array, heatmap_limits, trip_start, trip_end):
    # Set up the layout of the figure
    legend = go.layout.Legend(orientation='h',
                              x=0.0,
                              y=-0.05,
                              font={'color': 'azure'},
                              bgcolor='royalblue',
                              itemclick=False,
                              itemdoubleclick=False)
    margin = go.layout.Margin(l=0, r=0, b=0, t=30)
    # if we don't explicitly set the width, we get a lot of autoresize events
    layout = go.Layout(height=600,
                       title=None,
                       margin=margin,
                       legend=legend,
                       xaxis=go.layout.XAxis(title='Longitude', range=heatmap_limits[0]),
                       yaxis=go.layout.YAxis(title='Latitude', range=heatmap_limits[1]),
                       **fig_layout_defaults)

    # add the heatmap
    # Use plotly express in combination with xarray - easy plotting!
    fig = px.imshow(np.log1p(data_array.T), origin='lower')
    fig.layout = layout

    # add markers for the points clicked
    def add_point(x, y, **kwargs):
        fig.add_trace(go.Scatter(x=[x], y=[y], marker_color='azure', marker_size=8, mode='markers', showlegend=True, **kwargs))

    if trip_start:
        add_point(trip_start[0], trip_start[1], name='Trip start', marker_symbol='circle')

    if trip_end:
        add_point(trip_end[0], trip_end[1], name='Trip end', marker_symbol='x')

    return fig


layout = dbc.Container(
    [   
        html.Div(className='app-body', children=[
            # Stores
            dcc.Store(id='map_clicks', data=0),
            dcc.Store(id='trip_start', data=trip_start_initial),
            dcc.Store(id='trip_end', data=trip_end_initial),
            dcc.Store(id='heatmap_limits', data=heatmap_limits_initial),
            # Control panel
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
                                                            trip_start_initial,
                                                            trip_end_initial))
                    ]),
                    html.Div(className="five columns pretty_container", children=[
                        dcc.Graph(id='trip_summary_amount_figure'),
                        dcc.Graph(id='trip_summary_duration_figure'),
                        dcc.Markdown(id='trip_summary_md')
                    ]),
            ]),
        ])
    ]
)

@callback(Output('heatmap_figure', 'figure'),
              [Input('days', 'value'),
               Input('hours', 'value'),
               Input('heatmap_limits', 'data'),
               Input('trip_start', 'data'),
               Input('trip_end', 'data')],
              prevent_initial_call=True)
def update_heatmap_figure(days, hours, heatmap_limits, trip_start, trip_end):
    data_array = compute_heatmap_data(days, hours, heatmap_limits)
    return create_figure_heatmap(data_array, heatmap_limits, trip_start, trip_end)


@callback(
    Output('heatmap_limits', 'data'),
    [Input('heatmap_figure', 'relayoutData')],
    [State('heatmap_limits', 'data')],
    prevent_initial_call=True)
def update_limits(relayoutData, heatmap_limits):
    if relayoutData is None:
        raise dash.exceptions.PreventUpdate
    elif relayoutData is not None and 'xaxis.range[0]' in relayoutData:
        d = relayoutData
        heatmap_limits = [[d['xaxis.range[0]'], d['xaxis.range[1]']], [d['yaxis.range[0]'], d['yaxis.range[1]']]]
    else:
        raise dash.exceptions.PreventUpdate
        if heatmap_limits is None:
            heatmap_limits = heatmap_limits_initial
    return heatmap_limits


@callback([Output('map_clicks', 'data'),
               Output('trip_start', 'data'),
               Output('trip_end', 'data')],
              [Input('heatmap_figure', 'clickData')],
              [State('map_clicks', 'data'),
               State('trip_start', 'data'),
               State('trip_end', 'data')],
              prevent_initial_call=True)
def click_heatmap_action(click_data_heatmap, map_clicks, trip_start, trip_end):
    if click_data_heatmap is not None:
        point = click_data_heatmap['points'][0]['x'], click_data_heatmap['points'][0]['y']
        new_location = point[0], point[1]
        # the 1st and 3rd and 5th click change the start point
        if map_clicks % 2 == 0:
            trip_start = new_location
            trip_end = None  # and reset the end point
        else:
            # the 2nd, 4th etc set the end point
            trip_end = new_location
        map_clicks += 1
    return map_clicks, trip_start, trip_end
# Trip plotting

@callback([Output('trip_summary_amount_figure', 'figure'),
               Output('trip_summary_duration_figure', 'figure'),
               Output('trip_summary_md', 'children'),
               Output('loader-trigger-2', 'children')],
              [Input('days', 'value'),
               Input('hours', 'value'),
               Input('trip_start', 'data'),
               Input('trip_end', 'data')]
              )
def trip_details_summary(days, hours, trip_start, trip_end):
    if trip_start is None or trip_end is None:
        fig_empty = create_figure_empty()
        if trip_start is None:
            text = '''Please select a start location on the map.'''
        else:
            text = '''Please select a destination location on the map.'''
        return fig_empty, fig_empty, text, "trigger loader"

    trip_detail_data = compute_trip_details(days, hours, trip_start, trip_end)
    
    counts = trip_detail_data['counts']
    counts_total = np.array(trip_detail_data['counts_total'])
    counts_duration = np.array(trip_detail_data['counts_duration'])
    fig_amount, peak_amount = create_figure_histogram(df_original.bin_edges(df_original.total_amount, limits_amount, shape=bins),
                                                      counts_total,
                                                      title=None,
                                                      xlabel='Total amount [$]',
                                                      ylabel='Numbe or rides')
    # The trip duration
    fig_duration, peak_duration = create_figure_histogram(df_original.bin_edges(df_original.trip_duration_min, limits_amount, shape=bins),
                                                          counts_duration,
                                                          title=None,
                                                          xlabel='Trip duration [min]',
                                                          ylabel='Numbe or rides')

    trip_stats = f'''
                    **Trip statistics:**
                    - Number of rides: {counts}
                    - Most likely trip total cost: ${peak_amount}
                    - Most likely trip duration: {peak_duration} minutes
                    '''

    return fig_amount, fig_duration, trip_stats, "trigger loader"