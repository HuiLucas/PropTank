# Use the official Python image from the Docker Hub
FROM python:3.9

# Set the working directory in the container to /app
WORKDIR /app

# Copy all contents from the current directory to /app in the container
COPY . /app

# Install any dependencies your Python application needs
RUN pip install -r Requirements.txt  # If you have a requirements.txt file

# Set the entry point to your main Python file
CMD ["python", "Optimization.py"]