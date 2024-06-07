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

# Install psycopg2 and other dependencies
RUN apt-get update \
    && apt-get -y install libpq-dev gcc curl

# Install Python Packages
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -e .

HEALTHCHECK --interval=5m --timeout=3s \
            --start-period=45s --start-interval=2s \
            CMD curl -f http://localhost:${HEALTHCHECK_PORT}/healthcheck || exit 1

# Command to run the application
# CMD ["python", "app.py"]
CMD ["python", "./ronin/main.py"]

