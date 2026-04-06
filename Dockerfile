FROM python:3.10-slim

WORKDIR /app

# Copy requirements first to leverage Docker layer caching.
# If requirements.txt hasn't changed, pip install is skipped on rebuild.
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application source code
COPY . .

# Document the port the application listens on
EXPOSE 8000

# PORT is set here; Render overrides it at runtime
ENV PORT=8000

CMD ["sh", "-c", "uvicorn backend.main:app --host 0.0.0.0 --port $PORT"]