import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def load_thermocouple_data():
    """Load measurement data from Excel file."""
    water_data = pd.read_excel("data/Termopara.xlsx", sheet_name="metoda1")
    wood_data = pd.read_excel("data/Termopara.xlsx", sheet_name="metoda2")
    return water_data, wood_data

def calculate_linear_regression(x, y):
    """
    Calculate linear regression parameters using the least squares method.
    
    Parameters:
    -----------
    x : array-like
        Independent variable data
    y : array-like
        Dependent variable data
        
    Returns:
    --------
    a : float
        Slope of the regression line
    b : float
        Y-intercept of the regression line
    std_dev : float
        Standard deviation of residuals
    r : float
        Correlation coefficient
    r_squared : float
        Coefficient of determination
    """
    n = len(x)
    a = (n * np.sum(x * y) - np.sum(x) * np.sum(y)) / (n * np.sum(x**2) - (np.sum(x))**2)
    b = (np.sum(y) - a * np.sum(x)) / n    # Calculate statistical parameters
    residuals = y - (a * x + b)
    std_dev = np.std(residuals)
    r = np.corrcoef(x, y)[0, 1]
    r_squared = r**2
    
    # Print regression statistics
    print("\nRegression Statistics:")
    print(f"Slope (a): {a:.4f}")
    print(f"Intercept (b): {b:.4f}")
    print(f"Standard uncertainty u(a): {std_dev:.4f}")
    print(f"Standard uncertainty u(b): {std_dev:.4f}")
    
    return a, b, std_dev, r, r_squared


def calculate_melting_temperature(U_0, a, std_dev):
    """
    Calculate the melting temperature and its uncertainty.
    
    Parameters:
    -----------
    U_0 : float
        Average voltage at melting point [mV]
    a : float
        Slope of the regression line
    std_dev : float
        Standard deviation (uncertainty of parameters)
        
    Returns:
    --------
    T : float
        Melting temperature [°C]
    u_T : float
        Uncertainty of the melting temperature [°C]
    """
    # Convert mV to µV for calculation
    U_0_microvolts = U_0 * 1000
    
    # Thermocouple sensitivity (k = 41 µV/°C)
    k = 41
    
    # Calculate temperature
    T = U_0_microvolts / k
    
    # Calculate uncertainty (convert to °C)
    u_T = np.sqrt((U_0 * std_dev)**2 + (a * std_dev)**2 + std_dev**2) * 1000 / k
    
    return T, u_T

def plot_water_heating_curve(data):
    """Plot the thermoelectric force vs. water heating time."""
    plt.figure(figsize=(10, 6))
    plt.title("Zależność siły termoelektrycznej od temperatury podgrzewania wody")
    plt.xlabel("t [s]")
    plt.ylabel("U [mV]")
    plt.grid(True)
    plt.axhline(0, color='black', lw=0.5)
    plt.axvline(0, color='black', lw=0.5)
    plt.plot(data["T"], data["mV"], 'o', label="Pomiary")
    plt.legend()
    plt.show()

def plot_wood_alloy_curve(data, regression_params, point_times, point_voltages):
    """Plot the Wood's alloy measurements with regression line and annotations."""
    a, b = regression_params[:2]
    
    plt.figure(figsize=(10, 6))
    # Plot regression line
    x = np.linspace(min(data["T"]), max(data["T"]), 1000)
    y = a * x + b
    plt.plot(x, y, label="Regresja liniowa", color="red")
    
    # Plot measurement points
    plt.plot(data["T"], data["mA"], 'o', label="Pomiary")
    
    # Add annotations for specific points
    for i, (t, U) in enumerate(zip(point_times, point_voltages), 1):
        plt.annotate(f'U₍{i}₎ = {U:.2f} mA',
                    xy=(t, U),
                    xytext=(min(data["T"]) + 50, U),
                    textcoords='data',
                    arrowprops=dict(facecolor='black', arrowstyle='->'),
                    ha='left')
    
    plt.title("Termopara dla stopu Wooda z regresją liniową")
    plt.xlabel("t [s]")
    plt.ylabel("U [mA]")
    plt.grid(True)
    plt.axhline(0, color='black', lw=0.5)
    plt.axvline(0, color='black', lw=0.5)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    # Load data
    water_data, wood_data = load_thermocouple_data()
    
    # Define measurement points
    point_times = [640, 1080]  # Time points of interest
    point_voltages = [wood_data.loc[wood_data["T"] == t, "mA"].values[0] for t in point_times]
    
    # Plot water heating measurements
    plot_water_heating_curve(water_data)
    
    # Calculate regression parameters for Wood's alloy measurements
    regression_params = calculate_linear_regression(wood_data["T"], wood_data["mA"])
      # Calculate melting temperature and uncertainty
    U_0 = np.mean(point_voltages)  # Average voltage at melting points
    T, u_T = calculate_melting_temperature(U_0, regression_params[0], regression_params[2])
    
    # Print melting temperature results
    print(f"\nMelting Temperature Analysis:")
    print(f"Average voltage (U₀): {U_0:.2f} mV")
    print(f"Temperature: {T:.1f} °C")
    print(f"Uncertainty u(T): {u_T:.1f} °C")
    print(f"Final result: T = ({T:.1f} ± {u_T:.1f}) °C")# Plot Wood's alloy measurements
    plot_wood_alloy_curve(wood_data, regression_params, point_times, point_voltages)