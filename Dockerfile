# ✅ Use official Playwright base image with Python
FROM mcr.microsoft.com/playwright/python:v1.42.1-focal

# Set working directory
WORKDIR /app

# Copy dependency files first
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the rest of your app
COPY . .

# Set environment variable so Playwright knows not to download again
ENV PLAYWRIGHT_BROWSERS_PATH=0

# Install browsers (important for production)
RUN playwright install --with-deps

# Expose the port (same as FastAPI)
EXPOSE 10000

# Start the FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
