# Use an official Python runtime as a parent image
FROM python:3.8

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /usr/src/crowcrows

# Copy entrypoint and requirements first (to leverage Docker cache)
COPY ./entrypoint.sh ./entrypoint.sh
COPY ./requirements.txt ./requirements.txt

# Copy the rest of the application
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Make entrypoint executable
RUN chmod +x ./entrypoint.sh

# Expose port
EXPOSE 8000

# Run entrypoint
#ENTRYPOINT ["./entrypoint.sh"]