/**
 * XinoFarmer - Main JavaScript Application
 * Handles UI interactions, API calls, and bot control
 */

class XinoFarmerApp {
    constructor() {
        this.isRunning = false;
        this.isPaused = false;
        this.logIndex = 0;
        this.startTime = null;
        this.timerInterval = null;
        this.logPollingInterval = null;
    }

    init() {
        this.bindEvents();
        this.startLogPolling();
        this.loadConfig();
    }

    bindEvents() {
        // Navigation
        document.querySelectorAll('.nav-item[data-tab]').forEach(item => {
            item.addEventListener('click', (e) => this.handleNavClick(e));
        });

        // Bot Control Buttons
        const startBtn = document.getElementById('startBtn');
        const pauseBtn = document.getElementById('pauseBtn');
        const stopBtn = document.getElementById('stopBtn');
        const saveBtn = document.getElementById('saveBtn');

        if (startBtn) startBtn.addEventListener('click', () => this.startBot());
        if (pauseBtn) pauseBtn.addEventListener('click', () => this.pauseBot());
        if (stopBtn) stopBtn.addEventListener('click', () => this.stopBot());
        if (saveBtn) saveBtn.addEventListener('click', () => this.saveConfig());

        // Logout
        const logoutBtn = document.getElementById('logoutBtn');
        if (logoutBtn) logoutBtn.addEventListener('click', () => this.logout());

        // Clear Logs
        const clearLogsBtn = document.getElementById('clearLogsBtn');
        if (clearLogsBtn) clearLogsBtn.addEventListener('click', () => this.clearLogs());

        // Telegram toggle
        const telegramActive = document.getElementById('telegramActive');
        if (telegramActive) {
            telegramActive.addEventListener('change', (e) => {
                const tokenGroup = document.getElementById('telegramTokenGroup');
                if (tokenGroup) {
                    tokenGroup.style.display = e.target.value === 'Yes' ? 'block' : 'none';
                }
            });
        }

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.key === 'F9') {
                e.preventDefault();
                if (this.isRunning) {
                    this.stopBot();
                }
            }
        });
    }

    handleNavClick(e) {
        e.preventDefault();
        const tabId = e.currentTarget.dataset.tab;

        // Update active nav item
        document.querySelectorAll('.nav-item').forEach(item => item.classList.remove('active'));
        e.currentTarget.classList.add('active');

        // Show corresponding tab content
        document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
        const tabContent = document.getElementById(`tab-${tabId}`);
        if (tabContent) tabContent.classList.add('active');

        // Update page title
        const pageTitle = document.getElementById('pageTitle');
        if (pageTitle) {
            pageTitle.textContent = e.currentTarget.querySelector('span').textContent;
        }
    }

    async startBot() {
        const action = document.getElementById('actionSelect')?.value || 'SpotFarm';

        try {
            const response = await this.apiCall('/api/bot/start', 'POST', { action });

            if (response.status === 'ok') {
                this.isRunning = true;
                this.isPaused = false;
                this.updateBotStatus();
                this.startTimer();
                this.addLog(`Bot started with action: ${action}`, 'success');
                this.showToast('Bot started successfully!', 'success');
            }
        } catch (error) {
            this.addLog(`Failed to start bot: ${error.message}`, 'error');
            this.showToast('Failed to start bot', 'error');
        }
    }

    async stopBot() {
        try {
            const response = await this.apiCall('/api/bot/stop', 'POST');

            if (response.status === 'ok') {
                this.isRunning = false;
                this.isPaused = false;
                this.updateBotStatus();
                this.stopTimer();
                this.addLog('Bot stopped', 'warning');
                this.showToast('Bot stopped', 'info');
            }
        } catch (error) {
            this.addLog(`Failed to stop bot: ${error.message}`, 'error');
            this.showToast('Failed to stop bot', 'error');
        }
    }

    async pauseBot() {
        try {
            const response = await this.apiCall('/api/bot/pause', 'POST');

            if (response.status === 'ok') {
                this.isPaused = response.is_paused;
                this.updateBotStatus();
                const status = this.isPaused ? 'paused' : 'resumed';
                this.addLog(`Bot ${status}`, 'warning');
                this.showToast(`Bot ${status}`, 'info');
            }
        } catch (error) {
            this.addLog(`Failed to pause bot: ${error.message}`, 'error');
        }
    }

    async saveConfig() {
        const config = this.gatherConfig();

        try {
            const response = await this.apiCall('/api/config', 'POST', config);

            if (response.status === 'ok') {
                this.addLog('Configuration saved', 'success');
                this.showToast('Configuration saved!', 'success');
            }
        } catch (error) {
            this.addLog(`Failed to save config: ${error.message}`, 'error');
            this.showToast('Failed to save configuration', 'error');
        }
    }

    async loadConfig() {
        try {
            const config = await this.apiCall('/api/config', 'GET');
            this.applyConfig(config);
        } catch (error) {
            console.error('Failed to load config:', error);
        }
    }

    gatherConfig() {
        const config = {
            Main: {
                VMName: document.getElementById('vmName')?.value || '',
                LDPath: document.getElementById('ldPath')?.value || '',
                Action: document.getElementById('actionSelect')?.value || 'SpotFarm',
                Language: document.getElementById('languageSelect')?.value || 'English',
                Player: document.getElementById('playerSelect')?.value || '1'
            },
            SpotFarm: {
                SpotFarmMap: document.getElementById('spotFarmMap')?.value || 'Ashwold'
            },
            Dungeon: {
                name: document.getElementById('dungeonName')?.value || '',
                Team_solo: document.getElementById('dungeonTeamSolo')?.value || 'Solo',
                Time_to_exit: document.getElementById('dungeonTimeToExit')?.value || '300'
            },
            Fish2: {
                Fish2Type: document.getElementById('fishType')?.value || 'Gold',
                Maps: document.getElementById('fishMap')?.value || 'Ashwold',
                Zones: document.getElementById('fishZone')?.value || 'Zone1',
                Fish2_IterMin: document.getElementById('fishIterMin')?.value || '3',
                Fish2_IterMax: document.getElementById('fishIterMax')?.value || '5'
            },
            Cyrangar: {
                Mode: document.getElementById('cyrangarMode')?.value || 'EndlessFight',
                StayAtTheDoor: document.getElementById('cyrangarStayAtDoor')?.value || 'No',
                Time_to_exit: document.getElementById('cyrangarTimeToExit')?.value || '180'
            },
            Telegram: {
                Active: document.getElementById('telegramActive')?.value || 'No'
            }
        };

        return config;
    }

    applyConfig(config) {
        if (!config) return;

        // Main settings
        if (config.Main) {
            this.setSelectValue('vmName', config.Main.VMName);
            this.setSelectValue('ldPath', config.Main.LDPath);
            this.setSelectValue('actionSelect', config.Main.Action);
            this.setSelectValue('languageSelect', config.Main.Language);
            this.setSelectValue('playerSelect', config.Main.Player);
        }

        // SpotFarm settings
        if (config.SpotFarm) {
            this.setSelectValue('spotFarmMap', config.SpotFarm.SpotFarmMap);
        }

        // Dungeon settings
        if (config.Dungeon) {
            this.setSelectValue('dungeonName', config.Dungeon.name);
            this.setSelectValue('dungeonTeamSolo', config.Dungeon.Team_solo);
            this.setSelectValue('dungeonTimeToExit', config.Dungeon.Time_to_exit);
        }

        // Fishing settings
        if (config.Fish2) {
            this.setSelectValue('fishType', config.Fish2.Fish2Type);
            this.setSelectValue('fishMap', config.Fish2.Maps);
            this.setSelectValue('fishZone', config.Fish2.Zones);
            this.setSelectValue('fishIterMin', config.Fish2.Fish2_IterMin);
            this.setSelectValue('fishIterMax', config.Fish2.Fish2_IterMax);
        }

        // Cyrangar settings
        if (config.Cyrangar) {
            this.setSelectValue('cyrangarMode', config.Cyrangar.Mode);
            this.setSelectValue('cyrangarStayAtDoor', config.Cyrangar.StayAtTheDoor);
            this.setSelectValue('cyrangarTimeToExit', config.Cyrangar.Time_to_exit);
        }

        // Telegram settings
        if (config.Telegram) {
            this.setSelectValue('telegramActive', config.Telegram.Active);
            const telegramActive = document.getElementById('telegramActive');
            if (telegramActive && config.Telegram.Active === 'Yes') {
                const tokenGroup = document.getElementById('telegramTokenGroup');
                if (tokenGroup) tokenGroup.style.display = 'block';
            }
        }
    }

    setSelectValue(id, value) {
        const element = document.getElementById(id);
        if (element && value !== undefined && value !== null) {
            element.value = value;
        }
    }

    updateBotStatus() {
        const statusIndicator = document.getElementById('botStatus');
        const statusText = document.getElementById('statusText');
        const startBtn = document.getElementById('startBtn');
        const pauseBtn = document.getElementById('pauseBtn');
        const stopBtn = document.getElementById('stopBtn');

        if (statusIndicator && statusText) {
            statusIndicator.className = 'status-indicator';

            if (this.isRunning) {
                if (this.isPaused) {
                    statusIndicator.classList.add('status-paused');
                    statusText.textContent = 'Paused';
                } else {
                    statusIndicator.classList.add('status-running');
                    statusText.textContent = 'Running';
                }
            } else {
                statusIndicator.classList.add('status-stopped');
                statusText.textContent = 'Stopped';
            }
        }

        // Update button states
        if (startBtn) startBtn.disabled = this.isRunning && !this.isPaused;
        if (pauseBtn) pauseBtn.disabled = !this.isRunning;
        if (stopBtn) stopBtn.disabled = !this.isRunning;

        // Update pause button text
        if (pauseBtn) {
            pauseBtn.innerHTML = this.isPaused
                ? '<svg viewBox="0 0 24 24" fill="currentColor" width="20" height="20"><path d="M8 5v14l11-7z"/></svg> Resume'
                : '<svg viewBox="0 0 24 24" fill="currentColor" width="20" height="20"><path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/></svg> Pause';
        }
    }

    startTimer() {
        this.startTime = Date.now();
        this.timerInterval = setInterval(() => this.updateTimer(), 1000);
    }

    stopTimer() {
        if (this.timerInterval) {
            clearInterval(this.timerInterval);
            this.timerInterval = null;
        }
        this.startTime = null;
        const runningTime = document.getElementById('runningTime');
        if (runningTime) runningTime.textContent = '00:00:00';
    }

    updateTimer() {
        if (!this.startTime || this.isPaused) return;

        const elapsed = Date.now() - this.startTime;
        const hours = Math.floor(elapsed / 3600000);
        const minutes = Math.floor((elapsed % 3600000) / 60000);
        const seconds = Math.floor((elapsed % 60000) / 1000);

        const timeString = [hours, minutes, seconds]
            .map(n => n.toString().padStart(2, '0'))
            .join(':');

        const runningTime = document.getElementById('runningTime');
        if (runningTime) runningTime.textContent = timeString;
    }

    startLogPolling() {
        this.logPollingInterval = setInterval(() => this.pollLogs(), 2000);
    }

    async pollLogs() {
        try {
            const response = await this.apiCall(`/api/logs?since=${this.logIndex}`, 'GET');

            if (response.logs && response.logs.length > 0) {
                response.logs.forEach(log => {
                    this.addLogEntry(log.message, this.getLogClass(log.color), log.timestamp);
                });
                this.logIndex = response.total;
            }
        } catch (error) {
            // Silently fail log polling
        }
    }

    getLogClass(color) {
        const colorMap = {
            'green': 'log-success',
            'red': 'log-error',
            'yellow': 'log-warning',
            'orange': 'log-warning',
            'blue': 'log-info'
        };
        return colorMap[color] || '';
    }

    addLog(message, type = '') {
        const timestamp = new Date().toISOString();
        this.addLogEntry(message, `log-${type}`, timestamp);
    }

    addLogEntry(message, className = '', timestamp = null) {
        const logConsole = document.getElementById('logConsole');
        if (!logConsole) return;

        const time = timestamp
            ? new Date(timestamp).toLocaleTimeString()
            : new Date().toLocaleTimeString();

        const entry = document.createElement('div');
        entry.className = 'log-entry';
        entry.innerHTML = `
            <span class="log-time">[${time}]</span>
            <span class="log-message ${className}">${this.escapeHtml(message)}</span>
        `;

        logConsole.appendChild(entry);
        logConsole.scrollTop = logConsole.scrollHeight;

        // Limit log entries
        while (logConsole.children.length > 500) {
            logConsole.removeChild(logConsole.firstChild);
        }
    }

    clearLogs() {
        const logConsole = document.getElementById('logConsole');
        if (logConsole) {
            logConsole.innerHTML = `
                <div class="log-entry">
                    <span class="log-time">[${new Date().toLocaleTimeString()}]</span>
                    <span class="log-message">Logs cleared</span>
                </div>
            `;
        }
        this.logIndex = 0;
    }

    async logout() {
        try {
            await this.apiCall('/api/auth/logout', 'POST');
            window.location.href = '/';
        } catch (error) {
            window.location.href = '/';
        }
    }

    async apiCall(endpoint, method = 'GET', body = null) {
        const options = {
            method,
            headers: {
                'Content-Type': 'application/json'
            }
        };

        if (body && method !== 'GET') {
            options.body = JSON.stringify(body);
        }

        const response = await fetch(endpoint, options);

        if (!response.ok) {
            const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
            throw new Error(error.detail || error.message || 'Request failed');
        }

        return response.json();
    }

    showToast(message, type = 'info') {
        // Remove existing toasts
        const existingToast = document.querySelector('.alert-toast');
        if (existingToast) {
            existingToast.remove();
        }

        const icons = {
            'success': '✓',
            'error': '✕',
            'warning': '⚠',
            'info': 'ℹ'
        };

        const toast = document.createElement('div');
        toast.className = `alert alert-toast alert-${type}`;
        toast.innerHTML = `
            <span class="alert-icon">${icons[type] || icons.info}</span>
            <span>${this.escapeHtml(message)}</span>
        `;
        document.body.appendChild(toast);

        // Trigger animation
        setTimeout(() => toast.classList.add('show'), 10);

        // Auto remove
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, 4000);
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Global instance
window.XinoFarmerApp = XinoFarmerApp;
