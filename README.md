# Graph Plotter for Physics Pendulum Exercises

A simple tool to analyze and graph data from pendulum experiments using `matplotlib` and `numpy`.

## How to Use the Tool

1. **Prepare Your Data**:
   - Ensure your pendulum experiment data is stored in an Excel file (e.g., `Pendulum.xlsx`) with the following columns:
     - `D`: Distance from the center of weight (in meters).
     - `t1`: Start time for 40 oscillations (in seconds).
     - `t2`: End time for 40 oscillations (in seconds).
   - Place the Excel file in the appropriate directory where the script can access it.

2. **Install Dependencies**:
   - The project requires the following Python libraries:
     - `pyxdf`
     - `matplotlib`
     - `pyqt6`
     - `numpy`
     - `scipy`
     - `pandas`
     - `scikit-learn`
     - `openpyxl`
     - `pyedflib`
   - Use [rye](https://rye.astral.sh/) to install dependencies:

     ```bash
     rye sync
     ```

   - Alternatively, install dependencies manually with `pip`:

     ```bash
     pip install pyxdf matplotlib pyqt6 numpy scipy pandas scikit-learn openpyxl pyedflib
     ```

3. **Activate the  EnvironmentVirtual**:
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

4. **Run the Script**:
   - Execute the main script to analyze the data and generate the graph:

     ```bash
     python src/eeg/Pendulum.py
     ```

5. **View the Results**:
   - The script will:
     - Calculate the slope (\( A \)) and intercept (\( B \)) of the linear regression.
     - Compute the gravity (\( g \)) and moment of inertia with uncertainties.
     - Display the results in the terminal and on the graph.
   - The graph will include:
     - A scatter plot of the data points.
     - A fitted regression line.
     - A text box showing the calculated results (slope, intercept, gravity, and moment of inertia).

## Example Output

### Command Line

```sh
Slope (A): 3.1046 ± 0.1059 s²/m Intercept (B): 0.3433 ± 0.0073 m·s² Gravity (g): 12.7161 ± 1.3466 m/s² Moment of Inertia: 0.0866 ± 0.0035 kg·m²
```

### Graph

- The graph will display the data points, regression line, and the results in a text box.

## Troubleshooting

- Ensure your Excel file is formatted correctly and contains valid data.
- If you encounter issues with dependencies, verify that your Python environment is properly set up.
