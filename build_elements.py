# import local modules
from config_settings import *

# Data management
import pandas as pd

from dash import Dash, callback, callback_context, clientside_callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import dash_daq as daq
import dash_leaflet as dl

# ----------------------------------------------------------------------------
# PARAMETERS
# ----------------------------------------------------------------------------
# set unicode for arrow / special 'expand' character
arrow = u'\u2197'


# ----------------------------------------------------------------------------
# Build Card gallery
# ----------------------------------------------------------------------------
def build_card(images, selected_image, card_index):
    image = images.loc[selected_image]

    card = dbc.Card(
        [
            dbc.CardImg(src=image.Image_url, top=True),
            dbc.CardBody(
                [
                    dbc.Button(
                        arrow,
                        id = {'type':'card-btn', 'index':card_index},
                        style={'float':'right', 'font-size':'1.2em'}),
                    html.H4(image.Title, className="card-title"),
                    html.P(image.Entry_ID),
                ],
            ),
        ],
        style={"width": "24rem", 'float':'left', 'margin':'5px','padding':'5px', 'border-radious':'5px'
        # ,'height':'35rem'
        },
    )
    return card

def build_card_gallery(images, images_list):
    # try:
    page_layout = html.Div([
        html.Div([build_card(images, i, images_list.index(i)) for i in images_list]),
        html.Div(id='image-popout'),
        # html.Div(
        #     dbc.Modal([
        #                 dbc.ModalHeader(id='modal-image-header'),
        #                 dbc.ModalBody(id='modal-image-header'),
        #                 dbc.ModalFooter(id='modal-image-header'),
        #                     ],
        #             id="modal-image",
        #             size="xl",
        #             centered=True,
        #             is_open=False
        #     )
        # )
    ])
    return page_layout

def build_modal_children(card_index):
    selected_image = images_list[card_index]
    image = images.loc[selected_image]

    modal_children = [
                        dbc.ModalHeader(image.Title),
                        dbc.ModalBody(image.Description),
                        dbc.ModalFooter(selected_image),
                    ]

    return modal_children

def build_gallery_popout(card_index):
    selected_image = images_list[card_index]
    image = images.loc[selected_image]
    header = image.Title
    body = image.Description
    footer = selected_image
    return header, body, footer


# ----------------------------------------------------------------------------
# Build Image Data Entry Form
# ----------------------------------------------------------------------------
def build_form_components():
    location_information = html.Div([
        # dl.Map(dl.TileLayer(url=url, maxZoom=20, attribution=attribution))
        dl.Map(
            [dl.TileLayer(), dl.LayerGroup(id="layer")],
            center = [26.903, -98.158],
            zoom = 8,
            id = "map",
        ),

        html.Div(id='map_location'),
    ], style={'width': '100%', 'height': '65vh', 'margin': "auto", "display": "block", "position": "relative"})

    contact_information = html.Div([
        html.H5('Contact Information'),
        html.P("Please enter your contact information if you are willing to share this with researchers."),
        dbc.Row([
                dbc.Label("Name", html_for="first-name-input", width=1),
                dbc.Col(dbc.Input(type="text", id="first-name-input", placeholder="Enter first name"),width=4,),
                dbc.Col(dbc.Input(type="text", id="last-name-input", placeholder="Enter last name"),width=4,),
            ],className="mb-3",),
        dbc.Row([

            ],className="mb-3",),
        dbc.Row([
                dbc.Label("Email", html_for="email-input", width=1),
                dbc.Col(dbc.Input(type="email", id="email-input", placeholder="Enter email"),width=10,),
            ],className="mb-3",),
        dbc.Row([
                dbc.Label("Phone", html_for="phone-input", width=1),
                dbc.Col(dbc.Input(type="tel",inputMode ="tel", id="phone-input", placeholder="Enter phone number"),width=4,),
            ],className="mb-3",),
        dbc.Row([
                dbc.Label("May we follow up?", html_for="allow-contact-input", width=3),
                dbc.Col(dbc.RadioItems(
                        options=[
                            {"label": "No", "value": 0},
                            {"label": "Yes", "value": 1},
                        ],
                        # value=0,
                        id="allow-contact-input",
                        inline=True,
                        value = 1
                    ),width=3),
            ],className="mb-3",),
        dbc.Collapse(
            dbc.Row([
                    dbc.Label("Preferred Contact Method", html_for="preferred-contact-input", id='preferred-contact-label', width=4),
                    dbc.Col(dbc.RadioItems(
                            options=[
                                {"label": "Phone", "value": 0},
                                {"label": "Email", "value": 1},
                            ],
                            # value=0,
                            id="preferred-contact-input",
                            inline=True,
                        ),width=4),
                ],className="mb-3"),
            id='preferred-contact',
            is_open=True,
        ),

    ])

    location_confidence = html.Div([
            dbc.Row([
                html.H5('Location Confidence'),
                html.P("Please indicate how confident you are in the location selected on the map"),
            ]),
            dbc.Row([
                # dbc.Label("Degree of Confidence", html_for="allow-contact-input", width=3),
                dbc.Col(dbc.RadioItems(
                        options=[
                            {"label": "Very (feet)", "value": 'feet'},
                            {"label": "Fairly (blocks)", "value": 'blocks'},
                            {"label": "Somewhat (~1/4 mile)", "value": '1/4 mile'},
                            {"label": "Slightly (~1 mile)", "value": '1 mile'},
                            {"label": "Not at all (>1 mile)", "value": '> 1mile'},
                        ],
                        # value=0,
                        id="confidence-input",
                        inline=True,
                    ),width=12),
            ])
        ])

    narrative_information = html.Div([
        dbc.Row([
            html.H5('Narrative'),
                # dbc.Label("Narrative", html_for="narrative-input"),
                dbc.Col(dbc.Textarea(id="narrative-input", placeholder="What would you like to share about this photo")),
            ],className="mb-3",),
    ])
    return location_information, contact_information, location_confidence, narrative_information

def build_picture_form(images, image_id):
    image = images.loc[image_id]
    location_information, contact_information, location_confidence, narrative_information = build_form_components()

    picture_form = html.Div([
        dbc.Row([
            dbc.Col([
                html.H3(image.Description),
                html.H5(image.Entry_ID),
                dcc.Markdown(image.Photo, className='text-center')


            ], className = 'image-border', xl=6, xxl=4 ),
            dbc.Col([
                html.H3('Image Location'),
                html.H5('Please describe where you think this image was taken'),
                location_information

            ], className = 'image-border', xl=6, xxl=4 ),
            dbc.Col([
                html.H3('Additional information about this photo'),
                html.Div(id='test-div'),
                html.Div([
                    location_confidence,
                    html.Br(),
                    narrative_information,
                    contact_information,

                ],id='entry-div', style={'scroll':'auto'}),

                dbc.Button("Submit information", id='btn-submit', color="primary", className="me-1", style={'float':'right'}),

            ], className = 'image-border'),

        ]),
    ])
    return picture_form

def build_form(images, image_id):
    # try:
    form = html.Div([
        # photo_row,
         build_picture_form(images, image_id),
         dbc.Modal(
         [
             dbc.ModalHeader(dbc.ModalTitle("GeoJSON")),
             dbc.ModalBody(html.Div(id='div-submit', className = 'popout')),
             # dbc.ModalFooter(
             #     dbc.Button(
             #         "Close", id="close", className="ms-auto", n_clicks=0
             #     )
             # ),
         ],
         id="modal",
         is_open=False,
     ),
        ])
    # except:
    #     page_layout = html.Div(['There has been a problem accessing the data for this application.'])
    return form
