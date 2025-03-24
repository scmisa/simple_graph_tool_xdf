import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Load data from Excel
data = pd.read_excel("data/Dane.xlsx")

# Extract D, t1, and t2 values from the Excel file
D = np.array(data["D"])  # Distance (meters)
t1 = np.array(data["t-1"])  # Time 1 (seconds)
t2 = np.array(data["t-2"])  # Time 2 (seconds)

# ----------------------------------------------------------------------
# Step 1: Calculate T as instructed (T = (t1 + t2) / 40)
# ----------------------------------------------------------------------
T = (t1 + t2) / 40

# ----------------------------------------------------------------------
# Step 2: Verify Data Integrity
# ----------------------------------------------------------------------
# Ensure D is positive and increasing
if np.any(D <= 0):
    raise ValueError("D must be positive. Check your data.")

# Ensure t1 and t2 are positive and t2 > t1 (if they are start/end times)
if np.any(t1 <= 0) or np.any(t2 <= 0):
    raise ValueError("Times t1 and t2 must be positive.")

# ----------------------------------------------------------------------
# Step 3: Calculate X and Y
# ----------------------------------------------------------------------
X = D**2
Y = D * (T**2)

# ----------------------------------------------------------------------
# Step 4: Print Values for Debugging
# ----------------------------------------------------------------------
print("D (meters):", D)
print("t1 (seconds):", t1)
print("t2 (seconds):", t2)
print("T (seconds):", T)
print("X (D²):", X)
print("Y (D*T²):", Y)

# ----------------------------------------------------------------------
# Step 5: Least Squares Regression
# ----------------------------------------------------------------------
# Prepare design matrix
X_design = np.vstack([X, np.ones(len(X))]).T

# Perform linear regression
coefficients, _, _, _ = np.linalg.lstsq(X_design, Y, rcond=None)
A, B = coefficients

# ----------------------------------------------------------------------
# Step 6: Analyze Results
# ----------------------------------------------------------------------
if A > 0:
    g = (4 * np.pi**2) / A
    print(f"Slope (A): {A:.4f}")
    print(f"Intercept (B): {B:.4f}")
    print(f"Gravity (g): {g:.4f} m/s²")
else:
    print("ERROR: Negative slope detected. Possible causes:")
    print("- t1 and t2 are swapped (e.g., t1 > t2).")
    print("- Invalid model (Y should increase with X).")
    print("- Data entry errors (e.g., negative D or times).")

# ----------------------------------------------------------------------
# Step 7: Plot Data and Regression Line
# ----------------------------------------------------------------------
plt.scatter(X, Y, color="blue", label="Data Points")
plt.plot(X, A * X + B, color="red", label=f"Fit: Y = {A:.2f}X + {B:.2f}")
plt.xlabel("X (D²)")
plt.ylabel("Y (D·T²)")
plt.title("Linear Regression for Gravity Calculation")
plt.legend()
plt.grid(True)
plt.show()
