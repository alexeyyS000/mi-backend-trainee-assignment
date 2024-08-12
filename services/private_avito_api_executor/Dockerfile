FROM mcr.microsoft.com/playwright/python:v1.22.0-focal

WORKDIR /app

# Install poetry
RUN apt update && apt install -y python3 python3-pip python3-venv curl
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH /root/.local/bin:$PATH

COPY poetry.lock .
COPY pyproject.toml .

# Install Python dependecies
RUN poetry install --no-dev

# Build gRPC services
COPY protobufs /app/protobufs
RUN poetry run python -m grpc_tools.protoc \
    -I /app/protobufs \
    --python_out=. \
     --grpc_python_out=. \
    /app/protobufs/services/private_avito_api_executor/private_avito_api_executor.proto

# Install Playwright
RUN poetry run playwright install

COPY . .