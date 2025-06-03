import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load data from Excel file (in some columns there are formulas, so we use openpyxl engine)
# Using data_only=True to get calculated values instead of formulas
data1 = pd.read_excel(
    "data/Wzmacniacz.xlsx", sheet_name="bezCEbezR0", engine="openpyxl"
)
data2 = pd.read_excel("data/Wzmacniacz.xlsx", sheet_name="bezCEzR0", engine="openpyxl")
data3 = pd.read_excel("data/Wzmacniacz.xlsx", sheet_name="zCEzR0", engine="openpyxl")
data4 = pd.read_excel("data/Wzmacniacz.xlsx", sheet_name="zCEbezR0", engine="openpyxl")

# Columns are f - frequency [Hz], U-we - input voltage [V], U-wy - output voltage [V], K - gain, lg(f) - logarithm of frequency already in the data


# A plot is logarithm of frequency vs gain all data on one chart
def plot_all_gains_vs_frequency():
    plt.figure(figsize=(12, 8))

    # Plot all 4 datasets on the same chart
    # Using frequency (not log) with log scale on X axis, and gain in dB on Y axis
    plt.semilogx(
        data1["f"],
        20 * np.log10(data1["K"]),
        marker="o",
        linestyle="-",
        label="bez CE bez R0",
        linewidth=2,
    )
    plt.semilogx(
        data2["f"],
        20 * np.log10(data2["K"]),
        marker="s",
        linestyle="-",
        label="bez CE z R0",
        linewidth=2,
    )
    plt.semilogx(
        data3["f"],
        20 * np.log10(data3["K"]),
        marker="^",
        linestyle="-",
        label="z CE z R0",
        linewidth=2,
    )
    plt.semilogx(
        data4["f"],
        20 * np.log10(data4["K"]),
        marker="d",
        linestyle="-",
        label="z CE bez R0",
        linewidth=2,
    )

    plt.xlabel("Częstotliwość [Hz]", fontsize=12)
    plt.ylabel("K [dB]", fontsize=12)
    # plt.title("Frequency Response - Gain vs Frequency", fontsize=14, fontweight="bold")
    plt.grid(True, alpha=0.7, which="both")
    plt.legend(fontsize=10, loc="best")
    plt.tight_layout()
    plt.show()


# Call the function to display the plot
plot_all_gains_vs_frequency()
