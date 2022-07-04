import dash_leaflet as dl
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
from dash_labs.plugins import register_page
from dash import html, Output, Input, State, no_update, callback

from components.maps.map_coords import MapCoords
from components.filter.filter import Filter
from components.route.get_route import Route

register_page(__name__, path="coordinates-map", title="Mapa de coordenadas")

map_coords = MapCoords('Mapa Selector de coordenadas', 'map_coords', 'layer')
map_layout = map_coords.map_layout

filter = Filter("date_range", "button_estimate")
filter_layout = filter.layout

route_maker =  Route()


layout = dmc.Paper(
    [
        dbc.Row(dbc.Col(dmc.Paper(
            children = dmc.Button(
                "Filters", 
                id="button_filters",
                variant="light",
                leftIcon=[DashIconify(icon="codicon:filter-filled")],
                fullWidth=False,
                ),
                shadow="xs",
                m="lg"
            ), width="auto")),
        dbc.Row(dbc.Col(html.Div(map_layout),)),
        dmc.Drawer(
            children=filter.layout(),
            id="drawer_filters",
            padding="md",
            size="md",
            title="Filters"
        )
    ],
    shadow="lg",
    p="md",
    style={"max-width": "1320px", "margin": "auto"}
)


@callback(
    Output("drawer_filters", "opened"),
    Input("button_filters", "n_clicks"),
    prevent_initial_call=True,
)
def drawer_demo(n_clicks):
    return True


@callback(
    Output("origin", "position"),
    Output("origin", "children"),
    Input(map_coords.id, "dbl_click_lat_lng"),
    prevent_initial_call=True,
)
def map_click(dbl_click_lat_lng):
    children = "orgin: ({:.3f}, {:.3f})".format(*dbl_click_lat_lng)
    tooltip = dl.Tooltip(children)
    return dbl_click_lat_lng, tooltip


@callback(
    Output("destination", "position"),
    Output("destination", "children"),
    Input(map_coords.id, "click_lat_lng"),
    prevent_initial_call=True,
)
def map_dblclick(click_lat_lng):
    children = "dest: ({:.3f}, {:.3f})".format(*click_lat_lng)
    tooltip = dl.Tooltip(children)
    return click_lat_lng, tooltip


@callback(
    Output('route', 'positions'),
    Output(filter.button_id, "children"),
    Input(filter.button_id, "n_clicks"),
    State(map_coords.id, "click_lat_lng"),
    State('destination', 'position'),
    State(filter.date_id, "value"),
    prevent_initial_call=True,
)
def show_coords(n_clicks, start, end, date_range):
    coordinates = route_maker.coordinates(start, end)
    return coordinates, no_update