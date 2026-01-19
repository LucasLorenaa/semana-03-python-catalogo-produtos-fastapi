// Aplicação Principal
class App {
    constructor() {
        this.currentPage = 1;
        this.itemsPerPage = 10;
        this.allProducts = [];
        this.filteredProducts = [];
        this.currentEditingId = null;
        this.filterName = '';
        this.filterId = null;

        this.init();
    }

    async init() {
        this.setupEventListeners();
        await this.loadProducts();
    }

    setupEventListeners() {
        // Modal
        document.getElementById('btnOpenModal').addEventListener('click', () => this.openNewProductModal());
        document.getElementById('btnCloseModal').addEventListener('click', () => UI.closeModal());
        document.getElementById('btnCancelForm').addEventListener('click', () => UI.closeModal());
        document.getElementById('productForm').addEventListener('submit', (e) => this.handleFormSubmit(e));

        // Modal de Confirmação
        document.getElementById('btnCancelDelete').addEventListener('click', () => UI.closeConfirmModal());
        document.getElementById('btnConfirmDelete').addEventListener('click', () => this.confirmDelete());

        // Filtros
        document.getElementById('filterName').addEventListener('input', (e) => {
            this.filterName = e.target.value.toLowerCase();
            this.currentPage = 1;
            this.applyFilters();
        });

        document.getElementById('filterId').addEventListener('input', (e) => {
            this.filterId = e.target.value ? parseInt(e.target.value) : null;
            this.currentPage = 1;
            this.applyFilters();
        });

        document.getElementById('btnClearFilters').addEventListener('click', () => {
            document.getElementById('filterName').value = '';
            document.getElementById('filterId').value = '';
            this.filterName = '';
            this.filterId = null;
            this.currentPage = 1;
            this.renderPage();
        });

        // Fechar modal ao clicar fora
        document.getElementById('modal').addEventListener('click', (e) => {
            if (e.target.id === 'modal') {
                UI.closeModal();
            }
        });

        document.getElementById('confirmModal').addEventListener('click', (e) => {
            if (e.target.id === 'confirmModal') {
                UI.closeConfirmModal();
            }
        });
    }

    async loadProducts() {
        UI.showLoading(true);
        try {
            this.allProducts = await ProductAPI.getProducts(0, 1000);
            this.filteredProducts = [...this.allProducts];
            this.renderPage();
        } catch (error) {
            UI.showError('Erro ao carregar produtos: ' + error.message);
        } finally {
            UI.showLoading(false);
        }
    }

    applyFilters() {
        this.filteredProducts = this.allProducts.filter(product => {
            const matchName = product.name.toLowerCase().includes(this.filterName);
            const matchId = this.filterId === null || product.id === this.filterId;
            return matchName && matchId;
        });
        this.renderPage();
    }

    renderPage() {
        const start = (this.currentPage - 1) * this.itemsPerPage;
        const end = start + this.itemsPerPage;
        const pageProducts = this.filteredProducts.slice(start, end);

        UI.renderProducts(pageProducts, this.currentPage);

        const totalPages = Math.ceil(this.filteredProducts.length / this.itemsPerPage);
        UI.renderPagination(this.currentPage, totalPages);
    }

    goToPage(pageNumber) {
        const totalPages = Math.ceil(this.filteredProducts.length / this.itemsPerPage);
        if (pageNumber >= 1 && pageNumber <= totalPages) {
            this.currentPage = pageNumber;
            this.renderPage();
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
    }

    openNewProductModal() {
        this.currentEditingId = null;
        UI.closeModal();
        setTimeout(() => UI.openModal(), 100);
    }

    async editProduct(id) {
        try {
            this.currentEditingId = id;
            const product = await ProductAPI.getProductById(id);
            UI.loadProductToForm(product);
            UI.openModal();
        } catch (error) {
            UI.showError('Erro ao carregar produto: ' + error.message);
        }
    }

    deleteProduct(id, name) {
        UI.openConfirmModal(name, id);
    }

    async confirmDelete() {
        UI.closeConfirmModal();
        UI.showLoading(true);
        try {
            await ProductAPI.deleteProduct(window.productIdToDelete);
            UI.showSuccess('Produto deletado com sucesso!');
            await this.loadProducts();
        } catch (error) {
            UI.showError('Erro ao deletar produto: ' + error.message);
        } finally {
            UI.showLoading(false);
        }
    }

    async handleFormSubmit(e) {
        e.preventDefault();
        UI.showLoading(true);

        try {
            const formData = UI.getFormData();

            if (!formData.name || !formData.sku || formData.price <= 0) {
                UI.showError('Por favor, preencha todos os campos corretamente.');
                UI.showLoading(false);
                return;
            }

            if (this.currentEditingId) {
                // Atualizar
                await ProductAPI.updateProduct(this.currentEditingId, formData);
                UI.showSuccess('Produto atualizado com sucesso!');
            } else {
                // Criar
                await ProductAPI.createProduct(formData);
                UI.showSuccess('Produto criado com sucesso!');
            }

            UI.closeModal();
            await this.loadProducts();
        } catch (error) {
            UI.showError('Erro ao salvar produto: ' + error.message);
        } finally {
            UI.showLoading(false);
        }
    }

    // Formatar valor para moeda brasileira
    formatCurrency(element) {
        let value = element.value.replace(/\D/g, '');
        
        if (value.length === 0) {
            element.value = '';
            return;
        }

        // Converter para número com 2 casas decimais
        value = parseInt(value) / 100;
        
        // Formatar como moeda brasileira
        element.value = value.toLocaleString('pt-BR', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        });
    }

    // Converter moeda para número para envio à API
    currencyToNumber(currencyString) {
        if (!currencyString) return 0;
        // Remove "R$" e espaços em branco
        let cleanValue = currencyString.replace('R$', '').trim();
        // Substitui separador de milhares (ponto) e separador decimal (vírgula)
        cleanValue = cleanValue.replace(/\./g, '').replace(',', '.');
        return parseFloat(cleanValue) || 0;
    }
}

// Inicializar aplicação quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
    window.app = new App();
});
