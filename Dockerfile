FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY pyproject.toml README.md ./

# Create an empty src package to allow installation
RUN mkdir src && touch src/__init__.py

# Install the package in development mode
RUN pip install -e .

# Copy application code
COPY . .

# Run Flask app using waitress with debug logging
ENV PYTHONUNBUFFERED=1
CMD ["python", "-m", "src.server"]
