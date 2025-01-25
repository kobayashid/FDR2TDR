# FDR2TDR.py

## Overview
`FDR2TDR.py` is a Python script that processes a Touchstone file (`.s1p`) to analyze the time-domain step response for TDR (Time Domain Reflectometry) applications. The program reads the input file, performs the necessary signal processing, and outputs the results as a CSV file. It also visualizes the step response in a plot.

## Usage
```bash
python FDR2TDR.py input.s1p output.csv
```

- `input.s1p`: The input Touchstone file containing frequency-domain S11 data.
- `output.csv`: The output CSV file to save the processed data (location and real part of the step response).

## Example
Run the script with:
```bash
python FDR2TDR.py sample.s1p results.csv
```

## Notes
- The velocity factor used in the distance calculation is initially set to 0.66. This corresponds to a standard 50 Ω coaxial cable. It should be appropriately changed by the user according to the measurement conditions.
