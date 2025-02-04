# Use the official Python image.
FROM python:3.10-slim

# Set the working directory.
WORKDIR /app

# Copy dependency definitions.
COPY requirements.txt .

# Install dependencies.
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the application.
COPY . .

# Expose the port the app runs on.
EXPOSE 5000

# Run the application.
CMD ["python", "app/main.py"]