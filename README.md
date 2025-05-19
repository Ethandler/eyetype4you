# ️‍🗨️ Eyetype4You Bot

**Eyetype4You** is a premium AI-powered typing automation tool that simulates incredibly human-like typing—perfect for demonstrations, testing, or any situation where you need text entered naturally.*

## ✨ Key Features

- **🤖 Human-like Typing**: Simulates natural typing with realistic pauses, occasional typos and corrections
- **😎 Emoji Support**: Automatically handles emoji insertion seamlessly
- **🎨 Beautiful Themes**:
  - **Cyberpunk (Dark City)**: Deep blacks with neon blue accents for a futuristic feel
  - **Pink City (Light)**: Soft pinks and whites for a modern, bright experience
- **⚙️ Fully Customizable**:
  - Adjust typing speed from very fast to slow and natural
  - Control error frequency to match your typing style
  - Customize punctuation and thinking pauses
- **🔄 Multi-Bot Support**:
  - Run multiple typing bots concurrently
  - Target different windows or applications
  - Monitor progress and status in real-time

## 🚀 Why Eyetype4You?

Unlike other autotypers, Eyetype4You doesn't just dump text. It recreates the **authentic human typing experience** with:

- Strategic pauses after punctuation
- Natural hesitations between words
- Smart handling of code indentation
- Occasional typos with immediate corrections
- Perfect emoji insertion that works everywhere
- Multi-bot capability for complex testing or demonstration scenarios

## 🔧 How It Works

1. **Enter your text** (including emoji!) in the editor
2. Select your **speed and error rate** from the settings menu
3. Click "**Start Typing**" and select your target window
4. Watch Eyetype4You work its magic, typing naturally as a human would

### 🤖 Using Multi-Bot Feature

1. Click on the "**🤖 Multi-Bot**" menu at the top
2. Select "**Manage Bots**" to open the bot manager
3. Use "**Select Target Window**" to choose where bots will type
4. Click "**Add Bot**" to create a new bot with current text and settings
5. Monitor progress and status in the bot manager
6. Stop individual bots or all bots as needed

## 🎮 Controls & Settings

- **⚡ Speed Settings**: Choose from presets (Very Fast to Slow) or create a custom speed
- **🎯 Error Rate**: Adjust how often typos occur, from none to frequent
- **🎨 Themes**: Switch between Cyberpunk and Pink City themes to match your style
- **🤖 Multi-Bot Manager**: Create, monitor, and control multiple typing bots

## 🧠 Smart Typing Memory

Eyetype4You includes a sophisticated word memory system that:

- Learns from words you type frequently
- Adjusts confidence levels based on typing frequency
- Reduces errors on familiar words
- Applies natural decay to memory over time
- Works across multiple bots with thread-safe access

## 🔮 Coming Soon

- **Multiple Bot Personalities**: Different typing styles with unique error patterns
- **Bot Costumes**: Customize your bot's appearance with various character options
- **Background Operation**: Run in the background while you focus on other tasks
- **Text Templates**: Save commonly used text snippets for quick access
- **Advanced Scheduling**: Set up automated typing sessions at specific times

## 📋 System Requirements

- Windows 10/11 (64-bit)
- 50MB disk space
- 4GB RAM recommended

## 📄 License

© 2024 Eyetype4You. All rights reserved.
This software is licensed, not sold. Unauthorized distribution is prohibited.

## Build Instructions

### 1. Build the EXE (with PyInstaller)

Make sure you have all dependencies installed:

```sh
# ...existing code...
```

Then run:

```sh
pyinstaller --onefile --windowed --icon assets/eyes.ico --add-data "assets;assets" main.py
```

- This will bundle the assets folder and use your icon from `assets/eyes.ico`.
- The output EXE will be in the `dist/` folder.

If you want to include other files (like `word_memory.json`):

```sh
pyinstaller --onefile --windowed --icon assets/eyes.ico --add-data "assets;assets" --add-data "word_memory.json;." main.py
```

### 2. Test the EXE

- Run `dist/main.exe` and make sure all features and images work.

### 3. Build the Installer (Inno Setup)

- Open `Eyetype4YouInstaller.iss` in Inno Setup Compiler.
- Make sure the `[Files]` section includes:

```ini
Source: "dist\main.exe"; DestDir: "{app}"
Source: "assets\*"; DestDir: "{app}\assets"; Flags: recursesubdirs
Source: "word_memory.json"; DestDir: "{app}"
```

- Set the icon for the installer and shortcut:

```ini
[Icons]
Name: "{group}\Eyetype4You"; Filename: "{app}\main.exe"; IconFilename: "{app}\assets\eyes.ico"
```

- Compile the installer.

---

## Notes

- If you add new assets, update the `--add-data` argument.
- If you change the EXE name, update the installer script accordingly.
- For advanced PyInstaller options, consider using a `.spec` file.

## EyeType4You - User Guide

## Introduction

