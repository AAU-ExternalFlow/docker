### Build image
``docker image build -t externalflow:latest .``

### Start docker container
``docker container run -ti --rm -v $HOME/externalflow/uploads:/externalflow/uploads -p 8050:8050 -w /externalflow externalflow``

### Now go to http://127.0.0.1:8050/ or http://localhost:8050/