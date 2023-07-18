### Build image
docker image build -t externalflow:latest .

### (optional) Build image with Python cached
docker image build --build-arg CACHEBUST=$(powershell -Command "[System.DateTimeOffset]::UtcNow.ToUnixTimeSeconds()") -t externalflow:latest .

### Start docker container
docker container run -ti --rm -v $HOME/externalflow/uploads:/externalflow/uploads -p 8050:8050 externalflow