#!/bin/bash
# Quick start script for Induction Motor Lab

echo "=========================================="
echo "Three-Phase Induction Motor Analysis Lab"
echo "=========================================="
echo ""
echo "Checking Python dependencies..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed!"
    exit 1
fi

# Check for required packages
python3 -c "import numpy" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing numpy..."
    pip3 install numpy
fi

python3 -c "import matplotlib" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing matplotlib..."
    pip3 install matplotlib
fi

echo ""
echo "Starting Motor Lab..."
echo ""

# Run the application
python3 induction_motor_lab.py

echo ""
echo "Motor Lab closed."
