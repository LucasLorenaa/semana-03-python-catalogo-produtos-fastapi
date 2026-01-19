// Configuração da API
const API_BASE_URL = 'http://localhost:5000/products';

// Classe para gerenciar requisições à API
class ProductAPI {
    static async getProducts(skip = 0, limit = 10, minPrice = null) {
        try {
            let url = `${API_BASE_URL}?skip=${skip}&limit=${limit}`;
            if (minPrice !== null && minPrice > 0) {
                url += `&min_price=${minPrice}`;
            }
            
            const response = await fetch(url);
            if (!response.ok) {
                throw new Error(`Erro ao buscar produtos`);
            }
            return await response.json();
        } catch (error) {
            console.error('Erro na API:', error);
            throw error;
        }
    }

    static async getProductById(id) {
        try {
            const response = await fetch(`${API_BASE_URL}/${id}`);
            if (!response.ok) {
                throw new Error(`Erro ao buscar produto: ${response.statusText}`);
            }
            return await response.json();
        } catch (error) {
            console.error('Erro na API:', error);
            throw error;
        }
    }

    static async createProduct(productData) {
        try {
            console.log('Enviando dados:', productData);
            const response = await fetch(API_BASE_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(productData)
            });
            
            console.log('Status da resposta:', response.status);
            
            if (!response.ok) {
                let errorMessage = `Erro ${response.status}: ${response.statusText}`;
                try {
                    const errorData = await response.json();
                    errorMessage = errorData.detail || errorMessage;
                } catch (e) {
                    // Se não conseguir parsear JSON, usa o statusText
                }
                throw new Error(errorMessage);
            }
            const data = await response.json();
            console.log('Produto criado:', data);
            return data;
        } catch (error) {
            console.error('Erro ao criar produto:', error);
            throw error;
        }
    }

    static async updateProduct(id, productData) {
        try {
            const response = await fetch(`${API_BASE_URL}/${id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(productData)
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || `Erro ao atualizar produto: ${response.statusText}`);
            }
            return await response.json();
        } catch (error) {
            console.error('Erro na API:', error);
            throw error;
        }
    }

    static async deleteProduct(id) {
        try {
            const response = await fetch(`${API_BASE_URL}/${id}`, {
                method: 'DELETE'
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || `Erro ao deletar produto: ${response.statusText}`);
            }
            return await response.json();
        } catch (error) {
            console.error('Erro na API:', error);
            throw error;
        }
    }
}
