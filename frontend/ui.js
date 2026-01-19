// Classe para gerenciar a UI
class UI {
    static showLoading(show = true) {
        const loading = document.getElementById('loading');
        if (show) {
            loading.classList.add('active');
        } else {
            loading.classList.remove('active');
        }
    }

    static showError(message) {
        const errorDiv = document.getElementById('errorMessage');
        errorDiv.textContent = message;
        errorDiv.classList.add('show');
        setTimeout(() => {
            errorDiv.classList.remove('show');
        }, 5000);
    }

    static showSuccess(message) {
        // Criar ou usar elemento de sucesso
        let successDiv = document.getElementById('successMessage');
        if (!successDiv) {
            successDiv = document.createElement('div');
            successDiv.id = 'successMessage';
            successDiv.className = 'success-message';
            document.body.insertBefore(successDiv, document.body.firstChild);
        }
        successDiv.textContent = message;
        successDiv.classList.add('show');
        setTimeout(() => {
            successDiv.classList.remove('show');
        }, 3000);
    }

    static openModal() {
        const modal = document.getElementById('modal');
        modal.classList.add('show');
    }

    static closeModal() {
        const modal = document.getElementById('modal');
        modal.classList.remove('show');
        document.getElementById('productForm').reset();
        document.getElementById('productId').value = '';
        document.getElementById('modalTitle').textContent = 'Novo Produto';
    }

    static openConfirmModal(productName, productId) {
        const modal = document.getElementById('confirmModal');
        const message = document.getElementById('confirmMessage');
        message.textContent = `Tem certeza que deseja deletar o produto "${productName}"?`;
        modal.classList.add('show');
        window.productIdToDelete = productId;
    }

    static closeConfirmModal() {
        const modal = document.getElementById('confirmModal');
        modal.classList.remove('show');
    }

    static loadProductToForm(product) {
        document.getElementById('productId').value = product.id;
        document.getElementById('productName').value = product.name;
        document.getElementById('productSku').value = product.sku;
        document.getElementById('productPrice').value = product.price;
        document.getElementById('productActive').checked = product.active;
        document.getElementById('modalTitle').textContent = 'Editar Produto';
    }

    static getFormData() {
        return {
            name: document.getElementById('productName').value,
            sku: document.getElementById('productSku').value,
            price: parseFloat(document.getElementById('productPrice').value),
            active: document.getElementById('productActive').checked
        };
    }

    static renderProducts(products, currentPage = 1) {
        const tbody = document.getElementById('productsTableBody');
        const emptyState = document.getElementById('emptyState');
        
        if (products.length === 0) {
            tbody.innerHTML = '';
            emptyState.style.display = 'block';
            return;
        }

        emptyState.style.display = 'none';
        tbody.innerHTML = products.map(product => `
            <tr>
                <td>${product.id}</td>
                <td><strong>${product.name}</strong></td>
                <td>${product.sku}</td>
                <td>R$ ${parseFloat(product.price).toFixed(2)}</td>
                <td>
                    <span class="status-badge ${product.active ? 'status-active' : 'status-inactive'}">
                        ${product.active ? 'Ativo' : 'Inativo'}
                    </span>
                </td>
                <td>
                    <div class="actions">
                        <button class="action-btn edit-btn" onclick="app.editProduct(${product.id})">Editar</button>
                        <button class="action-btn delete-btn" onclick="app.deleteProduct(${product.id}, '${product.name}')">Deletar</button>
                    </div>
                </td>
            </tr>
        `).join('');
    }

    static renderPagination(currentPage, totalPages) {
        const paginationDiv = document.getElementById('pagination');
        
        if (totalPages <= 1) {
            paginationDiv.innerHTML = '';
            return;
        }

        let html = '';

        // Botão Anterior
        if (currentPage > 1) {
            html += `<button onclick="app.goToPage(${currentPage - 1})">← Anterior</button>`;
        }

        // Números de página
        const startPage = Math.max(1, currentPage - 2);
        const endPage = Math.min(totalPages, currentPage + 2);

        if (startPage > 1) {
            html += `<button onclick="app.goToPage(1)">1</button>`;
            if (startPage > 2) {
                html += `<span>...</span>`;
            }
        }

        for (let i = startPage; i <= endPage; i++) {
            if (i === currentPage) {
                html += `<button class="active">${i}</button>`;
            } else {
                html += `<button onclick="app.goToPage(${i})">${i}</button>`;
            }
        }

        if (endPage < totalPages) {
            if (endPage < totalPages - 1) {
                html += `<span>...</span>`;
            }
            html += `<button onclick="app.goToPage(${totalPages})">${totalPages}</button>`;
        }

        // Botão Próximo
        if (currentPage < totalPages) {
            html += `<button onclick="app.goToPage(${currentPage + 1})">Próximo →</button>`;
        }

        paginationDiv.innerHTML = html;
    }
}
