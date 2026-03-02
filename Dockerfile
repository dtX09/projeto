FROM python:3.12-slim

WORKDIR /app

# Instalar dependências de sistema mínimas + suporte Tkinter
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-tk \
    && rm -rf /var/lib/apt/lists/*

# Copiar ficheiros de configuração de dependências
COPY requirements.txt requirements-dev.txt pyproject.toml ./ 

RUN pip install --upgrade pip && \
    pip install -r requirements-dev.txt -r requirements.txt

# Copiar o resto do código (para builds de CI)
COPY . .

# Comando por omissão: shell interativo (útil em desenvolvimento)
CMD ["bash"]

