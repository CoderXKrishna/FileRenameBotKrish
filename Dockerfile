FROM python:3.8-slim-buster

# Create app directory and set it as the working directory
RUN mkdir -p /app && chown -R $USER:$USER /app
WORKDIR /app

# Install required system packages
RUN apt-get update && apt-get install -y \
        git \
        ffmpeg \
        ca-certificates \
        curl \
        && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV DEBIAN_FRONTEND noninteractive
ENV TZ=Asia/Kolkata

# Install python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app
