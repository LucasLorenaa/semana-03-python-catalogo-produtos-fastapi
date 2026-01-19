# Catálogo de Produtos - FastAPI

API de catálogo de produtos com FastAPI e SQLite, organizada em camadas de gateway (schemas/routers) e storage (DB/CRUD). Tests em pytest cobrem CRUD, validações, paginação e integridade.

## 🚀 Como rodar

1) Criar e ativar venv
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
```

2) Instalar dependências
```bash
pip install -r requirements.txt
```

3) Subir backend
```bash
python -m uvicorn app.main:app --reload --port 8000
```
Swagger: http://localhost:8000/docs

4) (Opcional) Servir frontend estático
```bash
cd frontend
python -m http.server 3000
```
Altere `frontend` para apontar para o backend se usar outra porta.

5) Rodar testes
```bash
.venv\Scripts\python.exe -m pytest app/tests/test_products.py -v --tb=short
```

## 📂 Estrutura atual

```
app/
├── main.py                  # Monta FastAPI e CORS
├── gateway/
│   ├── schemas.py           # Modelos Pydantic
│   └── routers/
│       └── products.py      # Rotas /products
├── storage/
│   ├── database.py          # Engine + SessionLocal
│   ├── models.py            # Modelos SQLAlchemy
│   └── crud.py              # Operações de banco
└── tests/
    └── test_products.py     # 26 testes de API
frontend/                    # HTML/CSS/JS estático
requirements.txt
README.md
```

## 🔌 Endpoints principais

- GET `/products` → lista paginada com `skip`, `limit` e `min_price`
- GET `/products/{id}` → detalhe
- POST `/products` → cria (campos: name, sku, price, active)
- PUT `/products/{id}` → atualiza parcial ou total
- DELETE `/products/{id}` → remove

### Exemplo de POST
```json
{
  "name": "Notebook",
  "sku": "PROD-001",
  "price": 2999.99,
  "active": true
}
```

## 🧪 Notas de qualidade

- Testes: 26 passando (pytest) cobrindo CRUD, validações, paginação e SKU duplicado.
- Banco: `products.db` é criado automaticamente; para resetar, delete o arquivo antes de rodar os testes ou o servidor.
- Aviso de resources: em execuções com cobertura podem surgir avisos de conexão SQLite não fechada; as sessões já fecham via dependency `get_db`.

## 🛠️ Tecnologias

- FastAPI, SQLAlchemy, Pydantic, SQLite
- Pytest para testes
