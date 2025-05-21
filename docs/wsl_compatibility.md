# WSL Compatibility Guide

This guide addresses compatibility considerations when running EyeType4You under Windows Subsystem for Linux (WSL).

## Challenges and Solutions

### GUI Support

PyQt5 requires X11 forwarding to display GUI elements from WSL:

1. **Install X Server on Windows**:
   - Install [VcXsrv](https://sourceforge.net/projects/vcxsrv/) or [Xming](https://sourceforge.net/projects/xming/)
   - Launch with "Disable access control" option checked

2. **Configure WSL Environment**:
   Add to your `~/.bashrc`:

   ```bash
   export DISPLAY=$(grep -m 1 nameserver /etc/resolv.conf | awk '{print $2}'):0
   export LIBGL_ALWAYS_INDIRECT=1
   ```

### Input Simulation Differences

The primary functionality challenge is keyboard input simulation, as WSL has a different input stack than native Windows.

**Platform-Specific Implementation:**

- Use `xdotool` and X11 utilities for input simulation in WSL.
- Use `pyautogui` or `keyboard` for native Windows.

### Data Path Differences

WSL has different path conventions than Windows. Use platform detection and path resolution utilities to ensure correct data/config locations.

## Implementation Strategy

- Detect WSL at runtime and use WSL-specific input and path logic.
- Provide a setup script for WSL dependencies and environment configuration.
- Test on both Windows and WSL.

## Dependencies for WSL

Install these additional dependencies when running in WSL:

```bash
sudo apt update
sudo apt install -y xdotool x11-utils python3-pyqt5 python3-pip
pip install pyautogui
```

## Automated WSL Setup

Create a script to automate WSL environment setup:

```bash
# Save to: scripts/setup_wsl.sh

# Check if running in WSL
if ! grep -q Microsoft /proc/version; then
    echo "This script is intended to run in WSL only."
    exit 1
fi

# Install required packages
sudo apt update
sudo apt install -y xdotool x11-utils python3-pyqt5 python3-pip

# Configure environment
if ! grep -q "export DISPLAY" ~/.bashrc; then
    echo 'export DISPLAY=$(grep -m 1 nameserver /etc/resolv.conf | awk "{print \$2}"):0' >> ~/.bashrc
    echo 'export LIBGL_ALWAYS_INDIRECT=1' >> ~/.bashrc
fi

# Test X11 connection
if xset q &>/dev/null; then
    echo "X11 connection successful"
else
    echo "X11 connection failed. Make sure X server is running on Windows host."
    echo "Install VcXsrv or Xming and launch with 'Disable access control' checked."
fi

echo "WSL setup complete!"
```

## See Also

- [PyQt5 X11 documentation](https://wiki.qt.io/Building_Qt_5_from_Git#X11)
- [xdotool documentation](https://manpages.ubuntu.com/manpages/bionic/man1/xdotool.1.html)
