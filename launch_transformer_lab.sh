#!/bin/bash

# Launch script for Electrical Engineering Laboratory - Transformer Analysis Tool

echo "=========================================="
echo "Electrical Engineering Laboratory"
echo "Transformer Analysis Tool"
echo "=========================================="
echo ""
echo "Checking dependencies..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3 to run this application"
    exit 1
fi

echo "Python 3: ✓"

# Check for required Python packages
python3 -c "import numpy" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Error: numpy is not installed"
    echo "Install with: pip install numpy"
    exit 1
fi
echo "numpy: ✓"

python3 -c "import matplotlib" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Error: matplotlib is not installed"
    echo "Install with: pip install matplotlib"
    exit 1
fi
echo "matplotlib: ✓"

python3 -c "import scipy" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Error: scipy is not installed"
    echo "Install with: pip install scipy"
    exit 1
fi
echo "scipy: ✓"

python3 -c "import tkinter" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Error: tkinter is not installed"
    echo "Install with: sudo apt-get install python3-tk (Ubuntu/Debian)"
    exit 1
fi
echo "tkinter: ✓"

echo ""
echo "All dependencies satisfied!"
echo "Launching Transformer Analysis Tool..."
echo ""

# Launch the application
python3 transformer_engineering_lab.py

echo ""
echo "Application closed."
