from dash import Dash, html, dcc, dash_table
import dash_bootstrap_components as dbc

uploadImage = [
    html.Div(children=[
        dcc.Upload(
            id='upload-image',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files')
            ]),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px'
            },
            # Allow multiple files to be uploaded
            multiple=False
        ),
        html.Div(id='output-image-upload'),
    ]),
]

AOA_checklist = [
    html.Div(children=[
        html.Label('checklistAOA:'),
        html.Br(),
        dcc.Checklist(
            id='checklistAOA',
            options=[
                {'label': '0degrees', 'value': '0d'},
                {'label': '5degrees', 'value': '5d'},
                {'label': '10degrees', 'value': '10d'} 
            ],
            value=[]
        ),
        html.Div(id='outputAOA'),
        html.Div(id='output-message')
    ]),
]