# Use a imagem oficial do Python
FROM python:3.9-slim

# Definir o diretório de trabalho
WORKDIR /app

# Copiar os arquivos de requisitos
COPY requirements.txt .

# Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante do código
COPY . .

# Comando para executar o agente
CMD ["python", "main.py"]
