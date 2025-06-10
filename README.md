# Graph Plotter for Physics Exercises

A comprehensive tool to analyze and graph data from physics experiments using `matplotlib`, `numpy`, and `pandas`.

## Features

This repository includes tools for:

1. **Pendulum Experiments**:
   - Analyze pendulum data to calculate the slope (\( A \)), intercept (\( B \)), gravity (\( g \)), and moment of inertia.
   - Generate graphs with regression lines and results.

2. **Focal Length Calculation**:
   - Calculate the focal length of lenses using data from physics experiments.
   - Perform graphical analysis to determine the focal length.
   - Includes additional comment print statements to display intermediate calculations for better understanding of the exercise.

3. **Spring Force Analysis (Siły Sprężyste)**:
   - Method A: Analyze spring length vs. applied mass to determine spring constant using Hooke's law.
   - Method B: Study oscillation period vs. suspended mass to calculate spring constant.
   - Perform linear regression analysis and calculate uncertainties.
   - Generate comparative plots for both methods.

4. **Thermocouple Analysis (Termopara)**:
   - Analyze thermocouple temperature measurements for different materials.
   - Study cooling curves and temperature dependencies.
   - Process data for water and Wood's alloy temperature measurements.
   - Generate temperature vs. time plots with analysis.

5. **Diode Analysis (Diody)**:
   - Analyze diode characteristics and I-V curves.
   - Calculate diode parameters and perform regression analysis.
   - Generate characteristic plots for diode behavior analysis.

6. **Signal Generator Analysis**:
   - Analyze signal generator output characteristics.
   - Process frequency response and amplitude measurements.
   - Generate plots for signal analysis and characterization.

7. **Amplifier Analysis (Wzmacniacz)**:
   - Analyze amplifier gain and frequency response.
   - Calculate amplification factors and bandwidth characteristics.
   - Multiple analysis versions available (standard, clean, improved).
   - Generate Bode plots and frequency response curves.

8. **Thermal Resistance Analysis (TermOpor)**:
   - Analyze thermal resistance and temperature coefficient measurements.
   - Study temperature-dependent resistance characteristics.
   - Process thermal response data and generate analysis plots.

---

## How to Use the Tools

### 1. Prepare Your Data

- For **Pendulum Experiments**:
  - Ensure your data is stored in an Excel file (`Pendulum.xlsx`) with the following columns:
    - `D`: Distance from the center of weight (in meters).
    - `t1`: Start time for 40 oscillations (in seconds).
    - `t2`: End time for 40 oscillations (in seconds).

- For **Focal Length Calculation**:
  - Ensure your data is stored in an Excel file (`focal-length.xlsx`) with two sheets:
    - **Sheet 1 (`pomn`)**: Data for the reduced image.
      - Columns: `x1`, `x2`, `x3`, `x4`, `x5` (object distances), and `y` (image distances).
    - **Sheet 2 (`pow`)**: Data for the magnified image.
      - Columns: `x1`, `x2`, `x3`, `x4`, `x5` (object distances), and `y` (image distances).

- For **Spring Force Analysis**:
  - Ensure your data is stored in an Excel file (`sily_sprezyste.xlsx`) with two sheets:
    - **Sheet 1 (`MetodaA`)**: Spring length vs. mass data.
      - Columns: `L_0` (initial length in mm), `M` (mass in g), `L` (spring length in m).
    - **Sheet 2 (`MetodaB`)**: Oscillation period vs. mass data.
      - Columns: `M` (mass in g), `t1`, `t2` (time measurements in s), `T` (period in s).

- For **Thermocouple Analysis**:
  - Ensure your data is stored in an Excel file (`Termopara.xlsx`) with sheets for different materials:
    - Temperature measurements over time for various substances.
    - Data should include time and temperature columns for analysis.

- For **Diode Analysis**:
  - Ensure your data is stored in an Excel file with voltage and current measurements.
  - Data should include columns for applied voltage and measured current for I-V characteristic analysis.

- For **Signal Generator Analysis**:
  - Ensure your data is stored in an Excel file (`Generator.xlsx`) with frequency and amplitude measurements.
  - Data should include frequency response and signal characteristics for analysis.