Welcome to EyeType4You! This intelligent typing assistant helps you type text into any application with customizable typing patterns that mimic natural human typing. This guide will walk you through all features of the application and how to use them effectively.

## Getting Started

### Main Interface Overview

When you first open EyeType4You, you'll see the main interface with these components:

- **Text Editor**: The large text area where you enter the text you want the bot to type
- **Quick Templates**: A sidebar with pre-set text snippets
- **Control Buttons**: Start Typing and Close buttons
- **Status Indicators**: Shows current speed, error rate, theme, and other settings
- **Option Checkboxes**: Background Mode and Notepad Mode toggles

### Basic Typing

1. **Enter text**: Type or paste the content you want the bot to type into the text editor
2. **Configure settings**: Adjust typing speed, error rate, etc. (more on this below)
3. **Click "Start Typing"**: You'll have a few seconds to click into your target application
4. **Watch the magic**: The bot will begin typing your text with human-like patterns

## Settings and Configuration

### Speed Settings

Access speed settings from: **Settings Menu → Speed**

- **Slow (0.20s)**: Deliberate, careful typing
- **Normal (0.12s)**: Average human typing speed
- **Fast (0.08s)**: Quick typist
- **Very Fast (0.05s)**: Power user speed
- **Custom Speed**: Set your own precise timing

### Error Rate

Control typing accuracy from: **Settings Menu → Errors**

- **No Errors (0%)**: Perfect typing
- **Low (1%)**: Occasional mistakes
- **Medium (2%)**: Regular typos
- **High (5%)**: Frequent errors
- **Custom Error Rate**: Set your own error percentage

### Special Modes

- **Background Mode**: When enabled, the bot continues typing even if you switch to another window
- **Notepad Mode**: Optimized for text editors like Notepad, improving compatibility

### Themes

Choose visual themes from: **Settings Menu → Theme**

- **Cyberpunk (Dark City)**: Dark mode with neon accents
- **Pink City (Light)**: Light mode with pink accents

## Bot Personalities

EyeType4You uses personality profiles to create more natural typing patterns.

### Selecting a Personality

1. Access personalities from: **Settings Menu → Bot Personalities**
2. In the dialog, browse the available personalities
3. Click on a personality to see its details
4. Click "Select This Personality" to apply it

Each personality affects:

- Typing speed
- Error frequency
- Pause patterns
- How corrections are handled
- Emoji typing style
- And more subtle behaviors

### Creating Custom Personalities

1. In the personality dialog, go to the "Create New" tab
2. Fill in the name and description
3. Adjust typing parameters to your preference
4. Configure advanced parameters like correction style
5. Click "Create Personality"

### Managing Custom Personalities

Use the "Manage Custom" tab to:

- View your custom personalities
- Delete unwanted personalities
- Edit existing personalities (in future updates)

## Multi-Bot Feature

EyeType4You supports running multiple typing bots simultaneously.

### Setting Up Multiple Bots

1. Access the Multi-Bot menu from: **Multi-Bot Menu**
2. Select "Manage Bots" to open the management dialog
3. Click "Add Bot" to create a new bot instance
4. Provide a name for your bot
5. Use "Select Target Window" to pre-select where the bot will type

### Bot Management

In the Multi-Bot Manager:

- View all active bots and their progress
- Stop individual bots with "Stop Selected"
- Stop all bots with "Stop All"
- See detailed status information
- Monitor errors and progress

## Word Memory System

EyeType4You learns which words you use frequently and adapts its typing behavior.

### Word Memory Features

Access from: **Word Memory Menu**

- **View Statistics**: See overall memory stats
- **View Difficult Words**: Check which words the bot finds challenging
- **Reset Memory**: Clear all word learning data (use with caution)

Words typed frequently become more "familiar" to the bot, resulting in:

- Fewer typing errors
- More confident typing (fewer pauses)
- More natural rhythm variations

## Templates

Quick Templates allow you to insert frequently used text snippets.

### Using Templates

1. Click on any template in the sidebar to insert it at the cursor position
2. Templates maintain their formatting and special characters

### Creating Custom Templates

1. Click "Add New" in the Templates sidebar
2. Enter your template text in the dialog
3. Click "Save Template"
4. Your custom template will appear in the list

## Tips and Tricks

- **Emoji Support**: The bot can type emojis! 😊 Just include them in your text
- **Autocorrect**: Common misspellings are automatically corrected as you type
- **Code Typing**: Some personalities have better support for code with proper indentation
- **Typing Pauses**: The bot naturally pauses at punctuation and between words
- **Focus Management**: When using multiple bots, they'll coordinate focus between windows

## Troubleshooting

- **Window Focus Issues**: If the bot can't focus on your target window, try disabling background mode
- **Special Characters**: Some applications may not support certain special characters - the bot will try to substitute with standard alternatives
- **Performance**: Running too many bots simultaneously may affect performance

---

We hope this guide helps you get the most out of EyeType4You! Happy typing!
