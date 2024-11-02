import sys
import os
import numpy as np
import matplotlib.pyplot as plt

# Check command-line arguments
if len(sys.argv) != 3:
    print("Usage: python xxx.py input.s1p output.csv")
    sys.exit(1)

# Get input and output file names from command-line arguments
input_filename = sys.argv[1]
output_filename = sys.argv[2]

# Check if the input file exists
if not os.path.isfile(input_filename):
    print(f"Error: The input file '{input_filename}' does not exist.")
    sys.exit(1)

# Read the Touchstone file (.s1p)
try:
    data = np.genfromtxt(input_filename, comments='#', delimiter=None)
except ValueError as e:
    print(f"Error reading file: {e}")
    sys.exit(1)

# Extract frequency and real/imaginary parts of S11
frequency = data[:, 0]  # Frequency (Hz)
s11_real = data[:, 1]   # Real part of S11
s11_imag = data[:, 2]   # Imaginary part of S11

# Convert S11 to complex format
s11_complex = s11_real + 1j * s11_imag

# Perform inverse Fourier transform (IFFT) to obtain the time-domain impulse response
impulse_response = np.fft.ifft(s11_complex, n=len(s11_complex))

# Integrate the impulse response to obtain the step response
step_response = np.cumsum(impulse_response)

# Calculate sampling interval (frequency spacing)
delta_f = frequency[1] - frequency[0]

# Calculate the time axis
c = 3e8  # Speed of light [m/s]
VF = 0.66  # Velocity factor for the 50-ohm coaxial cable

# Convert time to distance (considering round-trip and velocity factor)
time = np.fft.fftfreq(len(s11_complex), delta_f)
location = (c * VF * time) / 2  # Convert to distance [m]

# Keep only positive distances
positive_idx = np.where(location >= 0)
location = location[positive_idx]
step_response = step_response[positive_idx]

# Extract the real part of the step response
step_real = np.real(step_response)

# Save the TDR result to a CSV file
output_data = np.column_stack((location, step_real))
np.savetxt(output_filename, output_data, delimiter=',', header='Location [m], Real Part', comments='')

# Plot the graph
plt.figure(figsize=(12, 6))
plt.plot(location, step_real, label='Real Part', color='b')
plt.xlabel('Location [m]')
plt.ylabel('Amplitude')
plt.title('TDR Step Response')
plt.grid(True)
plt.xlim(0, max(location))  # Set display range from 0 to max distance
plt.legend()
plt.show()
