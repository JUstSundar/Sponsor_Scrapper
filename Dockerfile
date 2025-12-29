# ✅ Use the official Playwright image from GitHub Container Registry
FROM ghcr.io/microsoft/playwright/python:v1.42.1-jammy

# Set the working directory
WORKDIR /app

# Copy dependencies
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy all files into the container
COPY . .

# Install browsers
RUN playwright install --with-deps

# Expose FastAPI's default port
EXPOSE 10000

# Run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
