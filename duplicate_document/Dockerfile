# Use the official Python base image
FROM python:3.8-slim

# Set the working directory
WORKDIR /app

# Copy the script and requirements.txt (if you have one) into the container
COPY duplicate_document.py /app/
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Run duplicate_document.py when the container launches
CMD ["python", "duplicate_document.py"]
