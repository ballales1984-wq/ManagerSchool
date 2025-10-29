/**
 * DASHBOARD INTERATTIVA - ManagerSchool
 * Grafici e visualizzazioni interattive con Chart.js
 */

// ========================================
// CONFIGURAZIONE CHART.JS
// ========================================

Chart.defaults.color = '#333';
Chart.defaults.font.family = "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif';
Chart.defaults.font.size = 12;

// ========================================
// GRAFICO DISTRIBUZIONE VOTI
// ========================================

function initDistribuzioneVoti(data) {
    const ctx = document.getElementById('distribuzioneVoti');
    if (!ctx) return;
    
    const config = {
        type: 'bar',
        data: {
            labels: data.labels || [],
            datasets: [{
                label: 'Numero Voti',
                data: data.values || [],
                backgroundColor: 'rgba(102, 126, 234, 0.8)',
                borderColor: 'rgba(102, 126, 234, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: 'Distribuzione Voti',
                    font: { size: 16 }
                }
            }
        }
    };
    
    new Chart(ctx, config);
}

// ========================================
// GRAFICO TREND ANDAMENTO
// ========================================

function initTrendAndamento(data) {
    const ctx = document.getElementById('trendAndamento');
    if (!ctx) return;
    
    const config = {
        type: 'line',
        data: {
            labels: data.labels || [],
            datasets: [{
                label: 'Media Generale',
                data: data.medie || [],
                borderColor: 'rgba(102, 126, 234, 1)',
                backgroundColor: 'rgba(102, 126, 234, 0.1)',
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: false,
                    min: 0,
                    max: 10
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Trend Andamento Media',
                    font: { size: 16 }
                }
            }
        }
    };
    
    new Chart(ctx, config);
}

// ========================================
// GRAFICO FRAGILITÀ VS VOTI
// ========================================

function initFragilitaVsVoti(data) {
    const ctx = document.getElementById('fragilitaVsVoti');
    if (!ctx) return;
    
    const config = {
        type: 'scatter',
        data: {
            datasets: [{
                label: 'Fragilità vs Media',
                data: data.points || [],
                backgroundColor: 'rgba(245, 101, 101, 0.6)',
                borderColor: 'rgba(245, 101, 101, 1)'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Fragilità'
                    },
                    min: 0,
                    max: 100
                },
                y: {
                    title: {
                        display: true,
                        text: 'Media Voti'
                    },
                    min: 0,
                    max: 10
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Correlazione Fragilità - Voti',
                    font: { size: 16 }
                }
            }
        }
    };
    
    new Chart(ctx, config);
}

// ========================================
// GRAFICO MEDIE PER MATERIA
// ========================================

function initMediePerMateria(data) {
    const ctx = document.getElementById('mediePerMateria');
    if (!ctx) return;
    
    const config = {
        type: 'doughnut',
        data: {
            labels: data.labels || [],
            datasets: [{
                data: data.values || [],
                backgroundColor: [
                    'rgba(102, 126, 234, 0.8)',
                    'rgba(245, 101, 101, 0.8)',
                    'rgba(72, 187, 120, 0.8)',
                    'rgba(255, 193, 7, 0.8)',
                    'rgba(23, 162, 184, 0.8)'
                ],
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Medie per Materia',
                    font: { size: 16 }
                },
                legend: {
                    position: 'bottom'
                }
            }
        }
    };
    
    new Chart(ctx, config);
}

// ========================================
// GRAFICO PRESENZE
// ========================================

function initPresenzeChart(data) {
    const ctx = document.getElementById('presenzeChart');
    if (!ctx) return;
    
    const config = {
        type: 'bar',
        data: {
            labels: data.labels || [],
            datasets: [
                {
                    label: 'Presenze',
                    data: data.presenze || [],
                    backgroundColor: 'rgba(72, 187, 120, 0.8)'
                },
                {
                    label: 'Assenze',
                    data: data.assenze || [],
                    backgroundColor: 'rgba(245, 101, 101, 0.8)'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    stacked: true
                },
                y: {
                    stacked: true,
                    beginAtZero: true
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Presenze e Assenze',
                    font: { size: 16 }
                }
            }
        }
    };
    
    new Chart(ctx, config);
}

// ========================================
// CARICA DATI E INITIALIZZA GRAFICI
// ========================================

async function loadDashboardData() {
    try {
        // Carica statistiche generali
        const statsResponse = await fetch('/api/dashboard/stats');
        const stats = await statsResponse.json();
        
        // Carica dati per grafici
        const chartsResponse = await fetch('/api/dashboard/charts');
        const charts = await chartsResponse.json();
        
        // Inizializza tutti i grafici
        initDistribuzioneVoti(charts.distribuzione || {});
        initTrendAndamento(charts.trend || {});
        initFragilitaVsVoti(charts.fragilita || {});
        initMediePerMateria(charts.medie || {});
        initPresenzeChart(charts.presenze || {});
        
        console.log('✅ Grafici dashboard inizializzati');
        
    } catch (error) {
        console.error('Errore caricamento dati dashboard:', error);
    }
}

// ========================================
// AUTO-REFRESH GRAFICI
// ========================================

function autoRefreshCharts(interval = 30000) {
    setInterval(() => {
        // Ricarica dati ogni 30 secondi
        loadDashboardData();
    }, interval);
}

// ========================================
// EXPORT
// ========================================

if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        loadDashboardData,
        autoRefreshCharts
    };
}

