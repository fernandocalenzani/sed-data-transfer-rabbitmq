# Use the official Python 3.10 image as the base
FROM python:3.10

# Set the working directory inside the container
WORKDIR /firmware-producer

# Copy the requirements file to the working directory
COPY requirements.txt /firmware-producer/

# Update and upgrade system packages
RUN apt-get update && \
  apt-get upgrade -y && \
  # Remove unnecessary caches to reduce image size
  rm -rf /var/lib/apt/lists/*

# Installing curl packages
RUN apt-get update && \
  apt-get install -y curl

# Upgrade pip to the latest version
RUN python -m pip install --upgrade pip

# Install Python dependencies from the requirements.txt file
RUN pip install --no-cache-dir -r requirements.txt

# Install the libgl1-mesa-glx dependency required by OpenCV
RUN apt-get update && \
  apt-get install -y libgl1-mesa-glx

# Copy the entire local directory contents into the container's working directory
COPY . /firmware-producer/

# Specify the default command to be executed when the container is started
CMD ["python", "__main__.py"]
