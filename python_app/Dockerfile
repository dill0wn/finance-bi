# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

COPY . /app

# Set up basic shell settings
COPY bashrc /root/.bashrc

# Install psycopg2 dependencies
RUN apt-get update \
    && apt-get -y install libpq-dev gcc

# Install Python Packages
RUN pip install --no-cache-dir -r requirements.txt

# Command to run the application
# CMD ["python", "app.py"]
CMD ["tail", "-f", "/dev/null"]

