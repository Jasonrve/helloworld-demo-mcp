FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

COPY pyproject.toml README.md ./
COPY src ./src

RUN pip install --no-cache-dir .

EXPOSE 3000

CMD ["helloworld-demo-mcp", "--transport", "streamable-http", "--host", "0.0.0.0", "--port", "3000"]
