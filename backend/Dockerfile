# Usa uma imagem oficial do Python
FROM python:3.14.4

# Define a pasta de trabalho dentro do contêiner
WORKDIR /app

# Copia o arquivo dev.txt da sua pasta para o contêiner, já renomeando para requirements.txt
COPY requirements/dev.txt ./requirements.txt

# Instala as dependências usando o arquivo que acabou de ser copiado
RUN pip install --no-cache-dir -r requirements.txt

# Copia o resto do código
COPY . .

# Expõe a porta do FastAPI
EXPOSE 8000

# Comando para rodar a API usando o servidor
CMD ["fastapi", "dev", "src/main.py", "--port", "8000", "--host", "0.0.0.0"]