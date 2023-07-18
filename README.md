### Build image
``docker image build -t externalflow:latest .``

### Start docker container
``docker container run -ti --rm -v $HOME/externalflow/uploads:/externalflow/uploads -p 8050:8050 -w /externalflow externalflow``

### Now within the docker container start the web app:
``python3 dashWebApp/app.py``

### Now go to http://127.0.0.1:8050/