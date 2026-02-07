"""
ML Model for Relay Protection (Numpy Implementation).
A simple 2-layer MLP to predict Is and TMS.
"""

import numpy as np
import csv

class RelayMLP:
    def __init__(self, input_dim=4, hidden_dim=8, output_dim=2):
        self.W1 = np.random.randn(input_dim, hidden_dim) * 0.1
        self.b1 = np.zeros((1, hidden_dim))
        self.W2 = np.random.randn(hidden_dim, output_dim) * 0.1
        self.b2 = np.zeros((1, output_dim))

    def relu(self, x):
        return np.maximum(0, x)

    def forward(self, X):
        self.z1 = np.dot(X, self.W1) + self.b1
        self.a1 = self.relu(self.z1)
        self.z2 = np.dot(self.a1, self.W2) + self.b2
        return self.z2

    def train(self, X, y, lr=0.001, epochs=1000):
        loss_history = []
        for epoch in range(epochs):
            # Forward
            z1 = np.dot(X, self.W1) + self.b1
            a1 = np.maximum(0, z1)
            z2 = np.dot(a1, self.W2) + self.b2
            
            # Loss (MSE)
            loss = np.mean((z2 - y) ** 2)
            loss_history.append(loss)
            
            # Backward
            dz2 = 2 * (z2 - y) / X.shape[0]
            dW2 = np.dot(a1.T, dz2)
            db2 = np.sum(dz2, axis=0, keepdims=True)
            
            da1 = np.dot(dz2, self.W2.T)
            dz1 = da1 * (z1 > 0)
            dW1 = np.dot(X.T, dz1)
            db1 = np.sum(dz1, axis=0, keepdims=True)
            
            # Update
            self.W1 -= lr * dW1
            self.b1 -= lr * db1
            self.W2 -= lr * dW2
            self.b2 -= lr * db2
            
            if epoch % 200 == 0:
                print(f"Epoch {epoch}, Loss: {loss:.6f}")
        
        # Save loss plot
        try:
            import matplotlib.pyplot as plt
            plt.figure()
            plt.plot(loss_history)
            plt.title("ML Training Loss (MSE)")
            plt.xlabel("Epoch")
            plt.ylabel("Loss")
            plt.yscale('log')
            plt.grid(True)
            plt.savefig("ml_training_loss.png")
        except:
            pass

def load_data(filepath):
    X, y = [], []
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Features: i_load, i_grid, i_ibr_potential, ibr_active
            X.append([
                float(row['i_load']),
                float(row['i_grid']),
                float(row['i_ibr_potential']),
                float(row['ibr_active'])
            ])
            # Labels: is_pickup_target, tms_target
            y.append([
                float(row['is_pickup_target']),
                float(row['tms_target'])
            ])
    return np.array(X), np.array(y)

if __name__ == "__main__":
    X, y = load_data("relay_training_data.csv")
    
    # Simple Scaling
    X_mean, X_std = X.mean(axis=0), X.std(axis=0)
    y_mean, y_std = y.mean(axis=0), y.std(axis=0)
    
    X_scaled = (X - X_mean) / X_std
    y_scaled = (y - y_mean) / y_std
    
    model = RelayMLP()
    model.train(X_scaled, y_scaled, lr=0.01, epochs=2000)
    
    # Save model "weights"
    np.savez("relay_mlp_weights.npz", W1=model.W1, b1=model.b1, W2=model.W2, b2=model.b2, 
             X_mean=X_mean, X_std=X_std, y_mean=y_mean, y_std=y_std)
    print("Model trained and weights saved.")
