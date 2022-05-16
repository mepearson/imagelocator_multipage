import json
import datetime

from dash import Dash, callback, callback_context, clientside_callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL
import dash_bootstrap_components as dbc

# import local modules
from config_settings import *
from data_passing import *
from build_elements import *

# @callback(
#     Output('url', 'pathname'),
#     Input({'type':'btn-path', 'index':ALL}, 'n_clicks'))
# def display_value(nclicks):
#     ctx = callback_context
#     if not ctx.triggered:
#         return ''
#     else:
#         button_id = json.loads(ctx.triggered[0]['prop_id'].split('.')[0])
#         return button_id['type']

# ----------------------------------------------------------------------------
# GALLERY CALLBACKS
# ----------------------------------------------------------------------------

@callback(
    Output('modal-image','is_open'),
    Output('modal-image','children'),
    # Output('modal-body','children'),
    Input({"index": ALL, "type": 'card-btn'}, "n_clicks")
)
def open_modal(n_click):
    ctx = callback_context
    if not ctx.triggered:
        modal_children = 'No clicks yet'
        return False, modal_children
    else:
        button_id = json.loads(ctx.triggered[0]['prop_id'].split('.')[0])
        button_index = button_id['index']
        image_id = images_list[button_index]
        image = images.loc[image_id]
        link_href = '/form?' + image_id

        modal_children = [
                        dbc.ModalHeader([
                            html.H4(image.Title)
                            ]),
                        dbc.ModalBody([
                            html.Img(src=image.Image_url),
                            html.P(image.Description),
                            html.P(['Image Entry: ', selected_image])
                            ]),
                        dbc.ModalFooter([
                            # dbc.Button('Add Data', id={'type':'btn-add-info', 'index':button_index}),
                            dcc.Link('Submit Information about this Photo', href=link_href),
                        ]),
            ]

        # modal_children = build_modal_children(image_list_index)
        return True, modal_children

# ----------------------------------------------------------------------------
# IMAGE FORM CALLBACKS
# ----------------------------------------------------------------------------
@callback(
    Output("div-form", "children"),
    Input('url', "search")
)
def return_image_form(s):
    fail_msg = 'Please enter a valid image ID as a query parameter [?image=<image_id>] to the url above'
    if s:
        image_id = s.replace('?','')
        if image_id in images_list:
            return build_form(images, image_id)
        else:
            return html.H4(image_id)
    else:
        return html.H4(fail_msg)

@callback(
    [
        Output("layer", "children"),
        Output("map_location", "children")
    ],
    Input("map", "click_lat_lng")
)
def map_click(click_lat_lng):
    if click_lat_lng is None:
        new_layer_children = None
        message = html.P('Please place a point on the map where you believe this image was located.')
    else:
        new_layer_children = [
            dl.Marker(
                position = click_lat_lng,
                children = dl.Tooltip("({:.3f}, {:.3f})".format(*click_lat_lng))
            )
        ]
        location = html.Span('{:.3f}, {:.3f}'.format(*click_lat_lng), style={"font-weight": "bold", "color": "blue"})
        message = [html.Span('Marker Location: '), location]

    return new_layer_children, message

@callback(
    Output("preferred-contact", "is_open"),
    Input("allow-contact-input", "value")
)
def show_preferred(allow_contact):
    if allow_contact:
        return True
    else:
        return False

@callback(
    [Output('modal','is_open'), Output('div-submit','children')],
    Input('btn-submit','n_clicks'),
    [State("map", "click_lat_lng"), State("narrative-input","value"),State("first-name-input","value"),State("last-name-input","value"),
    State("email-input","value"),State("phone-input","value"),State("allow-contact-input","value"),State("preferred-contact-input","value"),
    ]
)
def func(n_clicks, point, narrative, firstname, lastname, email, phone, allowcontact, preferred):
    ctx = callback_context
    if not ctx.triggered:
        div_children = ['']
        return False, div_children
    else:
        new_entry = data_init

        new_entry['properties']['timestamp'] = datetime.datetime.now().isoformat()
        new_entry['properties']['image_id'] = selected_image
        new_entry['geometry']['coordinates'] = point
        new_entry['properties']['narrative']  = narrative

        new_entry['properties']['contact']['firstname']  = firstname
        new_entry['properties']['contact']['lastname']  = lastname
        new_entry['properties']['contact']['email']  = email
        new_entry['properties']['contact']['phone']  = phone

        if allowcontact:
            new_entry['properties']['contact']['contactable']  = "true"
            new_entry['properties']['contact']['preferred_contact']  = preferred
        else:
            new_entry['properties']['contact']['contactable']  = "false"
            new_entry['properties']['contact']['preferred_contact']  = None

        submit_div = json.dumps(new_entry,  sort_keys=True, indent=4, separators=(',', ': '))
        return True, submit_div
    # trigger = callback_context.triggered[0]
    # return "You clicked button {}".format(trigger["prop_id"].split(".")[0])
