# 👁️‍��️ Eyetype4You Bot

**Eyetype4You** is a premium AI-powered typing automation tool that simulates incredibly human-like typing—perfect for demonstrations, testing, or any situation where you need text entered naturally.

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

## 🚀 Why Eyetype4You?

Unlike other autotypers, Eyetype4You doesn't just dump text. It recreates the **authentic human typing experience** with:

- Strategic pauses after punctuation 
- Natural hesitations between words
- Smart handling of code indentation
- Occasional typos with immediate corrections
- Perfect emoji insertion that works everywhere

## 🔧 How It Works

1. **Enter your text** (including emoji!) in the editor
2. Select your **speed and error rate** from the settings menu
3. Click "**Start Typing**" and select your target window
4. Watch Eyetype4You work its magic, typing naturally as a human would

## 🎮 Controls & Settings

- **⚡ Speed Settings**: Choose from presets (Very Fast to Slow) or create a custom speed
- **🎯 Error Rate**: Adjust how often typos occur, from none to frequent
- **🎨 Themes**: Switch between Cyberpunk and Pink City themes to match your style

## 🔮 Coming Soon...

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
```
pip install -r requirements.txt
```

Then run:
```
pyinstaller --onefile --windowed --icon assets/eyes.ico --add-data "assets;assets" main.py
```
- This will bundle the assets folder and use your icon from `assets/eyes.ico`.
- The output EXE will be in the `dist/` folder.

If you want to include other files (like `word_memory.json`):
```
pyinstaller --onefile --windowed --icon assets/eyes.ico --add-data "assets;assets" --add-data "word_memory.json;." main.py
```

### 2. Test the EXE
- Run `dist/main.exe` and make sure all features and images work.

### 3. Build the Installer (Inno Setup)
- Open `Eyetype4YouInstaller.iss` in Inno Setup Compiler.
- Make sure the `[Files]` section includes:
  ```
  Source: "dist\main.exe"; DestDir: "{app}"
  Source: "assets\*"; DestDir: "{app}\assets"; Flags: recursesubdirs
  Source: "word_memory.json"; DestDir: "{app}"
  ```
- Set the icon for the installer and shortcut:
  ```
  [Icons]
  Name: "{group}\Eyetype4You"; Filename: "{app}\main.exe"; IconFilename: "{app}\assets\eyes.ico"
  ```
- Compile the installer.

---

## Notes
- If you add new assets, update the `--add-data` argument.
- If you change the EXE name, update the installer script accordingly.
- For advanced PyInstaller options, consider using a `.spec` file.
