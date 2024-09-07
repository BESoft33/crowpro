# Use an official Python runtime as a parent image
FROM python:3.8

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /usr/src/crowcrows

# Copy the requirements file and install dependencies
COPY ./requirements.txt ./requirements.txt

RUN python -m pip install --upgrade pip
RUN python -m pip install --no-cache-dir -r requirements.txt
RUN python manage.py makemigrations
RUN python manage.py migrate

# Copy the rest of the application code to the working directory
COPY crowpro/ .

# Copy the entrypoint script into the container
COPY entrypoint.sh ./entrypoint.sh

# Ensure the entrypoint script is executable
RUN chmod +x ./entrypoint.sh

# Expose port 8000 to the outside world
EXPOSE 8000

# Set the entrypoint script as the container's entrypoint
ENTRYPOINT ["./entrypoint.sh"]
