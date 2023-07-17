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
WORKDIR /externalflow/dashWebApp

ENV DASH_DEBUG_MODE False
EXPOSE 8050
CMD ["gunicorn", "-b", "0.0.0.0:8050", "--reload", "app:server"]


# # download openfoam
# RUN wget -q -O - https://dl.openfoam.com/add-debian-repo.sh | sudo bash ;\
#     apt-get install -y openfoam-default ;\
#     rm -rf /var/lib/apt/lists/*

# # add user "foam"
# RUN useradd --user-group --create-home --shell /bin/bash foam ;\
# 	echo "foam ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
    
# # source openfoam and fix docker mpi
# RUN echo "source /usr/lib/openfoam/openfoam/etc/bashrc" >> ~foam/.bashrc ;\
#    echo "export OMPI_MCA_btl_vader_single_copy_mechanism=none" >> ~foam/.bashrc

# # change environmental variables to make sure $WM_PROJECT_USER_DIR is outside of the container
# RUN sed -i '/export WM_PROJECT_USER_DIR=/cexport WM_PROJECT_USER_DIR="/data/foam-$WM_PROJECT_VERSION"' /usr/lib/openfoam/openfoam/etc/bashrc

# # change user to "foam"
# USER foam


