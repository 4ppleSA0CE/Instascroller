# Instascroller

A Voice-Controlled Instagram Autoscroller MVP - Control Instagram scrolling hands-free using voice commands.

## Features

- **Voice Recognition**: Uses Google Web Speech API for accurate voice command recognition
- **Simple Commands**: Supports basic commands like "scroll", "down", "up", and "stop"
- **Desktop Integration**: Works with any desktop browser running Instagram
- **Graceful Shutdown**: Clean exit with Ctrl+C or voice command
- **Error Handling**: Robust error handling and troubleshooting guidance

## Requirements

- Python 3.7+
- Working microphone
- Internet connection (required for Google Speech API)
- Desktop browser with Instagram open

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/Instascroller.git
cd Instascroller
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

### Windows Users
If you encounter issues with PyAudio installation on Windows, try:
```bash
pip install pipwin
pipwin install pyaudio
```

### macOS Users
You may need to install portaudio first:
```bash
brew install portaudio
pip install pyaudio
```

### Linux Users
Install the required system packages:
```bash
sudo apt-get install python3-pyaudio portaudio19-dev
pip install pyaudio
```

## Usage

1. **Open Instagram**: Launch Instagram in your desktop browser
2. **Make Instagram Active**: Click on the Instagram tab/window to ensure it's the active window
3. **Run the Script**: Execute the voice controller:
```bash
python instascroller.py
```

4. **Follow Instructions**: The script will guide you through microphone calibration
5. **Voice Commands**: Once calibrated, say any of these commands:
   - `"scroll"` or `"down"` - Scroll down on Instagram
   - `"up"` - Scroll up on Instagram  
   - `"stop"`, `"quit"`, or `"exit"` - End the session

6. **Exit**: Press `Ctrl+C` or say `"stop"` to exit gracefully

## Voice Commands

| Command | Action |
|---------|--------|
| `scroll`, `down`, `scroll down` | Scroll down on Instagram |
| `up`, `scroll up` | Scroll up on Instagram |
| `stop`, `quit`, `exit` | End the voice control session |

## Troubleshooting

### Microphone Issues
- Ensure your microphone is working and not muted
- Check microphone permissions in your system settings
- Try speaking clearly and at normal volume

### Speech Recognition Issues
- Verify your internet connection (Google Speech API requires internet)
- Speak clearly and avoid background noise
- Try adjusting microphone sensitivity in system settings

### PyAutoGUI Issues
- Make sure Instagram is the active window when giving commands
- On some systems, you may need to grant accessibility permissions
- The failsafe feature will stop the script if you move your mouse to a corner

### Installation Issues
- Make sure you're using Python 3.7 or higher
- Try using a virtual environment to avoid dependency conflicts
- For PyAudio issues, refer to the installation section above

## Technical Details

This MVP uses:
- **SpeechRecognition**: For voice command capture and processing
- **Google Web Speech API**: For speech-to-text conversion
- **PyAutoGUI**: For simulating mouse scroll actions
- **PyAudio**: For microphone access and audio processing

## Future Enhancements

This MVP establishes the foundation for future improvements:
- Selenium-based browser control for more precise Instagram interaction
- Hotword detection for always-on listening
- Continuous background listening mode
- Standalone desktop application packaging
- Additional voice commands (like, comment, share)
- Multi-platform support and mobile integration

## License

This project is open source. Feel free to contribute and improve!

## Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

