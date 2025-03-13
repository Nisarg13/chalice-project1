# Stage 1: Install dependencies in a temporary container
FROM python:3.12-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Create the final minimal image
FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY . .

EXPOSE 8000
CMD ["chalice", "local", "--host", "0.0.0.0", "--port", "8000"]
