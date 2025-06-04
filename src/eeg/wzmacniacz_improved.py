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

# Columns are f - frequency [Hz], U-we - input voltage [V], U-wy - output voltage [V],
# K - gain, lg(f) - logarithm of frequency already in the data


def oblicz_pasmo_przenoszenia(data):
    """
    Oblicza pasmo przenoszenia wzmacniacza.
    Pasmo przenoszenia to zakres częstotliwości między punktami -3dB,
    gdzie wzmocnienie spada do Kmax/√2 (0.707 razy wzmocnienie maksymalne).
    """
    if data.empty or "K" not in data.columns or "f" not in data.columns:
        print("Brak danych do obliczenia pasma przenoszenia")
        return 0, 0, 0

    # Konwertuj kolumny na float, aby uniknąć problemów z typami
    K_values = pd.to_numeric(data["K"], errors="coerce")
    f_values = pd.to_numeric(data["f"], errors="coerce")

    # Usuń wartości NaN
    valid_mask = ~(K_values.isna() | f_values.isna())
    K_values = K_values[valid_mask]
    f_values = f_values[valid_mask]

    if len(K_values) == 0:
        print("Brak prawidłowych danych numerycznych")
        return 0, 0, 0

    # Znajdź maksymalne wzmocnienie
    K_max = K_values.max()
    K_3dB = K_max / np.sqrt(2)  # -3dB punkt (0.707 * Kmax)

    # Utwórz DataFrame z oczyszczonymi danymi i posortuj
    clean_data = pd.DataFrame({"f": f_values, "K": K_values}).sort_values("f")

    # Znajdź indeks punktu z maksymalnym wzmocnieniem
    idx_max = clean_data["K"].idxmax()
    f_max = clean_data.loc[idx_max, "f"]

    # Dolna częstotliwość graniczna (f0) - lewa strona od maksimum
    left_data = clean_data[clean_data["f"] < f_max]
    if not left_data.empty:
        # Znajdź punkt najbliższy K_3dB z lewej strony
        left_diff = np.abs(left_data["K"] - K_3dB)
        f0_idx = left_diff.idxmin()
        f0 = left_data.loc[f0_idx, "f"]
    else:
        f0 = clean_data["f"].min()

    # Górna częstotliwość graniczna (f1) - prawa strona od maksimum
    right_data = clean_data[clean_data["f"] > f_max]
    if not right_data.empty:
        # Znajdź punkt najbliższy K_3dB z prawej strony
        right_diff = np.abs(right_data["K"] - K_3dB)
        f1_idx = right_diff.idxmin()
        f1 = right_data.loc[f1_idx, "f"]
    else:
        f1 = clean_data["f"].max()

    pasmo_szerokość = f1 - f0  # Szerokość pasma przenoszenia

    print(f"Kmax = {K_max:.3f}, K_3dB = {K_3dB:.3f}")
    print(
        f"Pasmo przenoszenia: {pasmo_szerokość:.1f} Hz (f0={f0:.1f} Hz, f1={f1:.1f} Hz)"
    )

    return pasmo_szerokość, f1, f0


def analiza_charakterystyk():
    """
    Przeprowadza szczegółową analizę charakterystyk wszystkich konfiguracji wzmacniacza.
    """
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
        print("-" * 40)  # Podstawowe statystyki - konwertuj na float dla pewności
        K_max = float(pd.to_numeric(data["K"], errors="coerce").max())
        K_min = float(pd.to_numeric(data["K"], errors="coerce").min())
        K_idx_max = pd.to_numeric(data["K"], errors="coerce").idxmax()
        f_at_max = float(pd.to_numeric(data.loc[K_idx_max, "f"], errors="coerce"))

        print(f"Maksymalne wzmocnienie: {K_max:.3f} ({20 * np.log10(K_max):.1f} dB)")
        print(f"Minimalne wzmocnienie: {K_min:.3f} ({20 * np.log10(K_min):.1f} dB)")
        print(f"Częstotliwość przy max. wzmocnieniu: {f_at_max:.1f} Hz")

        # Pasmo przenoszenia
        pasmo_szer, f1, f0 = oblicz_pasmo_przenoszenia(data)
        if pasmo_szer > 0:
            print(f"Pasmo przenoszenia (-3dB): {pasmo_szer:.1f} Hz")
            print(f"Dolna częstotliwość graniczna: {f0:.1f} Hz")
            print(f"Górna częstotliwość graniczna: {f1:.1f} Hz")


