import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Load data from Excel file
data1 = pd.read_excel(
    "data/Wzmacniacz.xlsx", sheet_name="bezCEbezR0", engine="openpyxl"
)
data2 = pd.read_excel("data/Wzmacniacz.xlsx", sheet_name="bezCEzR0", engine="openpyxl")
data3 = pd.read_excel("data/Wzmacniacz.xlsx", sheet_name="zCEzR0", engine="openpyxl")
data4 = pd.read_excel("data/Wzmacniacz.xlsx", sheet_name="zCEbezR0", engine="openpyxl")


def oblicz_pasmo_przenoszenia(data):
    """
    Oblicza pasmo przenoszenia wzmacniacza.
    Pasmo przenoszenia to zakres częstotliwości między punktami -3dB.
    """
    if data.empty or "K" not in data.columns or "f" not in data.columns:
        return 0.0, 0.0, 0.0

    # Konwertuj na float i usuń NaN
    f_values = pd.to_numeric(data["f"], errors="coerce").dropna()
    K_values = pd.to_numeric(data["K"], errors="coerce").dropna()

    if len(f_values) == 0 or len(K_values) == 0:
        return 0.0, 0.0, 0.0

    # Znajdź maksymalne wzmocnienie
    K_max = float(K_values.max())
    K_3dB = K_max / np.sqrt(2)

    # Utwórz clean dataframe
    clean_data = pd.DataFrame(
        {"f": f_values[: len(K_values)], "K": K_values[: len(f_values)]}
    ).sort_values("f")

    # Znajdź punkt maksymalny
    idx_max = clean_data["K"].idxmax()
    f_max = float(clean_data.loc[idx_max, "f"])

    # Znajdź granice pasma
    left_data = clean_data[clean_data["f"] < f_max]
    right_data = clean_data[clean_data["f"] > f_max]

    if not left_data.empty:
        left_diff = np.abs(left_data["K"] - K_3dB)
        f0_idx = left_diff.idxmin()
        f0 = float(left_data.loc[f0_idx, "f"])
    else:
        f0 = float(clean_data["f"].min())

    if not right_data.empty:
        right_diff = np.abs(right_data["K"] - K_3dB)
        f1_idx = right_diff.idxmin()
        f1 = float(right_data.loc[f1_idx, "f"])
    else:
        f1 = float(clean_data["f"].max())

    pasmo_szerokość = f1 - f0
    return pasmo_szerokość, f1, f0


def analiza_charakterystyk():
    """Analiza charakterystyk wszystkich konfiguracji"""
    konfiguracje = [
        (data1, "bez CE bez R0"),
        (data2, "bez CE z R0"),
        (data3, "z CE z R0"),
        (data4, "z CE bez R0"),
    ]

    print("=" * 60)
    print("ANALIZA CHARAKTERYSTYK WZMACNIACZA")
    print("=" * 60)

    for data, nazwa in konfiguracje:
        print(f"\n{nazwa}:")
        print("-" * 40)

        # Konwertuj na float
        K_values = pd.to_numeric(data["K"], errors="coerce")
        f_values = pd.to_numeric(data["f"], errors="coerce")

        K_max = float(K_values.max())
        K_min = float(K_values.min())
        f_at_max = float(f_values.iloc[K_values.idxmax()])

        print(f"Maksymalne wzmocnienie: {K_max:.3f} ({20 * np.log10(K_max):.1f} dB)")
        print(f"Minimalne wzmocnienie: {K_min:.3f} ({20 * np.log10(K_min):.1f} dB)")
        print(f"Częstotliwość przy max. wzmocnieniu: {f_at_max:.1f} Hz")

        pasmo_szer, f1, f0 = oblicz_pasmo_przenoszenia(data)
        if pasmo_szer > 0:
            print(f"Pasmo przenoszenia (-3dB): {pasmo_szer:.1f} Hz")
            print(f"Dolna częstotliwość graniczna: {f0:.1f} Hz")
            print(f"Górna częstotliwość graniczna: {f1:.1f} Hz")


