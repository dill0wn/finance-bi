# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Set up basic shell settings
COPY bashrc /root/.bashrc

RUN apt-get update

# Install psycopg2 and other dependencies
RUN apt-get -y install libpq-dev gcc curl

# Install Spark Dependencies
RUN apt-get -y install default-jre-headless


# Install Python Packages
COPY setup.py .
RUN pip install -e .

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

HEALTHCHECK --interval=5m --timeout=3s \
            --start-period=45s --start-interval=2s \
            CMD curl -f http://localhost:${RONIN_HEALTH_PORT}/healthcheck || exit 1

# Command to run the application
# CMD ["python", "app.py"]
CMD ["python", "./ronin/main.py"]

