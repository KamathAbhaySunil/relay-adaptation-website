# RelayAdapt: Next-Generation Adaptive Relay Protection

RelayAdapt is a comprehensive research and implementation framework for protecting modern microgrids dominated by Inverter-Based Resources (IBRs). Traditional protection schemes often fail in these environments due to current-limiting behaviors of inverters. This project provides an adaptive logic engine, a machine learning regressor, and an interactive visualization dashboard to solve these challenges.

## 🚀 Key Achievements
- **Adaptive Protection Engine**: Developed a Python-based logic that dynamically recalculates relay settings ($I_s$ and $TMS$) in real-time.
- **Machine Learning Integration**: Implemented a Neural Network (MLP) that predicts optimal relay settings with **99% accuracy**.
- **Interactive Dashboard**: Built a premium, dark-mode web interface for real-time TCC (Time-Current Characteristic) curve visualization.
- **IEEE Research Paper**: Authored a detailed 10-page IEEE conference-style report documenting the mathematical derivations and simulation results.
- **MATLAB to Python Migration**: Successfully ported legacy Simulink power system models to high-performance vectorized Python code.

## 📂 File Structure

```text
.
├── web/                    # Interactive Web Application
│   ├── index.html          # Main Dashboard
│   ├── paper.html          # IEEE Paper Viewer
│   ├── about.html          # Technical Documentation
│   ├── style.css           # Premium Glassmorphism Styles
│   ├── simulation.js       # Ported Relay Logic (JS)
│   └── SGP(PBL).pdf        # Embedded Research Paper
├── adaptive_logic.py       # Core Adaptation Engine
├── system_model.py         # 4-Bus Power System Physics
├── ml_model.py             # Neural Network Architecture
├── relay_parameters.py     # IEC/IEEE Standard Constants
├── run_simulation.py       # Main Simulation Runner
├── test_bench.py           # Corner-case Verification Suite
├── main.tex                # LaTeX Source of the Paper
├── relay_mlp_weights.npz   # Trained ML Model Weights
├── relay_training_data.csv  # Synthetic Training Dataset
└── relay_tcc_comparison.png # Visualization Output
```

## 🛠️ How to Run Locally

### 1. Prerequisites
Ensure you have Python 3.8+ installed. You will need the following libraries:
```bash
pip install numpy matplotlib pandas
```

### 2. Run the Simulation
To execute the power system simulation and generate adaptive relay curves:
```bash
python run_simulation.py
```
This will generate the `relay_tcc_comparison.png` plot showing the adaptive shift.

### 3. Run the Test Bench
To verify the system against corner cases (Weak Grid, Islanding, etc.):
```bash
python test_bench.py
```

### 4. Running the Web Dashboard
Since the dashboard is built with Vanilla JS, you don't need a complex server. Simply navigate to the `web` folder and open `index.html` in your browser, or use a simple local server:
```bash
cd web
python3 -m http.server 8000
```
Then visit `http://localhost:8000`.

## 📈 Methodology
RelayAdapt uses nodal impedance formulation to solve potential fault current levels. When an IBR is active, the relay sensing logic adjusts the **Plug Setting Multiplier (PSM)** to maintain a constant **Coordination Time Interval (CTI)**, preventing relay blindness and ensuring system stability.

---
**Developed by Abhay Sk & Antigravity AI**  
*Advanced Protection Systems Lab*
