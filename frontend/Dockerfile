# Usa uma imagem oficial do Node.js
FROM node:22.23.2

WORKDIR /app

# Copia apenas os arquivos de dependência primeiro (para usar o cache do Docker)
COPY package*.json ./
RUN npm install

# Copia o restante do código do frontend
COPY . .

# Expõe a porta padrão do Vite
EXPOSE 5173

# Roda o servidor de desenvolvimento e permite acesso externo (--host)
CMD ["npm", "run", "dev", "--", "--host"]