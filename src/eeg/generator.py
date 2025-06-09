import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Wczytaj dane z Excela
data = pd.read_excel("data/Generator.xlsx")

# Dane z pliku
f = np.array(data["f"].values)  # Częstotliwość (Hz)
U1 = np.array(data["U1"].values)  # Napięcie wejściowe (V)
U2 = np.array(data["U2"].values)  # Napięcie wyjściowe (V)
Bu = np.array(data["Bu"].values)  # Wzmocnienie przesuwnika: Bu = U2 / U1
FiB = np.array(data["FiB"].values)  # Przesunięcie fazowe przesuwnika (stopnie)

# Parametry wzmacniacza
U1_w = 1  # [V]
U2_w = 3  # [V]
K = U2_w / U1_w  # Wzmocnienie wzmacniacza (Ku)
Fi_u = 0  # Przesunięcie fazowe wzmacniacza (ψu), idealnie 0

# Stałe przebiegi Ku i ψu
Ku = np.full_like(f, K)
psi_u = np.full_like(f, Fi_u)

# Całkowite wzmocnienie i przesunięcie fazowe
Ku_total = Ku * Bu
phi_total = psi_u + FiB

# Znajdź punkt, gdzie Ku * Bu ≈ 1.1
target_gain = 1.1
idx = np.argmin(np.abs(Ku_total - target_gain))
target_f = f[idx]
target_phi = phi_total[idx]

# Rysowanie wykresów
plt.figure(figsize=(14, 12))

# 1. Ku (wzmacniacz)
plt.subplot(3, 2, 1)
plt.plot(f, Ku, "--", label="Ku = 3", color="blue")
plt.title("Stałe wzmocnienie Ku (wzmacniacz)")
plt.xlabel("Częstotliwość [Hz]")
plt.ylabel("Ku")
plt.grid()
plt.legend()

# 2. ψu (wzmacniacz)
plt.subplot(3, 2, 2)
plt.plot(f, psi_u, "--", label="ψu = 0°", color="green")
plt.title("Stałe przesunięcie fazowe ψu (wzmacniacz)")
plt.xlabel("Częstotliwość [Hz]")
plt.ylabel("ψu [°]")
plt.grid()
plt.legend()

# 3. βu (przesuwnik)
plt.subplot(3, 2, 3)
plt.plot(f, Bu, "o-", label="βu(f)", color="purple")
plt.title("Wzmocnienie βu (przesuwnik)")
plt.xlabel("Częstotliwość [Hz]")
plt.ylabel("βu")
plt.grid()
plt.legend()

# 4. φp (przesuwnik)
plt.subplot(3, 2, 4)
plt.plot(f, FiB, "o-", label="φp(f)", color="orange")
plt.title("Przesunięcie fazowe φp (przesuwnik)")
plt.xlabel("Częstotliwość [Hz]")
plt.ylabel("φp [°]")
plt.grid()
plt.legend()

# 5. Ku · βu
plt.subplot(3, 2, 5)
plt.plot(f, Ku_total, "o-", label="Ku · βu", color="red")
plt.axhline(y=target_gain, color="gray", linestyle="--", label=f"Ku·βu = {target_gain}")
plt.axvline(x=target_f, color="gray", linestyle=":")
plt.scatter(target_f, Ku_total[idx], color="black", zorder=5)
plt.title("Całkowite wzmocnienie Ku·βu")
plt.xlabel("Częstotliwość [Hz]")
plt.ylabel("Wzmocnienie")
plt.grid()
plt.legend()

# 6. φ = φp + ψu
plt.subplot(3, 2, 6)
plt.plot(f, phi_total, "o-", label="φ = φp + ψu", color="darkblue")
plt.axvline(x=target_f, color="gray", linestyle=":")
plt.scatter(
    target_f, target_phi, color="black", zorder=5, label=f"φ ≈ {target_phi:.2f}°"
)
plt.title("Całkowite przesunięcie fazowe φ")
plt.xlabel("Częstotliwość [Hz]")
plt.ylabel("φ [°]")
plt.grid()
plt.legend()

plt.tight_layout()
plt.show()
