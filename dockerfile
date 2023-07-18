FROM ubuntu:focal

ENV DEBIAN_FRONTEND=noninteractive

ENV TZ=Europe/Copenhagen
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install essentials
RUN apt-get update && apt-get install -y \
		sudo \
		wget \
		nano \
		git \
		build-essential \
		software-properties-common

# Install python packages
RUN apt-get update && apt-get install -y \
		python3.10 \
		python3-pip 
		
RUN pip install --upgrade pip

# Download openfoam
RUN wget -q -O - https://dl.openfoam.com/add-debian-repo.sh | sudo bash ;\
    apt-get install -y openfoam-default ;\
    rm -rf /var/lib/apt/lists/*

# Add new user "extflow"
RUN useradd --user-group --create-home --shell /bin/bash extflow ;\
	echo "extflow ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Source openfoam and fix docker mpi
RUN echo "source /usr/lib/openfoam/openfoam/etc/bashrc" >> ~extflow/.bashrc ;\
   echo "export OMPI_MCA_btl_vader_single_copy_mechanism=none" >> ~extflow/.bashrc

# Change environmental variables to make sure $WM_PROJECT_USER_DIR is outside of the container
RUN sed -i '/export WM_PROJECT_USER_DIR=/cexport WM_PROJECT_USER_DIR="/externalflow/extflow-$WM_PROJECT_VERSION"' /usr/lib/openfoam/openfoam/etc/bashrc

# Make sure to always run the following commands (no cache)
ADD "https://www.random.org/cgi-bin/randbyte?nbytes=10&format=h" skipcach

# Create working directory
RUN mkdir /externalflow/

# Download dash web application
RUN git clone https://github.com/AAU-ExternalFlow/dashWebApp.git
RUN mv dashWebApp /externalflow/dashWebApp

# Download image processing Python code
RUN git clone https://github.com/AAU-ExternalFlow/imageProcessing.git
RUN mv imageProcessing /externalflow/imageProcessing

# Install Python packages
RUN python3 -m pip install --ignore-installed -r externalflow/dashWebApp/requirements.txt
RUN python3 -m pip install --ignore-installed -r externalflow/imageProcessing/requirements.txt

# Set working dir
WORKDIR /externalflow

# Change user to "extflow"
USER extflow

# Start the Dash web app automatically when the docker container is started
# EXPOSE 8050
# CMD ["python3", "dashWebApp/app.py"]