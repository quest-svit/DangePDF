#Deriving the latest base image
FROM python:latest

#Labels as key value pair
LABEL Maintainer="tanmay.dange"

# Download Package Information
RUN apt-get update -y

# Install Tkinter
RUN apt-get install python3-tk -y

# Upgrading PIP
RUN pip install --upgrade pip

# Any working directory can be chosen as per choice like '/' or '/home' etc
WORKDIR /usr/app/

#to COPY the remote file at working directory in container
COPY . ./

# Install Python libraries
RUN pip install -r requirements.txt

# CMD instruction should be used to run the software
CMD [ "python", "./pdfViewer.py"]