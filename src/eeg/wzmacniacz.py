import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Wczytywanie danych
data1 = pd.read_excel(
    "data/Wzmacniacz.xlsx", sheet_name="bezCEbezR0", engine="openpyxl"
)
data2 = pd.read_excel("data/Wzmacniacz.xlsx", sheet_name="bezCEzR0", engine="openpyxl")
data3 = pd.read_excel("data/Wzmacniacz.xlsx", sheet_name="zCEzR0", engine="openpyxl")
data4 = pd.read_excel("data/Wzmacniacz.xlsx", sheet_name="zCEbezR0", engine="openpyxl")


def interpolacja_3dB(data, K_3dB):
    """Interpoluje częstotliwości przy których K = K_3dB."""
    data = data.sort_values("f")  # Sortujemy po częstotliwości
    f_vals = data["f"].values
    K_vals = data["K"].values

    fd, fg = None, None

    for i in range(1, len(K_vals)):
        if K_vals[i - 1] < K_3dB <= K_vals[i]:
            fd = np.interp(
                K_3dB, [K_vals[i - 1], K_vals[i]], [f_vals[i - 1], f_vals[i]]
            )
        elif K_vals[i - 1] >= K_3dB > K_vals[i]:
            fg = np.interp(
                K_3dB, [K_vals[i - 1], K_vals[i]], [f_vals[i - 1], f_vals[i]]
            )

    return fd, fg


def oblicz_pasmo_przenoszenia(data):
    """
    Oblicza pasmo przenoszenia wzmacniacza na podstawie interpolacji -3 dB.
    """
    if data.empty or "K" not in data.columns or "f" not in data.columns:
        print("Brak danych do obliczenia pasma przenoszenia")
        return 0, 0, 0

    K_max = data["K"].max()
    K_3dB = K_max / np.sqrt(2)

    fd, fg = interpolacja_3dB(data, K_3dB)

    if fd is None or fg is None:
        print("Nie udało się interpolować granic pasma (-3 dB)")
        return 0, 0, 0

    pasmo = fg - fd
    return pasmo, fg, fd


def analiza_charakterystyk():
    dane = {
        "bezCEbezR0": data1,
        "bezCEzR0": data2,
        "zCEzR0": data3,
        "zCEbezR0": data4,
    }

    for nazwa, dane_wzmacniacza in dane.items():
        pasmo, fg, fd = oblicz_pasmo_przenoszenia(dane_wzmacniacza)
        print(f"=== {nazwa} ===")
        print(f"Pasmo przenoszenia: {pasmo:.2f} Hz (od {fd:.2f} Hz do {fg:.2f} Hz)")
        print()

        # Opcjonalny wykres
        plt.plot(dane_wzmacniacza["f"], dane_wzmacniacza["K"], label=nazwa)

    plt.xscale("log")
    plt.xlabel("Częstotliwość [Hz]")
    plt.ylabel("Wzmocnienie [K]")
    plt.title("Charakterystyki częstotliwościowe wzmacniaczy")
    plt.legend()
    plt.grid(True, which="both", ls="--", lw=0.5)
    plt.show()


# Uruchomienie analizy
analiza_charakterystyk()
