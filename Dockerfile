# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set environment variables to prevent Python from writing pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install Poetry
RUN pip install poetry

# Set the working directory in the container
WORKDIR /src

# Copy the pyproject.toml and poetry.lock files
COPY src/pyproject.toml src/poetry.lock /src/

# Install the dependencies
RUN poetry install --no-root

# Copy the rest of the application code
COPY src/ /src/

# Expose the port that the app runs on
EXPOSE 5000

ENTRYPOINT ["poetry", "run"]
