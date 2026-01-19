
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .gateway.routers import products
from .storage.database import init_db

app = FastAPI(title="Catálogo de Produtos API")

# Configurar CORS PRIMEIRO, antes de tudo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products.router)


@app.on_event("startup")
def on_startup():
    """Garante que a tabela seja criada antes de receber requisições."""
    init_db()
