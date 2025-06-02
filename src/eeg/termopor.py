import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

data = pd.read_excel("data/TermOpor.xlsx")
# Data from the Excel file (T - temperature in Celsius, R - resistance in kOhms)
T = data["T"].values
R = data["R"].values  # R in kOhms


# Metoda najmniejszych kwadratów (jak REGLINP in Excel)
def least_squares_method(x, y):
    n = len(x)
    a = (n * np.sum(x * y) - np.sum(x) * np.sum(y)) / (
        n * np.sum(x**2) - (np.sum(x)) ** 2
    )
    b = (np.sum(y) - a * np.sum(x)) / n
    residuals = y - (a * x + b)
    std_dev = np.std(residuals)
    r = np.corrcoef(x, y)[0, 1]
    r_squared = r**2
    return a, b, std_dev, r, r_squared


# Calculate the regression parameters
a, b, std_dev, r, r_squared = least_squares_method(T, R)

# Print the regression statistics
print("\nStatystyki regresji:")
print(f"Nachylenie (a): {a:.4f}")
print(f"Przecięcie (b): {b:.4f}")
print(f"Niepewność standardowa u(a): {std_dev:.4f}")
print(f"Niepewność standardowa u(b): {std_dev:.4f}")
print(f"Współczynnik korelacji r: {r:.4f}")
print(f"Współczynnik determinacji r²: {r_squared:.4f}")

# Calculate temperature coefficient of electrical resistance α
# From R(T) = R₀(1 + α(T - T₀)) and linear regression R = aT + b
# We can derive: α = a/R₀
# Using T₀ = 0°C as reference, R₀ = b (resistance at 0°C)
T_ref = 0  # Reference temperature in °C
R_ref = b  # Resistance at reference temperature (from y-intercept)

# Calculate temperature coefficient α [1/°C]
alpha = a / R_ref

# Calculate uncertainty of α using error propagation
# u(α) = α * sqrt((u(a)/a)² + (u(b)/b)²)
u_a = std_dev  # Uncertainty in slope
u_b = std_dev  # Uncertainty in intercept
u_alpha = abs(alpha) * np.sqrt((u_a / a) ** 2 + (u_b / b) ** 2)

print(f"\nTemperaturowy współczynnik oporu elektrycznego:")
print(f"α = {alpha:.6f} ± {u_alpha:.6f} [1/°C]")
# print(f"α = ({alpha * 1000:.3f} ± {u_alpha * 1000:.3f}) × 10⁻³ [1/K]")

# Alternative calculation for different reference temperature (e.g., 20°C)
T_ref_alt = 20  # Alternative reference temperature
R_ref_alt = a * T_ref_alt + b  # Resistance at 20°C
alpha_alt = a / R_ref_alt
u_alpha_alt = abs(alpha_alt) * np.sqrt((u_a / a) ** 2 + (u_b / R_ref_alt) ** 2)

print(f"\nDla temperatury referencyjnej T₀ = {T_ref_alt}°C:")
print(f"R₀ = {R_ref_alt:.4f} kΩ")
print(f"α = {alpha_alt:.6f} ± {u_alpha_alt:.6f} [1/°C]")

# Define measurement uncertainties
delta_T = 1.0  # Temperature uncertainty ±1°C (typical for digital thermometer)
delta_R = 0.05  # Resistance uncertainty ±0.05 kOhm (based on multimeter precision)

# Plot the data and the regression line with uncertainty rectangles
plt.figure(figsize=(12, 8))

# Plot uncertainty rectangles for each measurement point
for i in range(len(T)):  # Create rectangle centered at each data point
    rect = patches.Rectangle(
        (T[i] - delta_T, R[i] - delta_R),  # Bottom-left corner
        2 * delta_T,  # Width (2 * uncertainty in T)
        2 * delta_R,  # Height (2 * uncertainty in R)
        linewidth=1,
        edgecolor="lightblue",
        facecolor="lightblue",
        alpha=1,
        label="Prostokąty niedokładności" if i == 0 else "",
    )
    plt.gca().add_patch(rect)

# Plot data points
plt.scatter(
    np.array(T), np.array(R), label="Dane pomiarowe", color="blue", s=50, zorder=5
)

# Plot regression line
T_line = np.linspace(min(T) - 5, max(T) + 5, 100)
R_line = a * T_line + b
plt.plot(
    T_line,
    R_line,
    label=f"Regresja liniowa: R = {a:.4f}T + {b:.4f}",
    color="red",
    linewidth=2,
    zorder=4,
)

# # Add text box with regression statistics
# textstr = f"""Statystyki regresji:
# Nachylenie a = {a:.4f} kΩ/°C
# Przecięcie b = {b:.4f} kΩ
# """

# props = dict(boxstyle="round", facecolor="wheat", alpha=0.8)
# plt.text(
#     0.02,
#     0.98,
#     textstr,
#     transform=plt.gca().transAxes,
#     fontsize=10,
#     verticalalignment="top",
#     bbox=props,
# )

plt.xlabel("Temperatura T (°C)", fontsize=12)
plt.ylabel("Oporność R (kΩ)", fontsize=12)
plt.title("Zależność oporności od temperatury", fontsize=14)
plt.legend(fontsize=10)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
