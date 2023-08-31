# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory within the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app/

# Set environment variables (if needed)
ENV SECRET_KEY="83knnjh23kjh490923894832423488333jh"
ENV ALGORITHM="HS256"
ENV ACCESS_TOKEN_EXPIRE_MINUTES=30

# Expose the port the app runs on
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
