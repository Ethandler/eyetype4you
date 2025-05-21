#!/bin/bash
# Save to: scripts/setup_wsl.sh

# Check if running in WSL
if ! grep -q Microsoft /proc/version; then
    echo "This script is intended to run in WSL only."
    exit 1
fi

# Install required packages
echo "Installing required packages..."
sudo apt update
sudo apt install -y xdotool x11-utils python3-pyqt5 python3-pip

# Configure environment
echo "Configuring WSL environment..."
if ! grep -q "export DISPLAY" ~/.bashrc; then
    echo 'export DISPLAY=$(grep -m 1 nameserver /etc/resolv.conf | awk "{print \$2}"):0' >> ~/.bashrc
    echo 'export LIBGL_ALWAYS_INDIRECT=1' >> ~/.bashrc
    echo "Environment variables added to .bashrc"
fi

# Test X11 connection
echo "Testing X11 connection..."
if xset q &>/dev/null; then
    echo "X11 connection successful"
else
    echo "X11 connection failed. Make sure X server is running on Windows host."
    echo "Install VcXsrv or Xming and launch with 'Disable access control' checked."
fi

echo "WSL setup complete!"