def porownanie_konfiguracji():
    """
    Porównuje różne konfiguracje wzmacniacza.
    """
    konfiguracje = {
        "bez CE bez R0": data1,
        "bez CE z R0": data2,
        "z CE z R0": data3,
        "z CE bez R0": data4,
    }

    print("\n" + "=" * 60)
    print("PORÓWNANIE KONFIGURACJI")
    print("=" * 60)  # Tworzenie tabeli porównawczej
    wyniki = []
    for nazwa, data in konfiguracje.items():
        K_max = float(pd.to_numeric(data["K"], errors="coerce").max())
        K_max_dB = 20 * np.log10(K_max)
        pasmo_szer, f1, f0 = oblicz_pasmo_przenoszenia(data)
        # Konwertuj wyniki obliczenia pasma na float dla pewności
        try:
            pasmo_szer_val = float(pasmo_szer) if pd.notna(pasmo_szer) else 0
            f0_val = float(f0) if pd.notna(f0) else 0
            f1_val = float(f1) if pd.notna(f1) else 0
        except (ValueError, TypeError):
            pasmo_szer_val = f0_val = f1_val = 0

        wyniki.append(
            {
                "Konfiguracja": nazwa,
                "Max K": f"{K_max:.3f}",
                "Max K [dB]": f"{K_max_dB:.1f}",
                "Pasmo [Hz]": f"{pasmo_szer_val:.1f}" if pasmo_szer_val > 0 else "N/A",
                "f0 [Hz]": f"{f0_val:.1f}" if f0_val > 0 else "N/A",
                "f1 [Hz]": f"{f1_val:.1f}" if f1_val > 0 else "N/A",
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


def plot_all_gains_vs_frequency():
    """
    Tworzy wykres charakterystyki częstotliwościowej wzmacniacza dla wszystkich konfiguracji.
    """
    plt.figure(figsize=(16, 10))

    # Kolory dla różnych konfiguracji
    colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]  # Wyraźniejsze kolory

    # Plot all 4 datasets on the same chart
    datasets = [
        (data1, "bez CE bez R0", "o"),
        (data2, "bez CE z R0", "s"),
        (data3, "z CE z R0", "^"),
        (data4, "z CE bez R0", "d"),
    ]

    # Najpierw narysuj wszystkie krzywe
    for i, (data, label, marker) in enumerate(datasets):
        plt.semilogx(
            data["f"],
            20 * np.log10(data["K"]),
            marker=marker,
            linestyle="-",
            label=label,
            linewidth=2.5,
            color=colors[i],
            markersize=7,
            markerfacecolor=colors[i],
            markeredgecolor="white",
            markeredgewidth=0.5,
        )  # Następnie dodaj oznaczenia pasma przenoszenia - tylko dla wyraźności
    for i, (data, label, _) in enumerate(datasets):
        pasmo_szerokość, f1, f0 = oblicz_pasmo_przenoszenia(data)
        if f0 > 0 and f1 > 0:
            # Dodaj cienkie pionowe linie dla granic pasma tylko na dole wykresu
            y_min = plt.ylim()[0]
            y_max = 20 * np.log10(data["K"].max())

            # Pionowe linie granic pasma
            plt.vlines(
                f0,
                y_min,
                y_max,
                colors=colors[i],
                linestyles="--",
                linewidth=1.5,
                alpha=0.7,
            )
            plt.vlines(
                f1,
                y_min,
                y_max,
                colors=colors[i],
                linestyles="--",
                linewidth=1.5,
                alpha=0.7,
            )

            # Pozioma linia -3dB tylko w zakresie pasma
            y_3dB = 20 * np.log10(data["K"].max() / np.sqrt(2))
            plt.hlines(
                y_3dB, f0, f1, colors=colors[i], linestyles=":", linewidth=2, alpha=0.8
            )

            # Dodaj etykiety pasma w czytelnych miejscach
            mid_f = np.sqrt(f0 * f1)  # Środek logarytmiczny
            plt.annotate(
                f"BW: {pasmo_szerokość:.0f}Hz",
                xy=(mid_f, y_3dB),
                xytext=(10, 10),
                textcoords="offset points",
                bbox=dict(boxstyle="round,pad=0.3", facecolor=colors[i], alpha=0.7),
                fontsize=9,
                color="white",
                weight="bold",
            )

            # Dodaj etykiety f0 i f1 na osi X
            plt.annotate(
                f"f0={f0:.0f}",
                xy=(f0, y_min + 2),
                ha="center",
                color=colors[i],
                fontsize=8,
                weight="bold",
            )
            plt.annotate(
                f"f1={f1:.0f}",
                xy=(f1, y_min + 2),
                ha="center",
                color=colors[i],
                fontsize=8,
                weight="bold",
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

    # Lepsza legenda
    legend1 = plt.legend(
        loc="upper right", fontsize=11, frameon=True, fancybox=True, shadow=True
    )

    # Dodaj drugą legendę dla oznaczen pasma
    from matplotlib.lines import Line2D

    legend_elements = [
        Line2D(
            [0],
            [0],
            color="gray",
            linestyle="--",
            linewidth=1.5,
            label="Granice pasma (f0, f1)",
        ),
        Line2D([0], [0], color="gray", linestyle=":", linewidth=2, label="Poziom -3dB"),
    ]
    legend2 = plt.legend(
        handles=legend_elements,
        loc="lower left",
        fontsize=10,
        frameon=True,
        fancybox=True,
        shadow=True,
    )

    # Dodaj pierwszą legendę z powrotem
    plt.gca().add_artist(legend1)

    plt.tight_layout()
    plt.show()


def plot_individual_configs():
    """
    Tworzy osobne wykresy dla każdej konfiguracji wzmacniacza.
    """
    datasets = [
        (data1, "bez CE bez R0", "o", "#1f77b4"),
        (data2, "bez CE z R0", "s", "#ff7f0e"),
        (data3, "z CE z R0", "^", "#2ca02c"),
        (data4, "z CE bez R0", "d", "#d62728"),
    ]

    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle(
        "Charakterystyki częstotliwościowe wzmacniacza - porównanie konfiguracji",
        fontsize=16,
        fontweight="bold",
    )

    axes = axes.flatten()

    for idx, (data, label, marker, color) in enumerate(datasets):
        ax = axes[idx]

        # Wykres główny
        ax.semilogx(
            data["f"],
            20 * np.log10(data["K"]),
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

        # Pasmo przenoszenia
        pasmo_szerokość, f1, f0 = oblicz_pasmo_przenoszenia(data)
        if f0 > 0 and f1 > 0:
            y_min, y_max = ax.get_ylim()
            y_3dB = 20 * np.log10(data["K"].max() / np.sqrt(2))

            # Oznaczenia pasma
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

            # Zaznacz obszar pasma
            ax.axvspan(
                f0, f1, alpha=0.2, color=color, label=f"BW = {pasmo_szerokość:.0f} Hz"
            )

        ax.set_xlabel("Częstotliwość [Hz]", fontsize=12)
        ax.set_ylabel("Wzmocnienie K [dB]", fontsize=12)
        ax.set_title(label, fontsize=14, fontweight="bold")
        ax.grid(True, alpha=0.3, which="both")
        ax.legend(fontsize=9, loc="best")

    plt.tight_layout()
    plt.show()


def zapisz_wyniki_do_pliku():
    """
    Zapisuje wyniki analizy do pliku tekstowego.
    """
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

            K_max = data["K"].max()
            K_min = data["K"].min()
            f_at_max = data.loc[data["K"].idxmax(), "f"]

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
    # Przeprowadź analizę charakterystyk
    analiza_charakterystyk()
    porownanie_konfiguracji()

    # Zapisz wyniki do pliku
    try:
        zapisz_wyniki_do_pliku()
    except Exception as e:
        print(f"Nie udało się zapisać wyników do pliku: {e}")

    # Wyświetl wykresy
    print("\nWyświetlanie zbiorczego wykresu wszystkich konfiguracji...")
    plot_all_gains_vs_frequency()

    print("\nWyświetlanie osobnych wykresów dla każdej konfiguracji...")
    plot_individual_configs()
    plot_individual_configs()
