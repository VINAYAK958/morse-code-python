# Python Morse Code Translator

This project is a Morse code translator that allows users to convert text to Morse code and vice versa. It also includes audio playback of Morse code signals. The application features a graphical user interface (GUI) that provides adjustable sliders for volume, speed, and frequency settings.

## Features

- **Text to Morse Code Conversion**: Convert plain text into Morse code.
- **Morse Code to Text Conversion**: Decode Morse code back into plain text.
- **Audio Playback**: Play Morse code audio signals corresponding to the input text.
- **Adjustable Settings**: Use sliders in the GUI to adjust volume, speed (DOT length), and frequency of the audio playback.

## Files

- `morse.py`: Contains the main logic for the Morse code translator, including conversion functions and audio playback.
- `gui.py`: Implements the GUI using Tkinter or PyQt, allowing users to adjust settings dynamically.

## Requirements

- Python 3.x
- Required libraries:
  - `numpy`
  - `scipy`
  - `pyaudio`
  - `tkinter` (or `PyQt` if using that for the GUI)

## Installation

1. Clone the repository or download the project files.
2. Install the required libraries using pip:
   ```
   pip install numpy scipy pyaudio
   ```
3. Run the application:
   ```
   python morse.py
   ```
   or
   ```
   python gui.py
   ```

## Usage

- Launch the application and choose the desired functionality from the menu.
- Use the GUI sliders to adjust volume, speed, and frequency settings as needed.
- Input text or Morse code as prompted to see the conversions and hear the audio playback.

## License

This project is licensed under the MIT License. Feel free to modify and distribute as needed.