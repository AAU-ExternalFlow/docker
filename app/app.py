import os
import datetime
from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import dash_uploader as du
import base64

UPLOAD_DIRECTORY = "/app/uploads"

debug = False if os.environ["DASH_DEBUG_MODE"] == "False" else True

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__)
# app = Dash(__name__)

server = app.server



du.configure_upload(app, UPLOAD_DIRECTORY)


#Path to temporary folder
path = "/app/uploads"
#Looks through all directories and finds the most recently modified one
directories = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
most_recent_directory = max(directories, key=lambda d: os.path.getmtime(os.path.join(path, d)))

#Find the most recently modified file in the most recent directory
files = [(f, os.path.getmtime(os.path.join(path, most_recent_directory, f))) for f in os.listdir(os.path.join(path, most_recent_directory)) if os.path.isfile(os.path.join(path, most_recent_directory, f))]
most_recent_file = max(files, key=lambda f: f[1])[0]

#Set the path to the most recently modified file in the most recent directory
file_path = os.path.join(path, most_recent_directory, most_recent_file)

#Image decoding
test_base64 = base64.b64encode(open(file_path, 'rb').read()).decode('ascii')

app.layout = html.Div([
    du.Upload(),
    # html.Div(id='output'),
    html.H1(children=file_path,className="hello"),
    html.Img(src='data:file_path;base64,{}'.format(test_base64)),
])



if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8050", debug=debug)