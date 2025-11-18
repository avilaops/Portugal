/**
 * GitHub Sync Module
 * Sincroniza dados locais com GitHub Repository
 */

class GitHubSync {
    constructor(config) {
        this.owner = config.owner || 'avilaops';
        this.repo = config.repo || 'Portugal';
        this.branch = config.branch || 'main';
        this.filePath = config.filePath || 'docs/data/estabelecimentos.json';
        this.token = config.token || null; // Personal Access Token (opcional)
        this.apiBase = 'https://api.github.com';
    }

    /**
     * Busca dados do GitHub
     */
    async fetchFromGitHub() {
        try {
            const url = `${this.apiBase}/repos/${this.owner}/${this.repo}/contents/${this.filePath}?ref=${this.branch}`;
            const headers = {
                'Accept': 'application/vnd.github.v3+json'
            };

            if (this.token) {
                headers['Authorization'] = `token ${this.token}`;
            }

            const response = await fetch(url, { headers });

            if (!response.ok) {
                throw new Error(`GitHub API error: ${response.status}`);
            }

            const data = await response.json();
            const content = atob(data.content); // Decode base64
            return {
                data: JSON.parse(content),
                sha: data.sha // Necessário para updates
            };
        } catch (error) {
            console.error('Erro ao buscar do GitHub:', error);
            return null;
        }
    }

    /**
     * Salva dados no GitHub (requer token)
     */
    async saveToGitHub(data, sha, message = 'Update estabelecimentos data') {
        if (!this.token) {
            console.warn('GitHub token não configurado. Salvando apenas localmente.');
            return false;
        }

        try {
            const url = `${this.apiBase}/repos/${this.owner}/${this.repo}/contents/${this.filePath}`;
            const content = btoa(JSON.stringify(data, null, 2)); // Encode base64

            const response = await fetch(url, {
                method: 'PUT',
                headers: {
                    'Accept': 'application/vnd.github.v3+json',
                    'Authorization': `token ${this.token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message,
                    content,
                    sha,
                    branch: this.branch
                })
            });

            if (!response.ok) {
                throw new Error(`GitHub API error: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Erro ao salvar no GitHub:', error);
            return false;
        }
    }

    /**
     * Sincroniza: busca do GitHub e mescla com dados locais
     */
    async sync(localData) {
        // Busca dados remotos
        const remote = await this.fetchFromGitHub();

        if (!remote) {
            console.log('Usando apenas dados locais');
            return { data: localData, sha: null, synced: false };
        }

        // Mescla dados (prioridade para o mais recente)
        const merged = this.mergeData(localData, remote.data.estabelecimentos || []);

        return {
            data: merged,
            sha: remote.sha,
            synced: true,
            lastSync: new Date().toISOString()
        };
    }

    /**
     * Mescla dados locais e remotos (evita duplicatas)
     */
    mergeData(local, remote) {
        const map = new Map();

        // Adiciona dados remotos
        remote.forEach(item => {
            map.set(item.id, item);
        });

        // Adiciona/atualiza com dados locais (mais recentes)
        local.forEach(item => {
            const existing = map.get(item.id);
            if (!existing || new Date(item.dataMapeamento) > new Date(existing.dataMapeamento)) {
                map.set(item.id, item);
            }
        });

        return Array.from(map.values());
    }
}

// Exporta para uso global
window.GitHubSync = GitHubSync;
