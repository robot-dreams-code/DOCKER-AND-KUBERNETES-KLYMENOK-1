FROM python:3.12-slim-buster AS builder 

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port your application listens on (if it's a web app)
EXPOSE 8080

# Define environment variables (optional)
ENV NAME World

# Run your Python application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]