from fastapi import FastAPI

# Inicializa o aplicativo FastAPI com algumas informações básicas
app = FastAPI(
    title="Meu Projeto API",
    description="Backend estruturado com FastAPI, SQLAlchemy e MySQL",
    version="0.1.0",
)

# Cria uma rota básica de teste para saber se está tudo funcionando
@app.get("/documentos")
async def root():
    return {
        "status": "sucesso",
        "mensagem": "A API está rodando perfeitamente!"
    }
# booommmm
