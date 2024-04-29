# Use an official Python runtime as a parent image
FROM python:3.9.4

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY requirements.txt /app/


COPY . /app/
# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000 to allow external connections to this service
EXPOSE 8000

# Define the command to run the Django development server
CMD ["python", "manage.py", "runserver", "127.0.0.1:8000"]
