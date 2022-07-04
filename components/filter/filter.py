import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
from dash_labs.plugins import register_page
from dash import html, Output, Input, callback, State
from datetime import datetime, timedelta, date

class Filter:
    def __init__(self, date_id, button_id, date_label=None, date_description=None):
        self.date_id = date_id
        self.button_id = button_id
        self.date_label = "Date Range for Travel"\
            if date_label is None\
                else date_label
        self.date_description ="Select a date range while you'll be available for travel."\
            if date_description is None\
                else date_description

    def layout(self):
        return dmc.Paper([
            dmc.DateRangePicker(
                id=self.date_id,
                label=self.date_label,
                description=self.date_label,
                minDate=date(2022, 1, 1),
                maxDate=date(2023, 12, 31),
                value=[datetime.now() - timedelta(days=1), datetime.now() + timedelta(days=7)]
            ),
            dmc.Space(h=10),
            dmc.Button(
                "Estimate",
                id=self.button_id,
                leftIcon=[DashIconify(icon="fluent:calculator-arrow-clockwise-24-regular")],
            ),
        ])

