# EyeType4You Developer Guide

## Project Structure

```
eyetype4you/
├── src/
│   └── eyetype4you/
│       ├── bot/            # Bot personality and configuration
│       ├── core/           # Core typing engine and word memory
│       ├── ui/             # Qt-based user interface
│       ├── utils/          # Utilities like emoji handling
│       └── multibot/       # Multi-bot management
├── assets/                 # Icons and resources
├── data/                   # Configuration and templates
├── docs/                   # Documentation
├── tests/                  # Unit and integration tests
├── scripts/                # Build and utility scripts
└── installer/              # Installer configuration
```

## Development Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

2. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

## Key Components

### TypingEngine
- Handles core typing simulation
- Manages typing speed and patterns
- Integrates with word memory system

### BotPersonality
- Defines typing characteristics
- Controls error rates and timing
- Customizable through UI

### WordMemory
- Learns from typing patterns
- Adapts confidence levels
- Thread-safe for multi-bot use

### MultiBotManager
- Coordinates multiple typing instances
- Manages bot lifecycles
- Handles resource allocation

## Building and Testing

### Running Tests
```bash
pytest
```

### Building the Executable
```bash
python scripts/build_exe.py
```

### Creating the Installer
1. Install Inno Setup
2. Open `installer/setup.iss`
3. Click Compile

## Contributing Guidelines

1. Fork the repository
2. Create a feature branch
3. Write tests for new features
4. Ensure all tests pass
5. Submit a pull request

## Code Style

- Follow PEP 8
- Use type hints
- Document public APIs
- Keep methods focused and small

## Thread Safety

The application uses multiple threads for:
- UI responsiveness
- Concurrent typing bots
- Word memory updates

Ensure thread safety when:
- Accessing shared resources
- Modifying word memory
- Managing bot states