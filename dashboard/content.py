from dash import dcc, html
import dash_bootstrap_components as dbc
from utils_modal import info_body
from configurations import config, time_options, content_style
from utils_functions import make_card_grid, speed_labels
import numpy as np


######################
#   Card components
######################
def make_plot_card(value_name, dropdown_id, graph_id, timestamp_id):
    # Header
    if value_name == "Wind Rose":
        header = dbc.Row([
            dbc.Col(html.I(className="bi bi-info-circle", id="Wind Rose-info-icon", n_clicks=0, style={"font-size": "24px", "cursor": "pointer"}),
                    style={"float": "left"}, className="position-absolute top-50 start-0 translate-middle-y", width=1),
            dbc.Modal([
                dbc.ModalHeader(dbc.ModalTitle("How to read a Wind Rose"), className="modal-header"),
                dbc.ModalBody(info_body)],
                id="modal_Wind Rose",
                scrollable=True,
                size="xl",
                is_open=False,
            ),
            dbc.Col(html.H4(value_name, className="my-auto"), style={"margin-right": "10px"}, width=6, align="center"),
            dbc.Col(dcc.Dropdown(
                id=dropdown_id,
                options=time_options,
                value=1,
                clearable=False,
                searchable=False,
                style={'color': 'black', 'align': 'center', 'width': '100px', 'float': 'right'},
            ), width=4, style={"display": "flex", "align-items": "center", "justify-content": "flex-end"}),
            dbc.Col([
                dbc.Button(
                    html.I(className="fa fa-refresh", style={"font-size": "24px"}),
                    id="Wind Rose-refresh-button",
                    n_clicks=0,
                    style={"float": "right"}, className="position-absolute top-50 end-0 translate-middle-y"),
                dbc.Tooltip(
                    "Refresh the plot",
                    target="Wind Rose-refresh-button",
                    placement="bottom",
                    style={"text-transform": "none"},
                ),
            ], width=1, align="center"),
        ], align="center")
    else:
        header = dbc.Row([
            dbc.Col(html.H4(value_name, className="my-auto"), width=7, align="center"),
            dbc.Col(dcc.Dropdown(
                id=dropdown_id,
                options=time_options,
                value=1,
                clearable=False,
                searchable=False,
                style={'color': 'black', 'align': 'center', 'width': '100px', 'float': 'right'},
            ), width=4, style={"display": "flex", "align-items": "center", "justify-content": "flex-end"}),
            dbc.Col([
                dbc.Button(
                    html.I(className="fa fa-refresh", style={"font-size": "24px"}),
                    id=f"{value_name}-refresh-button",
                    n_clicks=0,
                    style={"float": "right"}, className="position-absolute top-50 end-0 translate-middle-y"),  # , "margin-right": "30px"
                dbc.Tooltip(
                    "Refresh the plot",
                    target=f"{value_name}-refresh-button",
                    placement="bottom",
                    style={"text-transform": "none"},
                ),
            ], width=1, align="center"),
        ], align="center")
    # Body
    body = html.Div(dbc.Spinner(
        size="md",
        color="primary",
        delay_show=1000,
        children=[dcc.Graph(id=graph_id, figure={}, style={"width": "97%", "height": "100%"}, config=config)]),  # width and height to 100% of the parent element
        #id=f"{graph_id}-loading",
    )
    return dbc.Card(
        [
            dbc.CardHeader(header, className="card text-white bg-primary", style={'width': '100%'}),
            dbc.CardBody(body, style={"maxHeight": 500, "width": "100%", "padding": 0}),
            dbc.CardFooter(id=timestamp_id, children=[]),
        ],
        className="m-2 shadow",
        style={"minWidth": "36rem", "maxHeight": "36rem"},
    )


cards = [
    make_plot_card("Wind Speed", "wind_hour_choice", "wind-graph", "wind-timestamp"),
    make_plot_card("Humidity", "hum_hour_choice", "humidity-graph", "hum-timestamp"),
    make_plot_card("Temperature", "temp_hour_choice", "temp-graph", "temp-timestamp"),
    make_plot_card("Wind Rose", "windrose_hour_choice", "wind-rose", "windrose-timestamp"),
    make_plot_card("Global Radiation", "rad_hour_choice", "radiation-graph", "rad-timestamp"),
    make_plot_card("Brightness", "brightness_hour_choice", "brightness-graph", "brightness-timestamp"),
]

######################
# # Define content
######################
content = html.Div(children=[
    html.Div(dbc.Col(make_card_grid(cards))),
    dcc.Interval(id='interval-component', interval=60000, n_intervals=0, disabled=False),  # 1min update
], className="p-2", style=content_style)

##################
# Wind rose definition for the callback
##################
# Define bins and labels for speed and wind
spd_bins = [-1, 0.99, 5.99, 11.99, 19.99, 28.99, 38.99, 49.99, 61.99, 74.99, 88.99, 102.99, np.inf]
spd_labels = speed_labels(spd_bins, units='km/h')
# represent boundaries of wind direction bins. Each bin spans 22.5 degrees.
dir_bins = np.arange(-22.5 / 2, 360 + 22.5, 22.5)
# assign midpoint of each bin
dir_labels = (dir_bins[:-1] + dir_bins[1:]) / 2
