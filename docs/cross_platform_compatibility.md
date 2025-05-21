# Cross-Platform Compatibility

EyeType4You supports both Windows and WSL (Windows Subsystem for Linux) environments with platform-specific adaptations. This guide outlines the differences and considerations for each platform.

## Windows

- **Input Simulation**: Uses native input simulation via PyAutoGUI/keyboard library
- **Data Storage**: Stores data in `%APPDATA%\EyeType4You`
- **GUI Rendering**: Native Windows rendering via PyQt5

## WSL (Windows Subsystem for Linux)

- **Input Simulation**: Uses xdotool for keyboard simulation via X11
- **Data Storage**: Follows XDG Base Directory Specification
  - Configuration: `~/.config/eyetype4you`
  - Data: `~/.local/share/eyetype4you`
- **GUI Rendering**: Requires X11 forwarding to a Windows X server
- **Requirements**: Needs an X server on Windows host, xdotool, and X11 utilities

## Platform Detection

The application automatically detects the runtime environment and adapts its behavior accordingly:

```python
from eyetype4you.utils.platform_detector import is_wsl

if is_wsl():
    # WSL-specific behavior
else:
    # Windows-specific behavior
```

## Setting Up WSL Environment

See the [WSL Compatibility Guide](wsl_compatibility.md) for detailed setup instructions.

A setup script is provided to automate the configuration process:

```bash
# From the project root
bash scripts/setup_wsl.sh
```

## Path Resolution

The application handles path resolution automatically, ensuring data and configuration files are stored in the appropriate locations for each platform:

```python
from eyetype4you.utils.path_resolver import get_data_dir, get_config_dir

data_dir = get_data_dir()  # Platform-specific data directory
config_dir = get_config_dir()  # Platform-specific config directory
```

## Development Considerations

When adding new features or modifying existing ones, consider these guidelines:

1. **Platform-Specific Code**: Use the `is_wsl()` function to separate platform-specific implementations:

   ```python
   from eyetype4you.utils.platform_detector import is_wsl
   
   def perform_action():
       if is_wsl():
           # WSL implementation
       else:
           # Windows implementation
   ```

2. **File Paths**: Always use the path resolution utilities instead of hardcoded paths:

   ```python
   from eyetype4you.utils.path_resolver import get_data_dir
   
   data_path = get_data_dir() / "my_file.json"
   ```

3. **Testing**: Create platform-specific tests and mark them to be skipped on platforms where they don't apply:

   ```python
   import pytest
   from eyetype4you.utils.platform_detector import is_wsl
   
   @pytest.mark.skipif(not is_wsl(), reason="WSL-specific test")
   def test_wsl_feature():
       # Test WSL-specific functionality
   ```

4. **Dependencies**: Document platform-specific dependencies in requirements files and installation instructions.

## Common Issues

### WSL GUI Not Displaying

1. Check if an X server is running on Windows
2. Verify the DISPLAY environment variable is set correctly
3. Check firewall settings to allow X server connections

### WSL Input Not Working

1. Verify xdotool is installed: `which xdotool`
2. Check X11 connection: `xset q`
3. Try simulating input manually: `xdotool type "test"`

### Path Resolution Issues

1. Check if the application can access the required directories
2. Ensure proper permissions are set
3. Verify directory structure exists
