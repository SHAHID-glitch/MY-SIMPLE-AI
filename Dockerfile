FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements_hf.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements_hf.txt

# Copy entire application
COPY . .

# Expose port (HF Spaces uses 7860)
EXPOSE 7860

# Set environment variables
ENV FLASK_ENV=production
ENV PORT=7860

# Command to run the application
CMD ["python", "app.py"]
