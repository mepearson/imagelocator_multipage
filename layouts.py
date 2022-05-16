from dash import Dash, callback, callback_context, clientside_callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import dash_daq as daq

from config_settings import *
from data_passing import *
from build_elements import *

layout_home = html.Div([
    html.H3('Home'),
    dcc.Link('Return to Form', href='/form'),
    html.Br(),
    dcc.Link('Return to Gallery', href='/gallery')
])

layout_gallery = html.Div([
    # html.H3('Gallery'),
    # dcc.Link('Return to Form', href='/form'),
    html.Div([build_card(images, i, images_list.index(i)) for i in images_list]),
    html.Div(id='image-popout'),
    html.Div(
        dbc.Modal(

                id="modal-image",
                size="xl",
                centered=True,
                is_open=False
        )
    )
])

layout_form = html.Div([
    dbc.Row([
        dbc.Col(dcc.Link('Return to Gallery', href='/gallery'), width='1'),
    ], justify='end'),
    dbc.Row([
        html.Div(id='div-form'),
    ])
])
