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

// Chart Instance
let tccChart = null;

function calculateSettings() {
    // 1. Calculate Is (Pickup)
    // Using the same logic as adaptive_logic.py
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
    // Target time is 0.25s for primary protection
    const targetTime = 0.25;
    const curve = CURVES[state.curveType];
    const psm = state.faultCurrent / state.is;

    if (psm <= 1) {
        state.tms = 0.1;
    } else {
        // t = TMS * (k / ((I/Is)^alpha - 1))
        // TMS = t / (k / (psm^alpha - 1))
        state.tms = targetTime / (curve.k / (Math.pow(psm, curve.alpha) - 1));
    }

    // Clamp TMS
    state.tms = Math.max(0.05, Math.min(1.1, state.tms));

    updateUI();
}

function updateUI() {
    document.getElementById('fault-current-val').textContent = state.faultCurrent;
    document.getElementById('load-current-val').textContent = state.loadCurrent;
    document.getElementById('mode-status').textContent = state.ibrActive ? 'ADAPTIVE' : 'FIXED';
    document.getElementById('mode-status').parentElement.style.borderColor = state.ibrActive ? '#38bdf8' : '#94a3b8';

    document.getElementById('is-value').textContent = state.is.toFixed(2) + ' A';
    document.getElementById('tms-value').textContent = state.tms.toFixed(3);
    
    // Trip time check
    const curve = CURVES[state.curveType];
    const psm = state.faultCurrent / state.is;
    let tripTime = Infinity;
    if (psm > 1) {
        tripTime = state.tms * (curve.k / (Math.pow(psm, curve.alpha) - 1));
    }
    document.getElementById('trip-time-value').textContent = tripTime.toFixed(3) + 's';

    updateChart();
}

function updateChart() {
    const curve = CURVES[state.curveType];
    const dataPoints = [];
    
    // Generate logarithmic scale points for the curve
    // From 1.1 * Is to 20 * Is
    for (let psm = 1.1; psm <= 20; psm += 0.5) {
        const t = state.tms * (curve.k / (Math.pow(psm, curve.alpha) - 1));
        dataPoints.push({ x: psm * state.is, y: t });
    }

    const currentFaultPoint = {
        x: state.faultCurrent,
        y: state.tms * (curve.k / (Math.pow(state.faultCurrent / state.is, curve.alpha) - 1))
    };

    tccChart.data.datasets[0].data = dataPoints;
    tccChart.data.datasets[1].data = [currentFaultPoint];
    tccChart.update();
}

function initChart() {
    const ctx = document.getElementById('tccChart').getContext('2d');
    tccChart = new Chart(ctx, {
        type: 'line',
        data: {
            datasets: [{
                label: 'Relay Characteristic',
                borderColor: '#38bdf8',
                backgroundColor: 'rgba(56, 189, 248, 0.1)',
                borderWidth: 2,
                pointRadius: 0,
                fill: true,
                tension: 0.4,
                data: []
            }, {
                label: 'Current Operating Point',
                borderColor: '#f8fafc',
                backgroundColor: '#f8fafc',
                pointRadius: 6,
                pointHoverRadius: 8,
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
                    title: { display: true, text: 'Current (Amperes)', color: '#94a3b8' },
                    grid: { color: 'rgba(255, 255, 255, 0.05)' },
                    ticks: { color: '#94a3b8' }
                },
                y: {
                    type: 'logarithmic',
                    min: 0.01,
                    max: 10,
                    title: { display: true, text: 'Time (Seconds)', color: '#94a3b8' },
                    grid: { color: 'rgba(255, 255, 255, 0.05)' },
                    ticks: { color: '#94a3b8' }
                }
            },
            plugins: {
                legend: { display: false }
            }
        }
    });
}

// Event Listeners
document.getElementById('fault-current').addEventListener('input', (e) => {
    state.faultCurrent = parseFloat(e.target.value);
    calculateSettings();
});

document.getElementById('load-current').addEventListener('input', (e) => {
    state.loadCurrent = parseFloat(e.target.value);
    calculateSettings();
});

document.getElementById('ibr-toggle').addEventListener('change', (e) => {
    state.ibrActive = e.target.checked;
    calculateSettings();
});

document.getElementById('curve-type').addEventListener('change', (e) => {
    state.curveType = e.target.value;
    calculateSettings();
});

// Init
window.addEventListener('DOMContentLoaded', () => {
    initChart();
    calculateSettings();
});
