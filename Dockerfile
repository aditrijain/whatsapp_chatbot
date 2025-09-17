# Base image with Python
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install ffmpeg system dependency
RUN apt-get update && apt-get install -y ffmpeg

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code
COPY . .

# Expose the port your FastAPI app will run on
EXPOSE 8000

# Command to run the FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
