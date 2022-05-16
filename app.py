from dash import Dash, dcc, html, Input, Output, callback

# import local modules
from config_settings import *
from data_passing import *

from layouts import *
from callbacks import *

external_stylesheets_list = [dbc.themes.SANDSTONE] #  set any external stylesheets

app = Dash(__name__,
                external_stylesheets=external_stylesheets_list,
                meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1'}],
                requests_pathname_prefix=REQUESTS_PATHNAME_PREFIX,
                prevent_initial_callbacks = True,
                suppress_callback_exceptions=True
                )


# server = app.server

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
# def display_page(pathname):
#     return html.Div([
#         html.H3(f'You are on page {pathname}')
    # ])
def display_page(pathname):
    if pathname == '/form':
         return layout_form
    elif pathname == '/gallery':
         return layout_gallery
    else:
        return html.Div([
            html.H3(f'You are on page {pathname}')
        ])
        return f'{pathname}'


# 2017.025.018

# ----------------------------------------------------------------------------
# RUN APPLICATION
# ----------------------------------------------------------------------------

if __name__ == '__main__':
    app.run_server(debug=True)
else:
    server = app.server
