/**
 * Ávila API Client
 * Cliente para integração com api.avila.inc
 */

class AvilaAPI {
    constructor() {
        this.baseURL = 'https://api.avila.inc/api/v1';
        this.token = localStorage.getItem('avila_auth_token');
    }

    /**
     * Headers padrão para requisições
     */
    getHeaders() {
        return {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${this.token}`,
            'X-Client': 'portugal-webapp'
        };
    }

    /**
     * Faz requisição à API
     */
    async request(endpoint, options = {}) {
        try {
            const response = await fetch(`${this.baseURL}${endpoint}`, {
                ...options,
                headers: {
                    ...this.getHeaders(),
                    ...options.headers
                }
            });

            if (response.status === 401) {
                // Token expirado, redireciona para login
                localStorage.removeItem('avila_auth_token');
                localStorage.removeItem('avila_user');
                window.location.href = 'login.html';
                return null;
            }

            if (!response.ok) {
                throw new Error(`API Error: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('API Request Error:', error);
            // Se API não estiver disponível, continua funcionando localmente
            return null;
        }
    }

    // ==================== ESTABELECIMENTOS ====================

    /**
     * Lista todos os estabelecimentos
     */
    async getEstabelecimentos() {
        return await this.request('/estabelecimentos');
    }

    /**
     * Cria novo estabelecimento
     */
    async createEstabelecimento(data) {
        return await this.request('/estabelecimentos', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }

    /**
     * Atualiza estabelecimento
     */
    async updateEstabelecimento(id, data) {
        return await this.request(`/estabelecimentos/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }

    /**
     * Deleta estabelecimento
     */
    async deleteEstabelecimento(id) {
        return await this.request(`/estabelecimentos/${id}`, {
            method: 'DELETE'
        });
    }

    /**
     * Busca estabelecimentos por filtros
     */
    async searchEstabelecimentos(filters) {
        const params = new URLSearchParams(filters);
        return await this.request(`/estabelecimentos/search?${params}`);
    }

    // ==================== DASHBOARD ====================

    /**
     * Obtém estatísticas do dashboard
     */
    async getDashboardStats() {
        return await this.request('/dashboard/stats');
    }

    /**
     * Obtém prioridades de contato
     */
    async getPrioridades() {
        return await this.request('/dashboard/prioridades');
    }

    // ==================== SINCRONIZAÇÃO ====================

    /**
     * Sincroniza dados locais com a nuvem
     */
    async syncData(localData) {
        return await this.request('/sync', {
            method: 'POST',
            body: JSON.stringify({
                estabelecimentos: localData,
                timestamp: new Date().toISOString()
            })
        });
    }

    /**
     * Obtém última sincronização
     */
    async getLastSync() {
        return await this.request('/sync/last');
    }

    // ==================== RELATÓRIOS ====================

    /**
     * Gera relatório de mapeamento
     */
    async generateReport(type = 'geral') {
        return await this.request(`/reports/${type}`);
    }

    /**
     * Exporta dados em formato específico
     */
    async exportData(format = 'json') {
        return await this.request(`/export?format=${format}`);
    }

    // ==================== ANALYTICS ====================

    /**
     * Registra evento de analytics
     */
    async trackEvent(eventName, eventData = {}) {
        return await this.request('/analytics/events', {
            method: 'POST',
            body: JSON.stringify({
                event: eventName,
                data: eventData,
                timestamp: new Date().toISOString()
            })
        });
    }
}

// Instância global da API
const avilaAPI = new AvilaAPI();

// Sistema híbrido: Local + Cloud
class HybridDataManager {
    constructor() {
        this.api = avilaAPI;
        this.localStorageKey = 'estabelecimentos';
        this.syncEnabled = true;
    }

    /**
     * Obtém dados (tenta cloud primeiro, fallback para local)
     */
    async getData() {
        if (navigator.onLine && this.syncEnabled) {
            const cloudData = await this.api.getEstabelecimentos();
            if (cloudData) {
                // Atualiza cache local
                localStorage.setItem(this.localStorageKey, JSON.stringify(cloudData));
                return cloudData;
            }
        }
        
        // Fallback: dados locais
        const localData = localStorage.getItem(this.localStorageKey);
        return localData ? JSON.parse(localData) : [];
    }

    /**
     * Salva dados (local + sync para cloud)
     */
    async saveData(data) {
        // Sempre salva localmente primeiro
        localStorage.setItem(this.localStorageKey, JSON.stringify(data));
        
        // Tenta sincronizar com cloud
        if (navigator.onLine && this.syncEnabled) {
            const result = await this.api.syncData(data);
            if (result) {
                console.log('✅ Dados sincronizados com a nuvem');
            } else {
                console.log('⚠️ Sincronização pendente (será feita quando possível)');
            }
        }
        
        return data;
    }

    /**
     * Adiciona novo estabelecimento
     */
    async addEstabelecimento(estabelecimento) {
        const data = await this.getData();
        estabelecimento.id = Date.now();
        estabelecimento.dataMapeamento = new Date().toISOString();
        data.push(estabelecimento);
        
        await this.saveData(data);
        
        // Track analytics
        await this.api.trackEvent('estabelecimento_criado', {
            tipo: estabelecimento.tipo,
            bairro: estabelecimento.bairro
        });
        
        return estabelecimento;
    }

    /**
     * Atualiza estabelecimento
     */
    async updateEstabelecimento(id, updates) {
        const data = await this.getData();
        const index = data.findIndex(e => e.id === id);
        
        if (index !== -1) {
            data[index] = { ...data[index], ...updates };
            await this.saveData(data);
            return data[index];
        }
        
        return null;
    }

    /**
     * Remove estabelecimento
     */
    async deleteEstabelecimento(id) {
        const data = await this.getData();
        const filtered = data.filter(e => e.id !== id);
        await this.saveData(filtered);
        return true;
    }
}

// Instância global do gerenciador híbrido
const dataManager = new HybridDataManager();