- For **Amplifier Analysis**:
  - Ensure your data is stored in an Excel file (`Wzmacniacz.xlsx`) with gain and frequency measurements.
  - Data should include input/output voltage measurements and frequency response data.

- For **Thermal Resistance Analysis**:
  - Ensure your data is stored in an Excel file (`TermOpor.xlsx`) with temperature and resistance measurements.
  - Data should include temperature values and corresponding resistance measurements for analysis.

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

#### Using `uv` (Recommended)

Install dependencies with [uv](https://docs.astral.sh/uv/):

```bash
uv sync
```

#### Using `pip`

Alternatively, install dependencies manually:

```bash
pip install pyxdf matplotlib pyqt6 numpy scipy pandas scikit-learn openpyxl pyedflib
```

### 3. Activate the Virtual Environment

- If you are using `uv`, the virtual environment is automatically managed.
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

- For **Spring Force Analysis**:

  ```bash
  python src/eeg/sily_sprezyste.py
  ```

- For **Thermocouple Analysis**:

  ```bash
  python src/eeg/termopara.py
  ```

- For **Diode Analysis**:

  ```bash
  python src/eeg/diody.py
  ```

- For **Signal Generator Analysis**:

  ```bash
  python src/eeg/generator.py
  ```

- For **Amplifier Analysis**:

  ```bash
  python src/eeg/wzmacniacz.py
  ```

  Alternative versions:
  ```bash
  python src/eeg/wzmacniacz_clean.py
  python src/eeg/wzmacniacz_improved.py
  ```

- For **Thermal Resistance Analysis**:

  ```bash
  python src/eeg/termopor.py
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

- **Spring Force Analysis**:
  - Method A: Calculates spring constant from spring length vs. mass relationship.
  - Method B: Calculates spring constant from oscillation period vs. mass relationship.
  - Displays regression statistics, spring constants, and uncertainties.
  - Generates plots showing data points, regression lines, and calculated results.

- **Thermocouple Analysis**:
  - Processes temperature vs. time data for different materials.
  - Calculates cooling rates and temperature dependencies.
  - Generates temperature curves and analysis plots.

- **Diode Analysis**:
  - Analyzes I-V characteristics of diodes.
  - Calculates diode parameters such as forward voltage and reverse saturation current.
  - Generates characteristic curves and regression analysis plots.

- **Signal Generator Analysis**:
  - Processes frequency response and amplitude characteristics.
  - Analyzes signal quality and distortion parameters.
  - Generates frequency response plots and signal analysis graphs.

- **Amplifier Analysis**:
  - Calculates amplification gain and frequency response.
  - Analyzes bandwidth and phase characteristics.
  - Generates Bode plots and frequency response curves.
  - Multiple analysis approaches available for different aspects of amplifier behavior.

- **Thermal Resistance Analysis**:
  - Analyzes temperature coefficient of resistance.
  - Calculates thermal response characteristics.
  - Generates temperature vs. resistance plots with regression analysis.

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

### Spring Force Analysis

#### Command Line

```sh
Statystyki regresji:
Nachylenie (a): 0.0098
Przecięcie (b): 0.1420
Niepewność standardowa u(a): 0.0012
Niepewność standardowa u(b): 0.0012

Nachylenie a (m/kg): 0.0098
Stała sprężyny k: 100.15 N/m
Niepewność stałej sprężyny u(k): 12.34 N/m
L_0 = 0.1400 m odpowiada przecięciu y b = 0.1420 ± 0.0036 m

Nachylenie a (s/kg): 0.6234
Średnia arytmetyczna stałej sprężyny k: 98.76 N/kg
Odchylenie standardowe stałej sprężyny: 3.45 N/kg
Niepewność okresu delta_T: 0.0200 s
```

#### Graphs

- **Method A**: Spring length vs. mass with regression line and spring constant calculation.
- **Method B**: Oscillation period vs. mass with regression analysis and spring constant determination.

### Thermocouple Analysis

#### Command Line

```sh
Analiza danych termopary:
Temperatura początkowa wody: 85.2°C
Temperatura końcowa wody: 23.1°C
Szybkość chłodzenia: -0.52°C/min

Temperatura topienia stopu Wooda: 70.5°C ± 1.2°C
Czas stabilizacji temperatury: 15.3 min
```

#### Graphs

- Temperature vs. time curves for water cooling.
- Wood's alloy melting point analysis with plateau identification.

---

## Troubleshooting

- **Excel File Issues**:
  - Ensure your Excel file is formatted correctly and contains valid data.
  - Verify that the sheet names and column names match the expected format.
  - For spring force analysis, ensure `MetodaA` and `MetodaB` sheets exist with correct column names.
  - For thermocouple analysis, verify temperature and time data columns are properly formatted.

- **Unit Conversion Issues**:
  - Spring force analysis expects specific units: mass in grams, length in meters/millimeters as specified.
  - Thermocouple data should have temperature in Celsius and time in appropriate units.

- **Data Format Issues**:
  - Ensure numerical data doesn't contain text or missing values.
  - Check for consistent decimal separators (dots vs. commas) based on your system locale.

- **Dependency Issues**:
  - Verify that your Python environment is properly set up and all required libraries are installed.

- **Virtual Environment**:
  - Ensure the virtual environment is activated before running the scripts.

- **Plot Display Issues**:
  - If plots don't display, ensure you have a GUI backend for matplotlib installed.
  - On some systems, you may need to install additional packages for plot display.

---

## Generated Reports and Files

The project automatically generates LaTeX reports and plots for each experiment:

### Reports Directory Structure

```text
Reports/
├── Dioda/              # Diode analysis
│   ├── dioda.pdf       # Compiled LaTeX report
│   ├── dioda.tex       # LaTeX source
│   ├── Figure_1.png    # I-V characteristic plot
│   └── Figure_2.png    # Additional analysis plot
├── Generator/          # Signal generator analysis
│   ├── generator.pdf   # Compiled LaTeX report
│   ├── generator.tex   # LaTeX source
│   └── Generator.png   # Generator analysis plot
├── Ogniskowa/          # Focal length analysis
│   ├── ogniskowa.pdf   # Compiled LaTeX report
│   ├── ogniskowa.tex   # LaTeX source
│   ├── obraz_pom.png   # Reduced image plot
│   └── obraz_pow.png   # Magnified image plot
├── Pendulum/           # Pendulum experiments
│   ├── reportPendulum.pdf  # Compiled report
│   ├── reportPendulum.tex  # LaTeX source
│   └── pendulum.png        # Pendulum analysis plot
├── sily_sprezyste/     # Spring force analysis
│   ├── sily_sprezyste.pdf  # Compiled report
│   ├── sily_sprezyste.tex  # LaTeX source
│   ├── MetodaA.png         # Method A plot
│   └── MetodaB.png         # Method B plot
├── Template/           # LaTeX template files
│   ├── template.pdf    # Template document
│   ├── template.tex    # LaTeX template source
│   └── logaUR.pdf      # University logo
├── Termopara/          # Thermocouple analysis
│   ├── reportTermopara.pdf # Compiled report
│   ├── reportTermopara.tex # LaTeX source
│   ├── woda.png           # Water cooling plot
│   └── stopWooda.png      # Wood's alloy analysis plot
├── TermOpor/           # Thermal resistance analysis
│   ├── termopor.pdf    # Compiled LaTeX report
│   ├── termopor.tex    # LaTeX source
│   └── termOpor.png    # Thermal resistance plot
└── Wzmacniacz/         # Amplifier analysis
    ├── wzmacniacz.pdf  # Compiled LaTeX report
    ├── wzmacniacz.tex  # LaTeX source
    ├── wzmacniacz.png  # Standard amplifier plot
    ├── wzmacniaczImpr.png # Improved analysis plot
    ├── wykresy osobno.png # Separate plots
    └── analiza_wyniki.txt # Analysis results text file
```

### Data Files

All experimental data is stored in the `data/` directory:
- `Pendulum.xlsx` - Pendulum experiment data
- `focal-length.xlsx` - Lens focal length measurements
- `sily_sprezyste.xlsx` - Spring force analysis data (Methods A & B)
- `Termopara.xlsx` - Thermocouple temperature measurements
- `Generator.xlsx` - Signal generator analysis data
- `Wzmacniacz.xlsx` - Amplifier analysis measurements
- `TermOpor.xlsx` - Thermal resistance measurement data

---

## Additional Notes

- This tool is designed for educational purposes and assumes the input data follows the expected format.
- Contributions and suggestions for improvement are welcome!