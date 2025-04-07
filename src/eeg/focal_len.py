import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit

# Wczytaj dane z Excela
data1 = pd.read_excel("data/focal-length.xlsx", sheet_name="pomn")
data2 = pd.read_excel("data/focal-length.xlsx", sheet_name="pow")

measurment_err = 0.1  # cm

# Oblicz średnie wartości x z pięciu pomiarów
x_pomn = np.mean([data1[f"x{i}"] for i in range(1, 6)], axis=0)
x_pow = np.mean([data2[f"x{i}"] for i in range(1, 6)], axis=0)

y_pomn = data1["y"]
y_pow = data2["y"]

# Oblicz ogniskowe f dla każdego pomiaru: 1/f = 1/x + 1/y
f_pomn = 1 / (1 / x_pomn + 1 / y_pomn)
f_pow = 1 / (1 / x_pow + 1 / y_pow)

# Średnie ogniskowe
avg_f_pomn = np.mean(f_pomn)
avg_f_pow = np.mean(f_pow)
f_avg = np.mean([avg_f_pomn, avg_f_pow])
f_err = measurment_err / np.sqrt(len(f_pomn) + len(f_pow))

print(f"Średnia ogniskowa: {f_avg:.2f} cm ± {f_err:.2f} cm")

# --- GRAFICZNE WYZNACZENIE OGNISKOWEJ ---


# Dopasuj proste y = ax + b do obu zbiorów danych
def lin(x, a, b):
    return a * x + b


params_pomn, _ = curve_fit(lin, x_pomn, y_pomn)
params_pow, _ = curve_fit(lin, x_pow, y_pow)

lin_pomn = lambda x: params_pomn[0] * x + params_pomn[1]
lin_pow = lambda x: params_pow[0] * x + params_pow[1]

# Oblicz punkt przecięcia prostych (x_fg, y_fg)
A1, B1 = params_pomn
A2, B2 = params_pow

x_fg = (B2 - B1) / (A1 - A2)
y_fg = lin_pomn(x_fg)
fg = (x_fg + y_fg) / 2
ufg = abs(x_fg - y_fg) / 2

print(f"Graficznie wyznaczona ogniskowa: {fg:.2f} cm ± {ufg:.2f} cm")

# WYKRES
x_min = min(np.min(x_pomn), np.min(x_pow)) - 5
x_max = max(np.max(x_pomn), np.max(x_pow)) + 5
y_min = min(np.min(y_pomn), np.min(y_pow)) - 5
y_max = max(np.max(y_pomn), np.max(y_pow)) + 5

x_vals = np.linspace(x_min, x_max, 500)

plt.figure(figsize=(8, 6))
plt.scatter(x_pomn, y_pomn, color="blue", label="Obraz pomniejszony")
plt.scatter(x_pow, y_pow, color="red", label="Obraz powiększony")
plt.plot(x_vals, lin_pomn(x_vals), "b--")
plt.plot(x_vals, lin_pow(x_vals), "r--")
plt.scatter(
    [x_fg], [y_fg], color="black", marker="x", s=100, label=f"$f_n$ = {fg:.2f} cm"
)

plt.xlabel("x [cm] (odległość przedmiotu)")
plt.ylabel("y [cm] (odległość obrazu)")
plt.title("Graficzne wyznaczanie ogniskowej")
plt.grid(True)
plt.legend()
plt.xlim(x_min, x_max)
plt.ylim(y_min, y_max)
plt.gca().set_aspect("equal", adjustable="box")
plt.tight_layout()
plt.show()
