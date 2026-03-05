FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt requirements-dev.txt pyproject.toml ./

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt -r requirements-dev.txt

COPY . .

CMD ["python", "main.py"]