# Example: Using requirements.txt
FROM python:3.13-alpine

WORKDIR /app

# Copy only the requirements file first
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Now copy the rest of the application code
COPY main.py .

# Define how to run the application (example)
CMD ["python", "main.py"]
