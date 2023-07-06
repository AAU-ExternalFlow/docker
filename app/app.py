import os
import datetime
import base64
import uuid
# import sys
from dash import Dash, html, dcc, dash_table
from dash.dependencies import Input, Output, State
import plotly.express as pu
import pandas as pd
import dash_bootstrap_components as dbc

from app_components import *

UPLOAD_DIRECTORY = "/app/uploads"

checklist_options = [
    {'label': '0degrees', 'value': '0d'},
    {'label': '5degrees', 'value': '5d'},
    {'label': '10degrees', 'value': '10d'}
]

debug = False if os.environ["DASH_DEBUG_MODE"] == "False" else True

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


server = app.server
app.layout = html.Div([
    dbc.Card(
        dbc.CardBody([
            # html.Br(),
            dbc.Row([
                dbc.Col([
                    dcc.Markdown("""
                        # [External Flow AAU Energy](https://externalflow.energy.aau.dk/)
                        By [Jakob Hærvig](https://haervig.com/) and Victor Hvass Mølbak.
                    """)
                ], width=True),
                dbc.Col([
                    html.Img(src="externalFlow.jpg", alt="External Flow Logo", height="30px"),
                ], width=1)
            ], align="end"),
            html.Hr(),
            dbc.Row([
                dbc.Col([
                    dbc.Card(
                        dbc.CardBody(
                            uploadImage,
                        ),
                        className="border-0 bg-transparent"
                    ),

                    # html.Hr(),
                    dbc.Button(
                        "Angle of Attack",
                        id="button_AOA"
                    ),
                    dbc.Collapse(
                        dbc.Card(
                            dbc.CardBody(
                                AOA_checklist,
                            )
                        ),
                        id="collapse_AOA",
                        is_open=False
                    ),

                    dbc.Button( "Image Processing", id="button_imageProcessing", n_clicks=0),
                    dbc.Popover(
                        [
                            dbc.PopoverHeader("Image processing steps"),
                            dbc.PopoverBody(dbc.Row([
                                dbc.Col([
                                    "image here",
                                    html.Img(src="app/placeholder_image.png"),
                                ])
                            ])),
                        ],
                        id="popover_imageProcessing",
                        # is_open=False,
                        target="button_imageProcessing",
                        # body=True,
                        placement="bottom",
                        trigger="legacy",
                    ),
                    
                ], width=4)
            ], align='center')
        ])
    )




])



# app.layout = html.Div([
#     html.Div(children=[
#         dcc.Upload(
#             id='upload-image',
#             children=html.Div([
#                 'Drag and Drop or ',
#                 html.A('Select Files')
#             ]),
#             style={
#                 'width': '100%',
#                 'height': '60px',
#                 'lineHeight': '60px',
#                 'borderWidth': '1px',
#                 'borderStyle': 'dashed',
#                 'borderRadius': '5px',
#                 'textAlign': 'center',
#                 'margin': '10px'
#             },
#             # Allow multiple files to be uploaded
#             multiple=False
#         ),
#         html.Div(id='output-image-upload'),
#     ], style={'width': '49%', 'padding': 10, 'flex': 1}),

#     html.Div(children=[
#         html.Button('Analyze Image', id='analyze-button', n_clicks=0),
#         html.Div(id='output-image')
#     ], style={'width': '49%', 'padding': 10, 'flex': 1}),

#     html.Div(children=[
#         html.Label('checklistAOA:'),
#         html.Br(),
#         dcc.Checklist(
#             id='checklistAOA',
#             options=[
#                 {'label': '0degrees', 'value': '0d'},
#                 {'label': '5degrees', 'value': '5d'},
#                 {'label': '10degrees', 'value': '10d'} 
#             ],
#             value=[]
#         ),
#         html.Div(id='outputAOA'),
#         html.Div(id='output-message')
#     ]),

#     html.Div(children=[
#         dbc.Button("Legacy", id="dropdown", color="primary", n_clicks=0),
#         dbc.Popover(
#             [
#                 dbc.PopoverHeader("Popover header"),
#                 dbc.PopoverBody("And here's some amazing content. Cool!"),
#             ],
#             id="popover",
#             is_open=False,
#             target="dropdown",
#         ),
#     ]),
# ], style={'display': 'flex', 'flex-direction': 'row'})

#Callback to expand AOA menu.
@app.callback(
    Output("collapse_AOA", "is_open"),
    [Input("button_AOA", "n_clicks")],
    [State("collapse_AOA", "is_open")]
)
def toggle_shape_collapse(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open



def parse_contents(contents, filename, date):
    return html.Div([
        html.H5(filename),
        # html.H6(datetime.datetime.fromtimestamp(date)),

        # HTML images accept base64 encoded strings in the same format
        # that is supplied by the upload
        html.Img(src=contents, style={'width': '100%'}),
        html.Hr(),
        # html.Div('Raw Content'),
        # html.Pre(contents[0:200] + '...', style={
            # 'whiteSpace': 'pre-wrap',
            # 'wordBreak': 'break-all'
        # })
    ])

@app.callback(Output('output-image-upload', 'children'),
              Output('output-image-upload2', 'children'),
              Input('upload-image', 'contents'),
              State('upload-image', 'filename'),
              State('upload-image', 'last_modified'))
def update_output(contents, filename, date):
    if contents is not None:
        children = [
            parse_contents(contents, filename, date)
        ]
        return children


@app.callback(
    Output('output-image', 'children'),
    Input('analyze-button', 'n_clicks'),
    State('upload-image', 'contents'),
    prevent_initial_call=True
)
def analyze_image(n_clicks, contents):
    if contents is not None:
        #Decode the contents of the uploaded file
        _, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)

        #Save the image to a file within the container's file system
        unique_filename = str(uuid.uuid4()) + '.jpg'
        image_path = os.path.join(UPLOAD_DIRECTORY, unique_filename)
        with open(image_path, 'wb') as f:
            f.write(decoded)

        print('Analysis on uploaded image:', image_path)

        #Return the image in the output div
        return html.Img(src=contents, style={'width': '100%'})

@app.callback(
    Output('output-message', 'children'),
    [Input('checklistAOA', 'value')],
    prevent_initial_call=True
)
def save_checklist(checkbox_values):
    if checkbox_values:
        #Save the checklist as a text file
        filename = 'checklist.txt'
        file_path = os.path.join(UPLOAD_DIRECTORY, filename)

        #Sort the checklist values in the same order as the options
        sorted_values = sorted(checkbox_values, key=lambda x: [option['value'] for option in checklist_options].index(x))

        with open(file_path, 'w') as f:
            f.write('\n'.join(sorted_values))



# @app.callback(
#     Output("popover_imageProcessing", "is_open"),
#     [Input("button_imageProcessing", "n_clicks")],
#     [State("popover_imageProcessing", "is_open")],
# )
# def toggle_popover(n, is_open):
#     if n:
#         return not is_open
#     return is_open

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8050", debug=debug)