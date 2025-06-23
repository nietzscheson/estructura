FROM public.ecr.aws/docker/library/python:3.11-slim-bookworm AS builder

ENV PYTHONUNBUFFERED=1
ENV POETRY_HOME=/etc/poetry
ENV PATH="${POETRY_HOME}/bin:${PATH}"
ENV WORKDIR=/build

WORKDIR ${WORKDIR}

# Instalar dependencias del sistema mínimas
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    poppler-utils \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

# Instalar poetry
RUN pip install "poetry==1.7.0" --no-cache-dir

# Copiar solo los archivos necesarios para instalar dependencias
COPY pyproject.toml poetry.lock ./

# Configurar poetry y resolver dependencias en una capa separada
RUN poetry config virtualenvs.create false \
 && poetry install --no-root --no-dev

# Copiar dependencias necesarias para Lambda
RUN pip install awslambdaric --no-cache-dir


# --- Runtime final ---
FROM public.ecr.aws/docker/library/python:3.11-slim-bookworm AS runtime

ENV PYTHONUNBUFFERED=1
ENV PORT=8000
ENV WORKDIR=/var/task
WORKDIR ${WORKDIR}

# Copiar runtime adapter
COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:0.9.0 /lambda-adapter /opt/extensions/lambda-adapter

# Copiar dependencias desde builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

RUN apt-get update && apt-get install -y --no-install-recommends \
    poppler-utils \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copiar código de aplicación
COPY . .

# (Opcional) Healthcheck si aplica para local testing
HEALTHCHECK CMD curl --fail http://localhost:8000/health || exit 1
