# Graph Plotter for Physics Exercises

A simple tool to analyze and graph data from physics experiments using `matplotlib`, `numpy`, and `pandas`.

## Features

This repository includes tools for:

1. **Pendulum Experiments**:
   - Analyze pendulum data to calculate the slope (\( A \)), intercept (\( B \)), gravity (\( g \)), and moment of inertia.
   - Generate graphs with regression lines and results.
2. **Focal Length Calculation**:
   - Calculate the focal length of lenses using data from physics experiments.
   - Perform graphical analysis to determine the focal length.
   - Includes additional comment print statements to display intermediate calculations for better understanding of the exercise.

---

## How to Use the Tools

### 1. Prepare Your Data

- For **Pendulum Experiments**:
  - Ensure your data is stored in an Excel file (e.g., `Pendulum.xlsx`) with the following columns:
    - `D`: Distance from the center of weight (in meters).
    - `t1`: Start time for 40 oscillations (in seconds).
    - `t2`: End time for 40 oscillations (in seconds).
  - Place the Excel file in the appropriate directory where the script can access it.

- For **Focal Length Calculation**:
  - Ensure your data is stored in an Excel file (e.g., `focal-length.xlsx`) with two sheets:
    - **Sheet 1 (`pomn`)**: Data for the reduced image.
      - Columns: `x1`, `x2`, `x3`, `x4`, `x5` (object distances), and `y` (image distances).
    - **Sheet 2 (`pow`)**: Data for the magnified image.
      - Columns: `x1`, `x2`, `x3`, `x4`, `x5` (object distances), and `y` (image distances).

### 2. Install Dependencies

The project requires the following Python libraries:

- `pyxdf`
- `matplotlib`
- `pyqt6`
- `numpy`
- `scipy`
- `pandas`
- `scikit-learn`
- `openpyxl`
- `pyedflib`

#### Using `rye` (Recommended)

Install dependencies with [rye](https://rye.astral.sh/):

```bash
rye sync
```

#### Using `pip`

Alternatively, install dependencies manually:

```bash
pip install pyxdf matplotlib pyqt6 numpy scipy pandas scikit-learn openpyxl pyedflib
```

### 3. Activate the Virtual Environment

- If you are using `rye`, the virtual environment is automatically managed.
- Otherwise, activate the virtual environment manually:
  - **Linux/macOS**:

    ```bash
    source ./.venv/bin/activate
    ```

  - **Windows**:

    ```bash
    .\.venv\Scripts\activate
    ```

### 4. Run the Scripts

- For **Pendulum Experiments**:

  ```bash
  python src/eeg/Pendulum.py
  ```

- For **Focal Length Calculation**:

  ```bash
  python src/eeg/focal_len.py
  ```

### 5. View the Results

- **Pendulum Experiments**:
  - The script will calculate the slope (\( A \)), intercept (\( B \)), gravity (\( g \)), and moment of inertia with uncertainties.
  - It will display the results in the terminal and on a graph.
- **Focal Length Calculation**:
  - The script will calculate the focal length for both reduced and magnified images.
  - It will also perform graphical analysis to determine the focal length and display the results on a graph.
  - Additional print statements will show intermediate calculations, such as:
    - Average focal lengths for reduced and magnified images.
    - Graphically determined focal length and its uncertainty.

---

## Example Outputs

### Pendulum Experiments

#### Command Line

```sh
Slope (A): 3.1046 ± 0.1059 s²/m 
Intercept (B): 0.3433 ± 0.0073 m·s² 
Gravity (g): 12.7161 ± 1.3466 m/s² 
Moment of Inertia: 0.0866 ± 0.0035 kg·m²
```

#### Graph

- The graph will display the data points, regression line, and the results in a text box.

### Focal Length Calculation

#### Command Line

```sh
Średnia ogniskowa (obraz pomniejszony): 15.23 cm ± 0.12 cm
Średnia ogniskowa (obraz powiększony): 15.18 cm ± 0.10 cm
Graficznie wyznaczona ogniskowa: 15.20 cm ± 0.11 cm
```

#### Graph

- The graph will display:
  - Data points for reduced and magnified images.
  - Fitted regression lines for both datasets.
  - The intersection point representing the focal length.

---

## Troubleshooting

- **Excel File Issues**:
  - Ensure your Excel file is formatted correctly and contains valid data.
  - Verify that the sheet names and column names match the expected format.
- **Dependency Issues**:
  - Verify that your Python environment is properly set up and all required libraries are installed.
- **Virtual Environment**:
  - Ensure the virtual environment is activated before running the scripts.

---

## Additional Notes

- This tool is designed for educational purposes and assumes the input data follows the expected format.
- Contributions and suggestions for improvement are welcome!