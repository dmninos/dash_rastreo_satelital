import dash_leaflet as dl
from dash import html , dcc


class MapCoords:
    def __init__(self, map_title:str, _id:str, layer:str):
        """
        __init__ _summary_
        Args:
            map_title (str): Titulo del mapa, html H4 element
            ID (str): css id to use with callbacks
        """        
        self.map_title = map_title 
        self.id = _id
        self.layer = layer
        # self.__url = "https://a.basemaps.cartocdn.com/Positron/10/-72/4.png"

    # @staticmethod
    # def figure(self):

    #     mapa = go.Choroplethmapbox(
    #         geojson=departamentos, 
    #         locations=self.df.COD_DPTO, 
    #         z=self.df['COUNT'],
    #         colorscale="dense",
    #         text=self.df.DEPARTAMENTO,
    #         marker_opacity=0.9, 
    #         marker_line_width=0.5,
    #         colorbar_title = "COP",
    #         )
    #     annotations = [
    #         dict(
    #             showarrow=False,
    #             align="right",
    #             text="",
    #             font=dict(color="#000000"),
    #             bgcolor="#f9f9f9",
    #             x=0.95,
    #             y=0.95,
    #         )
    #     ]

    #     fig = go.Figure(data=mapa)

        

    #     fig.update_layout(
    #         geo_scope='south america',
    #         mapbox_style="carto-positron",
    #         mapbox_zoom=5.8, 
    #         mapbox_center = {"lat": 6.88970868, "lon": -74.2973328},
    #         annotations=annotations,
    #         height=400),

        
    #     fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        
    #     return fig

    @property
    def map_layout(self):   
            return  dl.Map([dl.TileLayer(url='http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png'), dl.LayerGroup(children=[
                    dl.Marker(position=[4.625019680565743, -74.08115386962892], id='origin'),
                    dl.Marker(position=[4.646236060730802, -74.06467437744142], id='destination'),
                    dl.Polyline(positions= [(4.6246155, -74.0815441), (4.6251219, -74.0824001), (4.6256179, -74.0820031), (4.6260047, -74.0817845), (4.628972, -74.0800679), (4.6289026, -74.0792116), (4.628862, -74.0787223), (4.6290264, -74.0780671), (4.6290675, -74.0779468), (4.6291799, -74.0773412), (4.6292298, -74.0768382), (4.629248, -74.0761873), (4.6291916, -74.0753652), (4.6291676, -74.0750116), (4.6295478, -74.0749777), (4.6293874, -74.0740494), (4.6292749, -74.0733983), (4.6301398, -74.0732429), (4.6300203, -74.0725577), (4.6300097, -74.0724974), (4.6311003, -74.0722959), (4.6313331, -74.0722409), (4.6317066, -74.0721601), (4.6321758, -74.072073), (4.6326675, -74.0719844), (4.6332356, -74.0718761), (4.6333339, -74.0718557), (4.6343928, -74.071622), (4.6344705, -74.0715388), (4.634849, -74.0710466), (4.635108, -74.0707751), (4.6351582, -74.0707276), (4.6355266, -74.0704423), (4.6360081, -74.070173), (4.6369896, -74.0699963), (4.6375308, -74.0698989), (4.637979, -74.0698182), (4.6389617, -74.0696413), (4.6399387, -74.0694655), (4.6408762, -74.0692967), (4.6409583, -74.0692817), (4.6423322, -74.0690306), (4.6427515, -74.068954), (4.6432836, -74.0688607), (4.6439211, -74.0687405), (4.6438691, -74.0677412), (4.6443714, -74.0676503), (4.6442986, -74.067204), (4.6442249, -74.0667716), (4.6440345, -74.0657597), (4.6439984, -74.0655504), (4.6440802, -74.0655361), (4.6447365, -74.065415), (4.6461905, -74.0651468)], id='route')
                ],
                id=self.layer)],
                bounceAtZoomLimits=True, center=[4.6097100, -74.0817500], zoom=11, minZoom=9.5, doubleClickZoom=False,
                id=self.id, style={'width': '100%', 'height': '50vh', 'margin': "auto", "display": "block"}),