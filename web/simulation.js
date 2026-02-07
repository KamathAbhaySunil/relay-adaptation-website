// IEC IDMT Curve Constants
const CURVES = {
    standard: { k: 0.14, alpha: 0.02 },
    very: { k: 13.5, alpha: 1.0 },
    extreme: { k: 80.0, alpha: 2.0 }
};

// State
let state = {
    faultCurrent: 5000,
    loadCurrent: 800,
    ibrActive: false,
    curveType: 'standard',
    is: 1000,
    tms: 0.1
};

let tccChart = null;

function calculateSettings() {
    // 1. Calculate Is (Pickup)
    if (state.ibrActive) {
        state.is = 1.3 * state.loadCurrent;
    } else {
        state.is = 1.25 * state.loadCurrent;
    }

    // Sensitivity check: Is must be less than fault current
    if (state.is > 0.8 * state.faultCurrent) {
        state.is = 0.5 * state.faultCurrent;
    }

    // 2. Calculate TMS
    // Target time is 0.25s
    const targetTime = 0.25;
    const curve = CURVES[state.curveType];
    const psm = state.faultCurrent / state.is;

    if (psm <= 1) {
        state.tms = 0.1;
    } else {
        state.tms = targetTime / (curve.k / (Math.pow(psm, curve.alpha) - 1));
    }

    // Clamp TMS to prevent curve "flying away"
    state.tms = Math.max(0.05, Math.min(1.1, state.tms));

    updateUI();
}

function updateUI() {
    document.getElementById('fault-current-val').textContent = state.faultCurrent;
    document.getElementById('load-current-val').textContent = state.loadCurrent;
    document.getElementById('mode-status').textContent = state.ibrActive ? 'ADAPTIVE' : 'FIXED';
    
    const badge = document.getElementById('mode-status').parentElement;
    badge.style.background = state.ibrActive ? 'rgba(56, 189, 248, 0.1)' : 'rgba(255, 255, 255, 0.05)';
    badge.style.borderColor = state.ibrActive ? 'var(--accent)' : 'var(--border)';

    document.getElementById('is-value').textContent = state.is.toFixed(0) + ' A';
    document.getElementById('tms-value').textContent = state.tms.toFixed(3);
    
    const psm = state.faultCurrent / state.is;
    let tripTimeText = "---";
    if (psm > 1.01) {
        const curve = CURVES[state.curveType];
        const t = state.tms * (curve.k / (Math.pow(psm, curve.alpha) - 1));
        tripTimeText = t.toFixed(3) + 's';
    }
    document.getElementById('trip-time-value').textContent = tripTimeText;

    updateChart();
}

function updateChart() {
    if (!tccChart) return;

    const curve = CURVES[state.curveType];
    const dataPoints = [];
    
    // Generate scale points from 1.1x Is up to 20x Is
    // We limit current range for visual stability
    const maxI = 20000;
    const step = 200;
    
    for (let i = state.is * 1.1; i <= maxI; i += step) {
        const psm = i / state.is;
        let t = state.tms * (curve.k / (Math.pow(psm, curve.alpha) - 1));
        // Clamp t for stability on log scale
        if (t > 0 && t < 100) {
            dataPoints.push({ x: i, y: t });
        }
    }

    const psmCurrent = state.faultCurrent / state.is;
    let currentPoint = null;
    if (psmCurrent > 1.05) {
        currentPoint = {
            x: state.faultCurrent,
            y: state.tms * (curve.k / (Math.pow(psmCurrent, curve.alpha) - 1))
        };
    }

    tccChart.data.datasets[0].data = dataPoints;
    tccChart.data.datasets[1].data = currentPoint ? [currentPoint] : [];
    
    // Use 'none' to skip animations which cause vertical jump artifacts
    tccChart.update('none');
}

function initChart() {
    const ctx = document.getElementById('tccChart').getContext('2d');
    tccChart = new Chart(ctx, {
        type: 'line',
        data: {
            datasets: [{
                label: 'TCC Curve',
                borderColor: '#38bdf8',
                backgroundColor: 'rgba(56, 189, 248, 0.05)',
                borderWidth: 2,
                pointRadius: 0,
                fill: true,
                tension: 0.3,
                data: []
            }, {
                label: 'Fault Point',
                borderColor: '#ffffff',
                backgroundColor: '#38bdf8',
                pointRadius: 6,
                pointBorderWidth: 2,
                showLine: false,
                data: []
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    type: 'logarithmic',
                    min: 1000,
                    max: 20000,
                    title: { display: true, text: 'Current (A)', color: '#94a3b8' },
                    grid: { color: 'rgba(255, 255, 255, 0.05)' },
                    ticks: { color: '#94a3b8' }
                },
                y: {
                    type: 'logarithmic',
                    min: 0.01,
                    max: 10, // FIX: Constant max to prevent "falling"
                    title: { display: true, text: 'Time (s)', color: '#94a3b8' },
                    grid: { color: 'rgba(255, 255, 255, 0.05)' },
                    ticks: { 
                        color: '#94a3b8',
                        callback: value => value.toFixed(2)
                    }
                }
            },
            plugins: {
                legend: { display: false }
            }
        }
    });
}

// Listeners
if (document.getElementById('fault-current')) {
    document.getElementById('fault-current').addEventListener('input', e => {
        state.faultCurrent = parseFloat(e.target.value);
        calculateSettings();
    });

    document.getElementById('load-current').addEventListener('input', e => {
        state.loadCurrent = parseFloat(e.target.value);
        calculateSettings();
    });

    document.getElementById('ibr-toggle').addEventListener('change', e => {
        state.ibrActive = e.target.checked;
        calculateSettings();
    });

    document.getElementById('curve-type').addEventListener('change', e => {
        state.curveType = e.target.value;
        calculateSettings();
    });

    window.addEventListener('DOMContentLoaded', () => {
        initChart();
        calculateSettings();
    });
}
