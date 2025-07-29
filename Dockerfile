FROM python:3.13-slim

WORKDIR /app
COPY . .

# Install system packages including PortAudio
RUN apt-get update \
  && apt-get install -y build-essential portaudio19-dev \
  && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8501
CMD ["streamlit", "run", "Home.py", "--server.address", "0.0.0.0", "--server.port", "8501"]
