import pyxdf
import matplotlib.pyplot as plt
import numpy as np  # noqa: F401

data, header = pyxdf.load_xdf("data/1min_3polar.xdf")

print(data)
# Print the header
plot_data = data[0]
plot_data1 = data[1]
plot_data2 = data[2]

fig, ax = plt.subplots()
ax.plot(plot_data["time_stamps"], plot_data["time_series"])
ax.plot(plot_data1["time_stamps"], plot_data1["time_series"])
ax.plot(plot_data2["time_stamps"], plot_data2["time_series"])

ax.set_xlabel("Time (s)")
ax.set_ylabel("Voltage (uV)")
ax.set_title("ECG Data")
ax.legend(["ECG1", "ECG2", "ECG3"])
ax.grid(True)

plt.show()
