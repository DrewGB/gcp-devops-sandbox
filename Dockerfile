# Tell docker to use Python 3.12 slim image
FROM python:3.12-slim

# Set working directory for the container
WORKDIR /app

#Copy the Requirments over
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY ./app ./app

# Expose the port the API will run on
EXPOSE 8000

# Run the app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]