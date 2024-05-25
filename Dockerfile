# Use the official Python image from the Docker Hub
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY main.py .
COPY capstoneClassification.pkl .
COPY sample_userinput.csv .

# Set environment variables for your sensitive information
# Make sure you have your .env file in the same directory as your Dockerfile
COPY .env .
RUN pip install python-dotenv

# Expose the port FastAPI runs on
EXPOSE 8000

# Run the FastAPI application using uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
