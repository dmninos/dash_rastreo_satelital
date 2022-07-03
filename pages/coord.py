from dash import html, callback, Input, Output, State
import dash_bootstrap_components as dbc
from dash_labs.plugins import register_page
import dash_leaflet as dl

from components.maps.map_coords import MapCoords
from components.route.get_route import Route

map_coords = MapCoords('Mapa Selector de coordenadas', 'map_coords', 'layer')
map_layout = map_coords.map_layout

router =  Route()

register_page(__name__, path="coord")

layout = dbc.Container(
    [
        dbc.Row([
            dbc.Col([
                html.Div(map_layout),
                html.Div(id='coords_print')
            ])
        ], ), 
    ]
)


@callback([
    Output("origin", "position"),
    Output("origin", "children"),
],
[
    Input(map_coords.id, "click_lat_lng"),
])
def map_click(click_lat_lng):
    children = "orgin: ({:.3f}, {:.3f})".format(*click_lat_lng)
    tooltip = dl.Tooltip(children)
    return click_lat_lng, tooltip


@callback([
    Output("destination", "position"),
    Output("destination", "children"),
],
[
    Input(map_coords.id, "dbl_click_lat_lng"),
])
def map_dblclick(dbl_click_lat_lng):
    children = "dest: ({:.3f}, {:.3f})".format(*dbl_click_lat_lng)
    tooltip = dl.Tooltip(children)
    return dbl_click_lat_lng, tooltip


@callback(
   Output('route', 'positions'),
[
   Input(map_coords.id, "click_lat_lng"),
   State('destination', 'position'),
])
def show_coords(click_lat_lng, end):
    print("coordinates: ", click_lat_lng, end)
    coordinates = router.coordinates(click_lat_lng, end)
    print("done")
    return coordinates