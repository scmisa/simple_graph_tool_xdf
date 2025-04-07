import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Load the data focal length data from the Excel file
data1 = pd.read_excel(
    "data/focal-length.xlsx", sheet_name="pomn"
)  # measurments of focal length when image is smaller than the object
data2 = pd.read_excel(
    "data/focal-length.xlsx", sheet_name="pow"
)  # measurments of focal length when image is larger than the object

# Lens equation
# 1/f = 1/x + 1/y
# f = focal length
# x = object distance from the lens
# y = image distance from the lens
# 1/f focusing ability of the lens (Diopter)

# In both datasheets in columns x1 to x5 are the object distances in cm we need to take the average of them
# and then calculate the focal length

# Y is the image distance in cm and it is only one value in both datasheets
# X is the object distance in cm and it is the average of the values in columns x1 to x5

# l is the distance between the lens and the screen in cm it is in both datasheets

# x is the average of the values in columns x1 to x5
x_pomn = np.array(
    [
        data1["x1"],
        data1["x2"],
        data1["x3"],
        data1["x4"],
        data1["x5"],
    ]
)
x_pow = np.array(
    [
        data2["x1"],
        data2["x2"],
        data2["x3"],
        data2["x4"],
        data2["x5"],
    ]
)


# Calculate the average of the object distances
x_pomn = np.mean(x_pomn, axis=0)
x_pow = np.mean(x_pow, axis=0)
# Calculate the focal length
# f = l * x / (l - x)
l_pomn = np.array(data1["l"])
l_pow = np.array(data2["l"])
y_pomn = np.array(data1["y"])
y_pow = np.array(data2["y"])
# Calculate the focal length for the first datasheet
f_pomn = l_pomn * x_pomn / (l_pomn - x_pomn)
# Calculate the focal length for the second datasheet
f_pow = l_pow * x_pow / (l_pow - x_pow)

# Calculate the average of the focal lengths
f_pomn_avg = np.mean(f_pomn)
f_pow_avg = np.mean(f_pow)

# Calculate the standard deviation of the focal lengths
f_pomn_std = np.std(f_pomn)
f_pow_std = np.std(f_pow)

# Calculate the standard error of the mean of the focal lengths
f_pomn_sem = f_pomn_std / np.sqrt(len(f_pomn))
f_pow_sem = f_pow_std / np.sqrt(len(f_pow))

# Calculate the uncertainty of the focal lengths
f_pomn_uncertainty = f_pomn_sem * 1.96  # 95% confidence interval
f_pow_uncertainty = f_pow_sem * 1.96  # 95% confidence interval

# Print the results
# Wydrukuj wyniki
print("Ogniskowa dla pierwszego arkusza danych (obraz pomniejszony) (cm):")
print(f"Średnia: {f_pomn_avg:.2f} ± {f_pomn_uncertainty:.2f}")
print(f"Odchylenie standardowe: {f_pomn_std:.2f}")
print()
print("Ogniskowa dla drugiego arkusza danych (obraz powiększony) (cm):")
print(f"Średnia: {f_pow_avg:.2f} ± {f_pow_uncertainty:.2f}")
print(f"Odchylenie standardowe: {f_pow_std:.2f}")
print()
print("Zdolnosc skupiajaca (Dioptrie):")
print(f"Średnia: {1 / f_pomn_avg:.2f} ± {1 / f_pomn_uncertainty:.2f}")
print(f"Odchylenie standardowe: {1 / f_pomn_std:.2f}")
print()
