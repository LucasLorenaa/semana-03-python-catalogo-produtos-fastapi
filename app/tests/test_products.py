
# ==================== TESTES CRUD ====================

def test_create_product(client):
    """Testa criação de um novo produto"""
    response = client.post("/products/", json={
        "name": "Notebook",
        "sku": "PROD-001",
        "price": 2999.99,
        "active": True
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Notebook"
    assert data["sku"] == "PROD-001"
    assert data["price"] == 2999.99
    assert data["active"] is True
    assert "id" in data

def test_create_product_with_minimum_fields(client):
    """Testa criação com apenas campos obrigatórios"""
    response = client.post("/products/", json={
        "name": "Mouse",
        "sku": "PROD-002",
        "price": 49.90
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Mouse"
    assert data["active"] is True  # Default value

def test_get_all_products(client):
    """Testa listagem de todos os produtos"""
    # Criar alguns produtos
    client.post("/products/", json={
        "name": "Teclado",
        "sku": "PROD-003",
        "price": 199.90
    })
    client.post("/products/", json={
        "name": "Monitor",
        "sku": "PROD-004",
        "price": 899.90
    })
    
    response = client.get("/products/")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert len(data["items"]) >= 2

def test_get_product_by_id(client):
    """Testa obtenção de um produto específico por ID"""
    # Criar um produto
    create_response = client.post("/products/", json={
        "name": "Webcam",
        "sku": "PROD-005",
        "price": 299.90
    })
    product_id = create_response.json()["id"]
    
    # Obter o produto
    response = client.get(f"/products/{product_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == product_id
    assert data["name"] == "Webcam"
    assert data["sku"] == "PROD-005"

def test_get_nonexistent_product(client):
    """Testa obtenção de um produto que não existe"""
    response = client.get("/products/9999")
    assert response.status_code == 404

def test_update_product(client):
    """Testa atualização de um produto"""
    # Criar um produto
    create_response = client.post("/products/", json={
        "name": "Headset",
        "sku": "PROD-006",
        "price": 159.90,
        "active": True
    })
    product_id = create_response.json()["id"]
    
    # Atualizar o produto
    response = client.put(f"/products/{product_id}", json={
        "name": "Headset Gamer",
        "price": 199.90,
        "active": False
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Headset Gamer"
    assert data["price"] == 199.90
    assert data["active"] is False
    assert data["sku"] == "PROD-006"  # SKU não deve mudar

def test_update_product_partial(client):
    """Testa atualização parcial de um produto"""
    # Criar um produto
    create_response = client.post("/products/", json={
        "name": "Mousepad",
        "sku": "PROD-007",
        "price": 49.90
    })
    product_id = create_response.json()["id"]
    
    # Atualizar apenas o preço
    response = client.put(f"/products/{product_id}", json={
        "price": 39.90
    })
    assert response.status_code == 200
    data = response.json()
    assert data["price"] == 39.90
    assert data["name"] == "Mousepad"  # Nome não deve mudar

def test_update_nonexistent_product(client):
    """Testa atualização de um produto que não existe"""
    response = client.put("/products/9999", json={
        "name": "Novo Nome"
    })
    assert response.status_code == 404

def test_delete_product(client):
    """Testa deleção de um produto"""
    # Criar um produto
    create_response = client.post("/products/", json={
        "name": "Hub USB",
        "sku": "PROD-008",
        "price": 79.90
    })
    product_id = create_response.json()["id"]
    
    # Deletar o produto
    response = client.delete(f"/products/{product_id}")
    assert response.status_code == 200
    
    # Verificar se foi deletado
    get_response = client.get(f"/products/{product_id}")
    assert get_response.status_code == 404

def test_delete_nonexistent_product(client):
    """Testa deleção de um produto que não existe"""
    response = client.delete("/products/9999")
    assert response.status_code == 404

# ==================== TESTES DE PAGINAÇÃO ====================

def test_get_products_with_pagination(client):
    """Testa paginação de produtos"""
    # Criar vários produtos
    for i in range(15):
        client.post("/products/", json={
            "name": f"Produto {i}",
            "sku": f"SKU-{i:03d}",
            "price": 99.90 + i
        })
    
    # Obter primeira página (padrão limit=10)
    response = client.get("/products/")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 10
    assert data["total"] >= 15

def test_get_products_with_custom_limit(client):
    """Testa paginação com limite customizado"""
    # Criar vários produtos
    for i in range(10):
        client.post("/products/", json={
            "name": f"Produto {i}",
            "sku": f"SKU-CUSTOM-{i:03d}",
            "price": 99.90
        })
    
    # Obter com limit=5
    response = client.get("/products/?limit=5")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) <= 5

def test_get_products_with_skip(client):
    """Testa paginação com skip"""
    # Criar produtos
    for i in range(3):
        client.post("/products/", json={
            "name": f"Produto Skip {i}",
            "sku": f"SKU-SKIP-{i:03d}",
            "price": 99.90
        })
    
    # Obter com skip=1
    response = client.get("/products/?skip=1&limit=100")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) >= 2

# ==================== TESTES DE VALIDAÇÃO ====================

def test_create_product_missing_required_field(client):
    """Testa criação sem campo obrigatório"""
    response = client.post("/products/", json={
        "name": "Produto Incompleto"
        # Faltam 'sku' e 'price'
    })
    assert response.status_code == 422

def test_create_product_invalid_price(client):
    """Testa criação com preço inválido (zero ou negativo)"""
    response = client.post("/products/", json={
        "name": "Produto Inválido",
        "sku": "PROD-INVALID",
        "price": -10
    })
    assert response.status_code == 422

def test_create_product_invalid_price_zero(client):
    """Testa criação com preço zero"""
    response = client.post("/products/", json={
        "name": "Produto Zero",
        "sku": "PROD-ZERO",
        "price": 0
    })
    assert response.status_code == 422

def test_product_name_max_length(client):
    """Testa validação de comprimento máximo do nome"""
    long_name = "A" * 121  # Máximo permitido é 120
    response = client.post("/products/", json={
        "name": long_name,
        "sku": "PROD-LONG",
        "price": 99.90
    })
    assert response.status_code == 422

def test_product_sku_max_length(client):
    """Testa validação de comprimento máximo do SKU"""
    long_sku = "SKU" + "A" * 48  # Máximo permitido é 50
    response = client.post("/products/", json={
        "name": "Produto SKU",
        "sku": long_sku,
        "price": 99.90
    })
    assert response.status_code == 422

# ==================== TESTES DE INTEGRIDADE ====================

def test_create_duplicate_sku(client):
    """Testa criação de produto com SKU duplicado"""
    # Criar primeiro produto
    client.post("/products/", json={
        "name": "Produto 1",
        "sku": "SKU-DUPLICATE",
        "price": 99.90
    })
    
    # Tentar criar com mesmo SKU
    response = client.post("/products/", json={
        "name": "Produto 2",
        "sku": "SKU-DUPLICATE",
        "price": 199.90
    })
    assert response.status_code == 400

def test_product_response_structure(client):
    """Testa estrutura da resposta de um produto"""
    response = client.post("/products/", json={
        "name": "Produto Estrutura",
        "sku": "PROD-STRUCT",
        "price": 99.90
    })
    data = response.json()
    
    # Verificar se todos os campos estão presentes
    assert "id" in data
    assert "name" in data
    assert "sku" in data
    assert "price" in data
    assert "active" in data

def test_get_products_with_min_price(client):
    """Testa filtro por preço mínimo"""
    # Criar produtos com diferentes preços
    for i in range(3):
        client.post("/products/", json={
            "name": f"Produto Preço {i}",
            "sku": f"SKU-PRICE-{i:03d}",
            "price": 100.0 + (i * 50)  # 100, 150, 200
        })
    
    # Buscar com min_price
    response = client.get("/products/?min_price=150")
    assert response.status_code == 200
    data = response.json()
    
    # Deve retornar apenas 2 produtos (150 e 200)
    assert data["total"] == 3  # Total de todos os produtos
    assert len(data["items"]) == 2
    assert all(p["price"] >= 150 for p in data["items"])


def test_create_product_duplicate_sku_returns_400(client):
    """Testa que SKU duplicado retorna 400"""
    # Criar primeiro produto
    response1 = client.post("/products/", json={
        "name": "Produto 1",
        "sku": "SKU-DUP",
        "price": 99.90
    })
    assert response1.status_code == 200
    
    # Tentar criar com mesmo SKU
    response2 = client.post("/products/", json={
        "name": "Produto 2",
        "sku": "SKU-DUP",
        "price": 199.90
    })
    assert response2.status_code == 400
    assert "SKU already exists" in response2.json().get("detail", "")


def test_get_products_empty(client):
    """Testa GET quando não há produtos"""
    response = client.get("/products/")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0
    assert data["items"] == []
    assert data["skip"] == 0
    assert data["limit"] == 10


def test_update_product_with_none_values(client):
    """Testa atualização parcial com valores None"""
    # Criar produto
    create_response = client.post("/products/", json={
        "name": "Produto Original",
        "sku": "SKU-UPDATE-NONE",
        "price": 100.0,
        "active": True
    })
    product_id = create_response.json()["id"]
    
    # Atualizar apenas um campo
    update_response = client.put(f"/products/{product_id}", json={
        "price": 150.0
    })
    assert update_response.status_code == 200
    
    # Verificar que o produto foi atualizado
    get_response = client.get(f"/products/{product_id}")
    assert get_response.status_code == 200
    data = get_response.json()
    assert data["price"] == 150.0
    assert data["name"] == "Produto Original"  # Não foi alterado


def test_list_products_with_limit_and_skip(client):
    """Testa paginação com limit e skip combinados"""
    # Criar 5 produtos
    for i in range(5):
        client.post("/products/", json={
            "name": f"Produto {i}",
            "sku": f"SKU-LIMIT-{i:03d}",
            "price": 100.0 + (i * 10)
        })
    
    # Pedir 2 produtos a partir do índice 1
    response = client.get("/products/?skip=1&limit=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 2
    assert data["skip"] == 1
    assert data["limit"] == 2
    assert data["total"] == 5


def test_product_inactive_flag(client):
    """Testa flag active do produto"""
    # Criar produto inativo
    response = client.post("/products/", json={
        "name": "Produto Inativo",
        "sku": "SKU-INACTIVE",
        "price": 100.0,
        "active": False
    })
    assert response.status_code == 200
    
    data = response.json()
    assert data["active"] == False
    assert data["name"] == "Produto Inativo"
    
    # Reativar
    product_id = data["id"]
    update_response = client.put(f"/products/{product_id}", json={
        "active": True
    })
    assert update_response.status_code == 200
    updated_data = update_response.json()
    assert updated_data["active"] == True
