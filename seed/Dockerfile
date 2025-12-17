FROM python:3.11-slim

# Install GDAL/OGR for shapefile processing
RUN apt-get update && apt-get install -y \
    gdal-bin \
    libgdal-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir psycopg2-binary

# Create working directory
WORKDIR /seed

# Copy seed script
COPY load_shapefiles.py /seed/
RUN chmod +x /seed/load_shapefiles.py

# The data directory will be mounted as a volume
# VOLUME /seed/data

CMD ["python", "/seed/load_shapefiles.py"]
