# Use Python 3.11 slim image
FROM python:3.11-slim-bookworm

# Set working directory
WORKDIR /app

# Install system dependencies required by TensorFlow and other packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (Cache optimization)
COPY requirements.txt /app/

# Copy pre-downloaded Python packages
COPY deps /deps

# Install using local wheels (FAST, NO INTERNET)
RUN python -m pip install --upgrade pip && \
    pip install --no-index --find-links=/deps -r requirements.txt

# Copy your full project
COPY . /app

# Expose Streamlit default port
EXPOSE 8501

# Run Streamlit
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
