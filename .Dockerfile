FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/var/input_data && \
    mkdir -p /app/var/extracted_archives && \
    mkdir -p /app/var/vector_db && \
    mkdir -p /app/var/generated_docs && \
    mkdir -p /app/var/generated_answers && \
    mkdir -p /app/var/log

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
CMD curl --fail http://localhost:8501/_stcore/health || exit 1

CMD [
    "streamlit",
    "run",
    "codescope_ai/app/ui/streamlit_app.py",
    "--server.address=0.0.0.0",
    "--server.port=8501"
]
