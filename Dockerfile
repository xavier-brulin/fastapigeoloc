# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /code

# Copy the requirements file into the container at /app
COPY ./requirements.txt /code/requirements.txt

# Install any dependencies
RUN pip install --no-cache-dir -r /code/requirements.txt

# Copy the rest of the working directory contents into the container at /app
COPY ./app /code/app
COPY ./static /code/static

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable for Uvicorn
ENV HOST 0.0.0.0
ENV PORT 80

# Run the FastAPI app with Uvicorn
CMD ["fastapi", "run", "app/main.py", "--reload", "--host", "0.0.0.0", "--port", "80"]