def porownanie_konfiguracji():
    """Porównuje różne konfiguracje wzmacniacza"""
    konfiguracje = {
        "bez CE bez R0": data1,
        "bez CE z R0": data2,
        "z CE z R0": data3,
        "z CE bez R0": data4,
    }

    print("\n" + "=" * 60)
    print("PORÓWNANIE KONFIGURACJI")
    print("=" * 60)

    wyniki = []
    for nazwa, data in konfiguracje.items():
        K_values = pd.to_numeric(data["K"], errors="coerce")
        K_max = float(K_values.max())
        K_max_dB = 20 * np.log10(K_max)
        pasmo_szer, f1, f0 = oblicz_pasmo_przenoszenia(data)

        wyniki.append(
            {
                "Konfiguracja": nazwa,
                "Max K": f"{K_max:.3f}",
                "Max K [dB]": f"{K_max_dB:.1f}",
                "Pasmo [Hz]": f"{pasmo_szer:.1f}" if pasmo_szer > 0 else "N/A",
                "f0 [Hz]": f"{f0:.1f}" if f0 > 0 else "N/A",
                "f1 [Hz]": f"{f1:.1f}" if f1 > 0 else "N/A",
            }
        )

    # Wyświetlenie tabeli
    print(
        f"{'Konfiguracja':<15} {'Max K':<8} {'Max K [dB]':<10} {'Pasmo [Hz]':<10} {'f0 [Hz]':<8} {'f1 [Hz]':<8}"
    )
    print("-" * 70)
    for wynik in wyniki:
        print(
            f"{wynik['Konfiguracja']:<15} {wynik['Max K']:<8} {wynik['Max K [dB]']:<10} {wynik['Pasmo [Hz]']:<10} {wynik['f0 [Hz]']:<8} {wynik['f1 [Hz]']:<8}"
        )


def plot_clean_comparison():
    """Czytelny wykres porównawczy z oznaczeniem pasm"""
    plt.figure(figsize=(14, 10))

    datasets = [
        (data1, "bez CE bez R0", "o", "#1f77b4"),
        (data2, "bez CE z R0", "s", "#ff7f0e"),
        (data3, "z CE z R0", "^", "#2ca02c"),
        (data4, "z CE bez R0", "d", "#d62728"),
    ]

    # Najpierw narysuj wszystkie krzywe
    for data, label, marker, color in datasets:
        f_vals = pd.to_numeric(data["f"], errors="coerce")
        K_vals = pd.to_numeric(data["K"], errors="coerce")

        plt.semilogx(
            f_vals,
            20 * np.log10(K_vals),
            marker=marker,
            linestyle="-",
            label=label,
            linewidth=2.5,
            color=color,
            markersize=6,
            markerfacecolor=color,
            markeredgecolor="white",
            markeredgewidth=0.5,
        )

    # Dodaj oznaczenia pasm dla każdej konfiguracji
    y_positions = [5, 10, 15, 20]  # Różne pozycje Y dla etykiet

    for i, (data, label, _, color) in enumerate(datasets):
        pasmo_szer, f1, f0 = oblicz_pasmo_przenoszenia(data)

        if f0 > 0 and f1 > 0 and pasmo_szer > 0:
            # Dodaj cienkie pionowe linie
            plt.axvline(f0, color=color, linestyle="--", linewidth=1, alpha=0.6)
            plt.axvline(f1, color=color, linestyle="--", linewidth=1, alpha=0.6)

            # Dodaj poziomą linię -3dB w zakresie pasma
            K_vals = pd.to_numeric(data["K"], errors="coerce")
            K_max = float(K_vals.max())
            y_3dB = 20 * np.log10(K_max / np.sqrt(2))

            plt.hlines(
                y_3dB, f0, f1, colors=color, linestyles=":", linewidth=2, alpha=0.7
            )

            # Etykieta pasma
            mid_f = np.sqrt(f0 * f1)
            plt.annotate(
                f"BW: {pasmo_szer:.0f}Hz",
                xy=(mid_f, y_positions[i]),
                xytext=(0, 0),
                textcoords="offset points",
                bbox=dict(boxstyle="round,pad=0.3", facecolor=color, alpha=0.7),
                fontsize=9,
                color="white",
                weight="bold",
                ha="center",
            )

    plt.xlabel("Częstotliwość [Hz]", fontsize=14, weight="bold")
    plt.ylabel("Wzmocnienie K [dB]", fontsize=14, weight="bold")
    plt.title(
        "Charakterystyka częstotliwościowa wzmacniacza\nz oznaczeniem pasm przenoszenia (-3dB)",
        fontsize=16,
        fontweight="bold",
        pad=20,
    )

    plt.grid(True, alpha=0.3, which="both")
    plt.legend(loc="upper right", fontsize=11, frameon=True, fancybox=True, shadow=True)
    plt.tight_layout()
    plt.show()


