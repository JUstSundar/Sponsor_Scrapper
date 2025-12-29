# Use official Playwright base with dependencies preinstalled
FROM mcr.microsoft.com/playwright/python:v1.42.1-jammy

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Default port for Uvicorn
EXPOSE 10000

# Launch your FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
