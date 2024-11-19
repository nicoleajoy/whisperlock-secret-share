# Specify the base container image
FROM python:3.12.5-alpine3.20

# Copy the necessary files from local to container
COPY . /app/

# Change working directories
WORKDIR /app

# Install dependencies
RUN pip install -r requirements.txt

# By default, Flask exposes port 5000, but we should make that explicit
EXPOSE 5000

# Execute the command that starts the application
CMD ["python", "app.py"]