import numpy as np
import matplotlib.pyplot as plt

# !DANE Z DIOD
# ?Dioda Germanowa w kierunku przewodzenia
GP_I = np.array([10, 20, 50, 100, 200, 500, 1000, 5000])  # microampery
GP_I = GP_I * 1e-6  # Convert to amperes
GP_U = np.array([0.009, 0.016, 0.034, 0.052, 0.075, 0.113, 0.147, 0.238])  # Volts

# ?Dioda Germanowa w kierunku zaporowym
GZ_U = np.array([5, 10, 15, 20, 30])  # Volts
GZ_I = np.array([93.2, 213.1, 364, 519.7, 807])  # microampery
GZ_I = GZ_I * 1e-6  # Convert to amperes

# ?Dioda Krzemowa w kierunku przewodzenia
KP_I = np.array([10, 20, 50, 100, 200, 500, 1000, 5000])  # microampery
KP_I = KP_I * 1e-6  # Convert to amperes
KP_U = np.array([0.393, 0.416, 0.449, 0.478, 0.503, 0.546, 0.578, 0.653])  # Volts

# ?Dioda Led w kierunku przewodzenia
LED_I = np.array([10, 20, 50, 100, 200, 500, 1000, 5000])  # microampery
LED_I = LED_I * 1e-6  # Convert to amperes
LED_U = np.array([1.41, 1.447, 1.435, 1.581, 1.557, 1.608, 1.642, 1.793])  # Volts

# ?Dioda Zenera w kierunku przewodzenia
ZZ_U = np.array([5.168, 5.535, 5.95, 6.21, 6.445, 6.61, 6.65, 6.68])  # Volts
ZZ_I = np.array([10, 20, 50, 100, 200, 500, 1000, 5000])  # microampery
ZZ_I = ZZ_I * 1e-6  # Convert to amperes

# ?Dioda Zenera w kierunku zaporowym
ZK_U = np.array([0.433, 0.479, 0.518, 0.543, 0.57, 0.609, 0.632, 0.684])  # Volts
ZK_I = np.array([10, 20, 50, 100, 200, 500, 1000, 5000])  # microampery
ZK_I = ZK_I * 1e-6  # Convert to amperes


# !WIZUALIZACJA DANYCH
def plot_diode_characteristics():
    plt.figure(figsize=(12, 8))

    # Dioda Germanowa w kierunku przewodzenia
    plt.subplot(2, 2, 1)
    plt.plot(GP_I, GP_U, "o-", label="Dioda Germanowa (przewodzenie)")
    plt.title("Dioda Germanowa - Kierunek Przewodzenia")
    plt.xlabel("Prąd (A)")
    plt.ylabel("Napięcie (V)")
    plt.grid()
    plt.legend()

    # Dioda Germanowa w kierunku zaporowym
    plt.subplot(2, 2, 2)
    plt.plot(GZ_U, GZ_I, "o-", label="Dioda Germanowa (zaporowy)", color="orange")
    plt.title("Dioda Germanowa - Kierunek Zaporowy")
    plt.xlabel("Napięcie (V)")
    plt.ylabel("Prąd (A)")
    plt.grid()
    plt.legend()

    # Dioda Krzemowa w kierunku przewodzenia
    plt.subplot(2, 2, 3)
    plt.plot(KP_I, KP_U, "o-", label="Dioda Krzemowa (przewodzenie)", color="green")
    plt.title("Dioda Krzemowa - Kierunek Przewodzenia")
    plt.xlabel("Prąd (A)")
    plt.ylabel("Napięcie (V)")
    plt.grid()
    plt.legend()

    # Dioda Led w kierunku przewodzenia
    plt.subplot(2, 2, 4)
    plt.plot(LED_I, LED_U, "o-", label="Dioda LED (przewodzenie)", color="red")
    plt.title("Dioda LED - Kierunek Przewodzenia")
    plt.xlabel("Prąd (A)")
    plt.ylabel("Napięcie (V)")
    plt.grid()
    plt.legend()

    # Dioda Zenera w kierunku przewodzenia
    plt.figure(figsize=(12, 8))
    plt.subplot(2, 2, 1)
    plt.plot(ZZ_I, ZZ_U, "o-", label="Dioda Zenera (przewodzenie)", color="purple")
    plt.title("Dioda Zenera - Kierunek Przewodzenia")
    plt.xlabel("Prąd (A)")
    plt.ylabel("Napięcie (V)")
    plt.grid()
    plt.legend()

    # Dioda Zenera w kierunku zaporowym
    plt.subplot(2, 2, 2)
    plt.plot(ZK_U, ZK_I, "o-", label="Dioda Zenera (zaporowy)", color="brown")
    plt.title("Dioda Zenera - Kierunek Zaporowy")
    plt.xlabel("Napięcie (V)")
    plt.ylabel("Prąd (A)")
    plt.grid()
    plt.legend()

    plt.tight_layout()
    plt.show()


plot_diode_characteristics()
