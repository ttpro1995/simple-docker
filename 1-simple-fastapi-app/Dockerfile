# Use the official Python base image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .


# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the working directory
COPY fastapi_app.py .

# Expose the port that the FastAPI application will be running on
EXPOSE 8000

# Set the entrypoint command to run the FastAPI application
CMD ["uvicorn", "fastapi_app:app", "--host", "0.0.0.0", "--port", "8000"]