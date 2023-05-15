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



# data = pd.DataFrame(
#     {
#         "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
#         "Amount": [4, 1, 2, 2, 4, 5],
#         "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"],
#     }
# )

# graph = px.bar(data, x="Fruit", y="Amount", color="City", barmode="group")

# 1) configure the upload folder
# du.configure_upload(app, r"C:\tmp\Uploads")
du.configure_upload(app, UPLOAD_DIRECTORY)

# app.layout = html.Div([
#     du.Upload(
#         id='dash-uploader',
#     ),
#     html.Div(id='output')
#     # html.Div(id='dash-uploader'),
# ])

img_element = html.Img(src=f"/uploads/{newest_folder}/{newest_file}")

app.layout = html.Div([
    du.Upload(),
    html.Div(id='output')
])


#Her forsøges at finde den nyeste uploaded fil i tmp/uploads
@app.callback(Output('output', 'children'), [Input('upload', 'contents')])
def display_image(contents):
    if contents is not None:
        # get file extension
        file_extension = contents.split(";")[0].split("/")[-1]
        # generate a unique file name
        file_name = f"upload_{uuid.uuid4().hex}.{file_extension}"
        # save the file to the upload directory
        with open(os.path.join(UPLOAD_DIRECTORY, file_name), "wb") as f:
            f.write(base64.b64decode(contents.split(",")[1]))
        # get the name of the newest folder in the upload directory
        newest_folder = max(os.listdir(UPLOAD_DIRECTORY), key=os.path.getmtime)
        # get the name of the newest .jpg file inside the newest folder
        newest_file = max(os.listdir(os.path.join(UPLOAD_DIRECTORY, newest_folder)), key=os.path.getmtime)
        # check if the newest file is a .jpg
        if newest_file.endswith(".jpg"):
            # create and return img element with the newest file as src attribute
            return html.Img(src=f"/uploads/{newest_folder}/{newest_file}")
        else:
            return html.Div()
    else:
        return html.Div()

# def parse_contents(contents, filename, date):
#     return html.Div([
#         html.H5(filename),
#         html.H6(datetime.datetime.fromtimestamp(date)),

#         # HTML images accept base64 encoded strings in the same format
#         # that is supplied by the upload
#         html.Img(src=contents),
#         html.Hr(),
#         html.Div('Raw Content'),
#         html.Pre(contents[0:200] + '...', style={
#             'whiteSpace': 'pre-wrap',
#             'wordBreak': 'break-all'
#         })
#     ])

# @app.callback(Output('output-image-upload', 'children'),
#               Input('upload-image', 'contents'),
#               State('upload-image', 'filename'),
#               State('upload-image', 'last_modified'))
# def update_output(list_of_contents, list_of_names, list_of_dates):
#     if list_of_contents is not None:
#         children = [
#             parse_contents(c, n, d) for c, n, d in
#             zip(list_of_contents, list_of_names, list_of_dates)]
#         return children


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8050", debug=debug)