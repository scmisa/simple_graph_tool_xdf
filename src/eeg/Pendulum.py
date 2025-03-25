import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Load data from Excel
data = pd.read_excel("data/Dane.xlsx")

# Extract D, t1, and t2 values from the Excel file
D = np.array(data["D"])  # Distance (meters)
t1 = np.array(data["t-1"])  # Time 1 (seconds) - 20 oscillations
t2 = np.array(data["t-2"])  # Time 2 (seconds) - 20 oscillations

D_calc = D[:-1]  # Skip the first two rows
t1_calc = t1[:-1]
t2_calc = t2[:-1]

# Calculate T as instructed: T = (t1 + t2) / 40
# T - period of one oscillation
# t1 - time for 20 oscillations
# t2 - time for 20 oscillations

T = (t1 + t2) / 40

T_calc = (t1_calc + t2_calc) / 40


# Calculate X and Y
# TODO: Add units to X and Y
# X = D², Y = D * T²
X = D**2
Y = D * (T**2)

# Calculate X and Y for the reduced dataset
X_calc = D_calc**2
Y_calc = D_calc * (T_calc**2)

# Units for X and Y
X_units = "m²"
Y_units = "m·s²"

# ----------------------------------------------------------------------

# Calculate Linear Regression using Least Squares Method

# Least Squares Regression
X_design = np.vstack([X, np.ones(len(X))]).T  # Design matrix
coefficients, residuals, _, _ = np.linalg.lstsq(X_design, Y, rcond=None)
A, B = coefficients
# ----------------------------------------------------------------------
# Least Squares Regression using the reduced dataset
# ----------------------------------------------------------------------

X_design_calc = np.vstack([X_calc, np.ones(len(X_calc))]).T  # Design matrix
coefficients, residuals, _, _ = np.linalg.lstsq(X_design_calc, Y_calc, rcond=None)
A, B = coefficients


# Units for A and B
A_units = f"{Y_units}/{X_units}"
B_units = Y_units


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
    u_g = (4 * np.pi**2 / A) * u_A
else:
    raise ValueError("Negative slope (A). Check data or model assumptions.")


# ----------------------------------------------------------------------
# Calculations for reduced dataset (without first two points) for g and its uncertainty (u_g)
# and for A and B with uncertainties (u_A and u_B)
# ----------------------------------------------------------------------

n_calc = len(X_calc)
if n_calc <= 2:
    raise ValueError("Not enough data points for uncertainty calculation.")

Y_fit_calc = A * X_calc + B
residuals_calc = Y_calc - Y_fit_calc
SSE_calc = np.sum(residuals_calc**2)

std_error_calc = np.sqrt(SSE_calc / (n_calc - 2))  # Degrees of freedom = n - 2
X_mean_calc = np.mean(X_calc)
denominator_calc = np.sum((X_calc - X_mean_calc) ** 2)

u_A = std_error_calc / np.sqrt(denominator_calc)
u_B = std_error_calc * np.sqrt(np.sum(X_calc**2) / (n_calc * denominator_calc))

if A > 0:
    g = (4 * np.pi**2) / A
    u_g = (4 * np.pi**2 / A) * u_A
else:
    raise ValueError("Negative slope (A). Check data or model assumptions.")

# ----------------------------------------------------------------------
# Calculate Moment of Inertia (moment_of_inertia) and its Uncertainty
# ----------------------------------------------------------------------
# moment_of_inertia = (m * g * D) / (4 * π²)
# mass
M = 0.783  # kg
U_M = 0.03  # kg +/-

moment_of_inertia = M * (B / A)
# Uncertainty in moment_of_inertia via error propagation
u_moment_of_inertia = moment_of_inertia * np.sqrt((u_A / A) ** 2 + (u_B / B) ** 2)
# Units
moment_of_inertia_units = "kg·m²"

# ----------------------------------------------------------------------
# Print Results with Uncertainties
# ----------------------------------------------------------------------
print(f"Slope (A): {A:.4f} ± {u_A:.4f}" + "s²/m")
print(f"Intercept (B): {B:.4f} ± {u_B:.4f}" + f" {B_units}")
print(f"Gravity (g): {g:.4f} ± {u_g:.4f} m/s²")
print(
    f"Moment of Inertia: {moment_of_inertia:.4f} ± {u_moment_of_inertia:.4f}" + "kg·m²"
)

# Plotting with all data points
plt.scatter(
    X[-1:], Y[-1:], color="orange", label="Punkt wykluczony z obliczeń"
)  # Excluded points
plt.scatter(
    X[:-1], Y[:-1], color="blue", label="Punkty uwzględnione w obliczeniach"
)  # Included points
plt.plot(X, A * X + B, color="red", label=f"Funkcja: Y = {A:.2f}X + {B:.2f}")
plt.title("Zależność X od Y")
plt.xlabel("X (m²)")
plt.ylabel("Y (m·s²)")
plt.legend()
plt.grid(True)
plt.show()


# TODO:
# - Jednostki dla X i Y, A i B
# - niepewność średnia
# - usunąć do obliczeń prostej regresji liniowej 2 pierwsze punkty
#  i zobaczyć jak wpłynie do na obliczenia
