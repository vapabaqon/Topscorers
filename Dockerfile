# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy your Python script into the container
COPY services ./services
COPY utils ./utils
COPY config.py ./
COPY main.py ./
COPY credentials.json ./
COPY logs ./logs

# Install the required libraries
RUN pip install certifi==2023.7.22 charset-normalizer==3.3.0 idna==3.4 requests==2.31.0 urllib3==2.0.6

# Run the script
CMD [ "python", "./main.py"]