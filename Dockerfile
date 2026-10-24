FROM python:3.9-slim

# Create working folder and install dependencies
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application files from the service directory into the image
COPY service/ ./service/

# Switch to a non-root user
RUN useradd --uid 1000 theia && chown -R theia /app
USER theia

# Expose port and run the service
EXPOSE 8080
CMD ["gunicorn", "--bind=0.0.0.0:8080", "--log-level=info", "service:app"]
