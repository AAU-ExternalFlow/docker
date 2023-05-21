import os
import datetime
import sys
from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
import plotly.express as pu
import pandas as pd
import dash_uploader as du
import logging  # Add this line

import base64
import uuid

UPLOAD_DIRECTORY = "/app/uploads"

debug = False if os.environ["DASH_DEBUG_MODE"] == "False" else True

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__)
# app = Dash(__name__)

server = app.server



du.configure_upload(app, UPLOAD_DIRECTORY)

# Initial file path and base64 encoded image
file_path = ""
test_base64 = ""

# #Path to temporary folder
# path = "/app/uploads"
# #Looks through all directories and finds the most recently modified one
# directories = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
# most_recent_directory = max(directories, key=lambda d: os.path.getmtime(os.path.join(path, d)))

# #Find the most recently modified file in the most recent directory
# files = [(f, os.path.getmtime(os.path.join(path, most_recent_directory, f))) for f in os.listdir(os.path.join(path, most_recent_directory)) if os.path.isfile(os.path.join(path, most_recent_directory, f))]
# most_recent_file = max(files, key=lambda f: f[1])[0]

# #Set the path to the most recently modified file in the most recent directory
# file_path = os.path.join(path, most_recent_directory, most_recent_file)

# #Image decoding
# test_base64 = base64.b64encode(open(file_path, 'rb').read()).decode('ascii')

# def upload_component(id):
#     return du.Upload(
#         id=id,
#         max_file_size=1000, #1000 Mb
#         filetypes=['png', 'jpg'],
#         upload_id=uuid.uuid1(),
#     )

# def get_app_layout():
#     return html.Div(
#     [
#         upload_component(id='dash-uploader'),
#         # html.Div(id='callback-output'),
#         # html.Img(id='callback-output',src='data:file_path;base64,{}'.format(test_base64)),
#         html.Img(id='callback-output', src='placeholder_image.png'),
#     ],
#     style={
#         'textAlign': 'center',
#         'width': '600px',
#         'padding': '10px',
#         'display': 'inline-block'
#     }
# )
    

app.layout = html.Div([
    du.Upload(id='upload'),
    html.H1(children=file_path, className="hello"),
    html.Img(id='uploaded-image')
])
# app.layout = get_app_layout
    # du.Upload(),
    # html.Div(id='output'),
    # html.H1(children=file_path,className="hello"),
    # html.Img(src='data:file_path;base64,{}'.format(test_base64)),

# Open a file to redirect the output
log_file = open("/app/output.log", "w")

@app.callback(
    Output('uploaded-image', 'src'),
    Output('uploaded-image', 'alt'),
    Output('uploaded-image', 'style'),
    Input('upload', 'isCompleted'),
    State('upload', 'fileNames'),
    State('upload', 'uploadId')
)
def update_uploaded_image(is_completed, filenames, upload_id):
    if is_completed and filenames and upload_id:
        # Get the latest uploaded file
        file_name = filenames[-1]
        file_path = os.path.join(UPLOAD_DIRECTORY, upload_id, file_name)
        # Image decoding
        test_base64 = base64.b64encode(open(file_path, 'rb').read()).decode('ascii')
        
        # Write the output to the log file
        print(file_path, file=log_file)
        log_file.flush()  # Ensure the output is written immediately

        return (
            'data:image/png;base64,{}'.format(test_base64),
            file_name,
            {'display': 'block'}
        )
    else:
        return '', '', {'display': 'none'}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8050", debug=debug)