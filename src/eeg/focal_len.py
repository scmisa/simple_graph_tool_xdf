import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Wczytaj dane
data_pomn = pd.read_excel("data/focal-length.xlsx", sheet_name="pomn")  # obraz pomniejszony
data_pow = pd.read_excel("data/focal-length.xlsx", sheet_name="pow")   # obraz powiększony

def przygotuj_dane(data):
    if '~x' not in data.columns:
        data['~x'] = data[['x1', 'x2', 'x3', 'x4', 'x5']].mean(axis=1)
    return data

def rysuj_wykres(data, tytul, kolor_punktu, kolor_promieni):
    data = przygotuj_dane(data)

    fig, ax = plt.subplots(figsize=(10, 6))

    # Store all points to find intersections between actual light rays
    wszystkie_promienie = []

    for i, row in data.iterrows():
        x = row['~x']
        y = row['y']

        # Przedmiot (x, 0), obraz (0, y) - główny promień
        ax.plot([x, 0], [0, y], linestyle='-', color=kolor_promieni, alpha=0.6)
        wszystkie_promienie.append(((x, 0), (0, y)))

        # Punkty
        ax.errorbar(x, 0, xerr=0.2, fmt='o', color=kolor_punktu, label='Przedmiot' if i == 0 else "")
        ax.errorbar(0, y, yerr=0.2, fmt='o', color='black', label='Obraz' if i == 0 else "")

    # Znajdź przecięcia między wszystkimi parami promieni
    punkty_przeciecia = []
    for i in range(len(wszystkie_promienie)):
        for j in range(i + 1, len(wszystkie_promienie)):
            # Weź dwa różne promienie
            (x1, y1), (x2, y2) = wszystkie_promienie[i]
            (x3, y3), (x4, y4) = wszystkie_promienie[j]
            
            try:
                a1 = (y2 - y1) / (x2 - x1)
                b1 = y1 - a1 * x1
                
                a2 = (y4 - y3) / (x4 - x3)
                b2 = y3 - a2 * x3
                
                # Oblicz punkt przecięcia
                if abs(a1 - a2) > 1e-10:  # Jeśli linie nie są równoległe
                    x_przec = (b2 - b1) / (a1 - a2)
                    y_przec = a1 * x_przec + b1
                    
                    # Sprawdź czy punkt przecięcia leży na obu odcinkach
                    if (min(x1, x2) <= x_przec <= max(x1, x2) and
                        min(x3, x4) <= x_przec <= max(x3, x4)):
                        punkty_przeciecia.append((x_przec, y_przec))
            except:
                continue

    if punkty_przeciecia:
        # Wybierz pierwszy punkt przecięcia
        x_przec, y_przec = punkty_przeciecia[2]
        
        # Narysuj punkt przecięcia
        ax.plot(x_przec, y_przec, 'r.', markersize=10)
        
        # Narysuj linię referencyjną do osi x
        ax.plot([x_przec, x_przec], [y_przec, 0], '--', color='gray', alpha=0.8)
        
        # Zaznacz ogniskową
        f_zmierzona = abs(x_przec)
        ax.axvline(x=f_zmierzona, linestyle='--', color='red', alpha=0.7, 
                  label=f'Ogniskowa f = {f_zmierzona:.1f} cm')
        ax.axvline(x=-f_zmierzona, linestyle='--', color='red', alpha=0.7)

    ax.axvline(x=0, color='blue', linewidth=2, label='Soczewka')
    ax.axhline(y=0, color='black', linewidth=1)

    ax.set_title(tytul)
    ax.set_xlabel("Położenie (x) [cm]")
    ax.set_ylabel("Wysokość (y) [cm]")
    ax.legend()
    ax.grid(True)
    plt.tight_layout()
    plt.show()

# Wykresy
rysuj_wykres(data_pow, "Obraz powiększony – skupianie promieni z błędem", "red", "orange")
rysuj_wykres(data_pomn, "Obraz pomniejszony – skupianie promieni z błędem", "blue", "green")