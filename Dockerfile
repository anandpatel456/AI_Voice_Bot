FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    portaudio19-dev \
    libasound2-dev \
    libportaudio2 \
    libportaudiocpp0 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy Python requirements first (for caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy your app code into the container
COPY . .

# Expose the default Streamlit port
EXPOSE 8501

# Health check (optional)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Set environment variables (avoid streamlit warnings)
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Run Streamlit
CMD ["streamlit", "run", "Home.py", "--server.address=0.0.0.0", "--server.port=8501", "--server.headless=true"]
