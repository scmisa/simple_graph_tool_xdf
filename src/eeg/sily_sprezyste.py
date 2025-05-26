import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def load_spring_data():
    """Załaduj dane pomiarowe z pliku Excel."""
    dataA = pd.read_excel("data/Sily_sprezyste.xlsx", sheet_name="MetodaA")
    dataB = pd.read_excel("data/Sily_sprezyste.xlsx", sheet_name="MetodaB")
    return dataA, dataB

def Smallest_square(x, y):
    """
    Oblicz parametry prostej regresji liniowej metodą najmniejszych kwadratów.
    
    Parametry:
    -----------
    x : array-like
        Dane zmiennej niezależnej
    y : array-like
        Dane zmiennej zależnej
        
    Zwraca:
    --------
    a : float
        Nachylenie prostej regresji
    b : float
        Przecięcie z osią Y
    std_dev : float
        Odchylenie standardowe reszt
    r : float
        Współczynnik korelacji
    r_squared : float
        Współczynnik determinacji
    """    
    n = len(x)
    a = (n * np.sum(x * y) - np.sum(x) * np.sum(y)) / (n * np.sum(x**2) - (np.sum(x))**2)
    b = (np.sum(y) - a * np.sum(x)) / n  # Oblicz parametry statystyczne
    residuals = y - (a * x + b)
    std_dev = np.std(residuals)
    r = np.corrcoef(x, y)[0, 1]
    r_squared = r**2
    
    # Wyświetl statystyki regresji
    print("\nStatystyki regresji:")
    print(f"Nachylenie (a): {a:.4f}")
    print(f"Przecięcie (b): {b:.4f}")
    print(f"Niepewność standardowa u(a): {std_dev:.4f}")
    print(f"Niepewność standardowa u(b): {std_dev:.4f}")
    
    return a, b, std_dev, r, r_squared

def plt_spring_A(data):
    L_0 = data["L_0"].iloc[0] / 1000  # początkowa długość sprężyny [mm] -> [m]
    M = data["M"]  # masa obciążenia [g]
    M = M / 1000  # przelicz na kg
    L = data["L"]  # długość sprężyny [m]
    g = 9.81  # przyspieszenie ziemskie [m/s^2]
    
    # Wykonaj regresję: M vs L
    a, b, std_dev, r, r_squared = Smallest_square(M, L)
    
    # Oblicz stałą sprężyny k
    # Z prawa Hooke'a: F = k * (L - L_0), oraz F = M * g
    # Więc: M * g = k * (L - L_0)
    # Przekształcając: L = (g/k) * M + L_0
    # Stąd: a = g/k, więc k = g/a
    k = g / a  # stała sprężyny [N/m] (a jest w m/kg, więc k jest już w N/m)    
    # Upewnij się, że wartości są skalarne
    if hasattr(a, 'iloc'):
        a = a.iloc[0] if len(a) > 0 else float(a)
    if hasattr(k, 'iloc'):
        k = k.iloc[0] if len(k) > 0 else float(k)
    if hasattr(std_dev, 'iloc'):
        std_dev = std_dev.iloc[0] if len(std_dev) > 0 else float(std_dev)
    
    print(f"Nachylenie a (m/kg): {a:.4f}")
    print(f"Stała sprężyny k: {k:.4f} N/m")
    
    # Oblicz niepewność stałej sprężyny
    u_k = (k * std_dev) / a  # niepewność stałej sprężyny [N/m]
    print(f"Niepewność stałej sprężyny u(k): {u_k:.4f} N/m")

    # Sprawdź czy L_0 odpowiada przecięciu z osią Y
    if abs(L_0 - b) <= 3 * std_dev:
        print(f"L_0 = {L_0:.4f} m odpowiada przecięciu y b = {b:.4f} ± {3 * std_dev:.4f} m")
    else:
        print(f"L_0 = {L_0:.4f} m nie odpowiada przecięciu y b = {b:.4f} m")
    
    # Narysuj punkty pomiarowe i prostą regresji
    plt.figure(figsize=(10, 6))
    plt.scatter(M, L, color='blue', label='Punkty pomiarowe')
    plt.plot(M, a * M + b, color='red', label='Prosta regresji')
    plt.title('Długość sprężyny w funkcji masy (Metoda A)')
    plt.xlabel('Masa (kg)')
    plt.ylabel('Długość sprężyny (m)')
    plt.grid()
    plt.legend()
    plt.show()


def plt_spring_B(data):
    M = data["M"]  # masa obciążenia [g]
    M = M / 1000  # przelicz na kg
    t1 = data["t1"]  # czas t1 [s]
    t2 = data["t2"]  # czas t2 [s]
    T = data["T"]  # okres [s]    # Metoda B: Badanie zaleznosci okresu drgań od masy zawieszonej na sprężynie
    a, b, std_dev, r, r_squared = Smallest_square(M, T)
    
    # Upewnij się, że wartości są skalarne
    if hasattr(a, 'iloc'):
        a = a.iloc[0] if len(a) > 0 else float(a)
    if hasattr(b, 'iloc'):
        b = b.iloc[0] if len(b) > 0 else float(b)
    if hasattr(std_dev, 'iloc'):
        std_dev = std_dev.iloc[0] if len(std_dev) > 0 else float(std_dev)
    
    # Oblicz stałą sprężyny k dla każdego pomiaru
    # Z wzoru na okres: T = 2 * pi * sqrt(m/k), więc k = (4 * pi^2 * m) / T^2
    k_values = (4 * np.pi**2 * M) / T**2  # stała sprężyny dla każdego pomiaru [N/kg]
    
    print(f"Nachylenie a (s/kg): {a:.4f}")
    
    # Oblicz średnią arytmetyczną stałej sprężyny k
    k_mean = np.mean(k_values)
    print(f"Średnia arytmetyczna stałej sprężyny k: {k_mean:.4f} N/kg")
    
    # Oblicz niepewność stałej sprężyny
    k_std = np.std(k_values)
    print(f"Odchylenie standardowe stałej sprężyny: {k_std:.4f} N/kg")

    # Niepewność okresu delta_T przyjąć 0,4s/20
    delta_T = 0.4 / 20  # niepewność okresu [s]
    print(f"Niepewność okresu delta_T: {delta_T:.4f} s")

    # Sprawdź czy średni okres T odpowiada przecięciu z osią Y
    T_mean = T.mean()
    if abs(T_mean - b) <= 3 * std_dev:
        print(f"Średni okres T = {T_mean:.4f} s odpowiada przecięciu y b = {b:.4f} ± {3 * std_dev:.4f} s")
    else:
        print(f"Średni okres T = {T_mean:.4f} s nie odpowiada przecięciu y b = {b:.4f} s")

    # Narysuj punkty pomiarowe i prostą regresji
    plt.figure(figsize=(10, 6))
    plt.scatter(M, T, color='blue', label='Punkty pomiarowe')
    plt.plot(M, a * M + b, color='red', label='Prosta regresji')
    plt.title('Okres drgań w funkcji masy (Metoda B)')
    plt.xlabel('Masa (kg)')
    plt.ylabel('Okres drgań (s)')
    plt.grid()
    plt.legend()
    plt.show()

if __name__ == "__main__":
    dataA, dataB = load_spring_data()
    plt_spring_A(dataA)

    plt_spring_B(dataB)