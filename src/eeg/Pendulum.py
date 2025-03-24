import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Load data from Excel
data = pd.read_excel("data/Dane.xlsx")

# Extract D, t1, and t2 values from the Excel file
D = np.array(data["D"])  # Distance (meters)
t1 = np.array(data["t-1"])  # Time 1 (seconds)
t2 = np.array(data["t-2"])  # Time 2 (seconds)

# Calculate T as instructed: T = (t1 + t2) / 40
T = (t1 + t2) / 40

# Calculate X and Y
X = D**2
Y = D * (T**2)

# Least Squares Regression
X_design = np.vstack([X, np.ones(len(X))]).T  # Design matrix
coefficients, residuals, _, _ = np.linalg.lstsq(X_design, Y, rcond=None)
A, B = coefficients

# ----------------------------------------------------------------------
# Calculate Uncertainties for A (slope) and B (intercept)
# ----------------------------------------------------------------------
n = len(X)
if n <= 2:
    raise ValueError("Not enough data points for uncertainty calculation.")

# Residuals and Sum of Squared Errors (SSE)
Y_fit = A * X + B
residuals = Y - Y_fit
SSE = np.sum(residuals**2)

# Standard Error of the Estimate
std_error = np.sqrt(SSE / (n - 2))  # Degrees of freedom = n - 2

# Uncertainty in Slope (A)
X_mean = np.mean(X)
denominator = np.sum((X - X_mean) ** 2)
u_A = std_error / np.sqrt(denominator)

# Uncertainty in Intercept (B)
u_B = std_error * np.sqrt(np.sum(X**2) / (n * denominator))

# ----------------------------------------------------------------------
# Calculate Gravity (g) and its Uncertainty
# ----------------------------------------------------------------------
if A > 0:
    g = (4 * np.pi**2) / A
    # Uncertainty in g via error propagation: u_g = (4π²/A²) * u_A
    u_g = (4 * np.pi**2 / A**2) * u_A
else:
    raise ValueError("Negative slope (A). Check data or model assumptions.")

# ----------------------------------------------------------------------
# Print Results with Uncertainties
# ----------------------------------------------------------------------
print(f"Slope (A): {A:.4f} ± {u_A:.4f}")
print(f"Intercept (B): {B:.4f} ± {u_B:.4f}")
print(f"Gravity (g): {g:.4f} ± {u_g:.4f} m/s²")

# Plotting
plt.scatter(X, Y, color="blue", label="Data Points")
plt.plot(X, A * X + B, color="red", label=f"Fit: Y = {A:.2f}X + {B:.2f}")
plt.xlabel("X (D²)")
plt.ylabel("Y (D·T²)")
plt.title("Linear Regression with Uncertainties")
plt.legend()
plt.grid(True)
plt.show()