def plot_individual_configs():
    """Osobne wykresy dla każdej konfiguracji"""
    datasets = [
        (data1, "bez CE bez R0", "o", "#1f77b4"),
        (data2, "bez CE z R0", "s", "#ff7f0e"),
        (data3, "z CE z R0", "^", "#2ca02c"),
        (data4, "z CE bez R0", "d", "#d62728"),
    ]

    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle(
        "Charakterystyki częstotliwościowe wzmacniacza", fontsize=16, fontweight="bold"
    )

    axes = axes.flatten()

    for idx, (data, label, marker, color) in enumerate(datasets):
        ax = axes[idx]

        f_vals = pd.to_numeric(data["f"], errors="coerce")
        K_vals = pd.to_numeric(data["K"], errors="coerce")

        ax.semilogx(
            f_vals,
            20 * np.log10(K_vals),
            marker=marker,
            linestyle="-",
            label=label,
            linewidth=2.5,
            color=color,
            markersize=6,
        )

        # Pasmo przenoszenia
        pasmo_szer, f1, f0 = oblicz_pasmo_przenoszenia(data)
        if f0 > 0 and f1 > 0:
            K_max = float(K_vals.max())
            y_3dB = 20 * np.log10(K_max / np.sqrt(2))

            ax.axvline(
                f0,
                color=color,
                linestyle="--",
                linewidth=2,
                alpha=0.8,
                label=f"f0 = {f0:.0f} Hz",
            )
            ax.axvline(
                f1,
                color=color,
                linestyle="--",
                linewidth=2,
                alpha=0.8,
                label=f"f1 = {f1:.0f} Hz",
            )
            ax.axhline(
                y_3dB,
                color="red",
                linestyle=":",
                linewidth=2,
                alpha=0.8,
                label=f"-3dB = {y_3dB:.1f} dB",
            )
            ax.axvspan(
                f0, f1, alpha=0.2, color=color, label=f"BW = {pasmo_szer:.0f} Hz"
            )

        ax.set_xlabel("Częstotliwość [Hz]", fontsize=12)
        ax.set_ylabel("Wzmocnienie K [dB]", fontsize=12)
        ax.set_title(label, fontsize=14, fontweight="bold")
        ax.grid(True, alpha=0.3, which="both")
        ax.legend(fontsize=9, loc="best")

    plt.tight_layout()
    plt.show()


def zapisz_wyniki_do_pliku():
    """Zapisuje wyniki analizy do pliku"""
    # Utwórz folder jeśli nie istnieje
    os.makedirs("Reports/Wzmacniacz", exist_ok=True)

    with open("Reports/Wzmacniacz/analiza_wyniki.txt", "w", encoding="utf-8") as f:
        f.write("ANALIZA CHARAKTERYSTYK WZMACNIACZA\n")
        f.write("=" * 60 + "\n\n")

        konfiguracje = [
            (data1, "bez CE bez R0"),
            (data2, "bez CE z R0"),
            (data3, "z CE z R0"),
            (data4, "z CE bez R0"),
        ]

        for data, nazwa in konfiguracje:
            f.write(f"{nazwa}:\n")
            f.write("-" * 40 + "\n")

            K_values = pd.to_numeric(data["K"], errors="coerce")
            f_values = pd.to_numeric(data["f"], errors="coerce")

            K_max = float(K_values.max())
            K_min = float(K_values.min())
            f_at_max = float(f_values.iloc[K_values.idxmax()])

            f.write(
                f"Maksymalne wzmocnienie: {K_max:.3f} ({20 * np.log10(K_max):.1f} dB)\n"
            )
            f.write(
                f"Minimalne wzmocnienie: {K_min:.3f} ({20 * np.log10(K_min):.1f} dB)\n"
            )
            f.write(f"Częstotliwość przy max. wzmocnieniu: {f_at_max:.1f} Hz\n")

            pasmo_szer, f1, f0 = oblicz_pasmo_przenoszenia(data)
            if pasmo_szer > 0:
                f.write(f"Pasmo przenoszenia (-3dB): {pasmo_szer:.1f} Hz\n")
                f.write(f"Dolna częstotliwość graniczna: {f0:.1f} Hz\n")
                f.write(f"Górna częstotliwość graniczna: {f1:.1f} Hz\n")
            f.write("\n")

    print("Wyniki zapisane do pliku: Reports/Wzmacniacz/analiza_wyniki.txt")


if __name__ == "__main__":
    # Przeprowadź analizę
    analiza_charakterystyk()
    porownanie_konfiguracji()

    # Zapisz wyniki
    try:
        zapisz_wyniki_do_pliku()
    except Exception as e:
        print(f"Nie udało się zapisać wyników: {e}")

    # Wykresy
    print("\nWyświetlanie czytelnego wykresu porównawczego...")
    plot_clean_comparison()

    print("\nWyświetlanie osobnych wykresów...")
    plot_individual_configs()
