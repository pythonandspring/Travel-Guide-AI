# Use Python 3.13.1 Slim as the base image
FROM python:3.12.6-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV VIRTUAL_ENV=/app/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install system dependencies (including sqlite3 and other dependencies)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    libportaudio2 \
    portaudio19-dev \
    libsndfile1 \
    gcc \
    python3-dev \
    libmariadb-dev-compat \
    libmariadb-dev \
    libffi-dev \
    pkg-config \
    bash \
    curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Create a virtual environment
RUN python3 -m venv $VIRTUAL_ENV

# Upgrade pip and setuptools
RUN pip install --no-cache-dir --upgrade pip setuptools

# Copy requirements.txt to the container (before application code to cache dependencies)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt -v

# Copy the rest of the project into the container
COPY . .

# Run Django migrations and data population scripts during container runtime instead of during build
RUN python manage.py makemigrations && \
    python manage.py migrate && \

    python -u "/app/dummy_data/scripts/cust_script_for_all.py" && \
    python -u "/app/dummy_data/scripts/guide_script_for_all.py" && \
    python -u "/app/dummy_data/scripts/hotel_script_for_all.py" && \
    python -u "/app/dummy_data/scripts/place_script_for_all.py" && \
    python -u "/app/dummy_data/scripts/hotel_rooms_script_for_all.py" && \
    python -u "/app/dummy_data/scripts/doctor_script_for_all.py" && \
    python -u "/app/dummy_data/scripts/profile_script_for_all.py" && \
    python -u "/app/front_images.py" && \
    python -u "/app/place_image.py" && \
    python -u "/app/hotel_images.py"

# Expose the port the app will run on
EXPOSE 8000

# Default command to run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]