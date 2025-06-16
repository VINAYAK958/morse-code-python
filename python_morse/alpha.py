import pyaudio
import numpy as np
import time
import tkinter as tk  # Import tkinter for GUI functionality
from tkinter import messagebox  # Import messagebox for displaying messages
from morse_logic import DICT
import speech_recognition as sr  # Import the speech recognition library
# Reverse dictionary for Morse-to-text conversion
REVERSE_DICT = {morse: char for char, morse in DICT.items()}

# Global variables for settings (to be set by GUI)
FREQUENCY = 800  # Frequency in Hz (set by GUI)
DOT_LENGTH = 0.1  # Dot length in seconds (set by GUI)
VOLUME = 0.5      # Volume (0.0 to 1.0, set by GUI)

# Audio settings
RATE = 44100        # Sampling rate

# Initialize PyAudio
p = pyaudio.PyAudio()
stream_out = p.open(format=pyaudio.paFloat32, channels=1, rate=RATE, output=True)

def play_beep(duration, frequency, volume):
    samples = (np.sin(2 * np.pi * np.arange(RATE * duration) * frequency / RATE)).astype(np.float32)
    samples *= volume
    stream_out.write(samples)

def play_morse_code(morse_code, dot_length, frequency, volume):
    """Play Morse code audio."""
    for symbol in morse_code:
        if symbol == '.':
            play_beep(dot_length, frequency, volume)  # Play for DOT_LENGTH
            time.sleep(dot_length)  # Pause for DOT_LENGTH
        elif symbol == '-':
            play_beep(dot_length * 3, frequency, volume)  # Play for DASH (3 * DOT_LENGTH)
            time.sleep(dot_length)  # Pause for DOT_LENGTH
        elif symbol == ' ':
            time.sleep(dot_length * 3)  # Pause between letters (3 * DOT_LENGTH)
        elif symbol == '/':
            time.sleep(dot_length * 7)  # Pause between words (7 * DOT_LENGTH)

def text_to_morse(text):
    """Convert text to Morse code."""
    text = text.upper()
    return ' '.join(DICT.get(char, '') for char in text)

def morse_to_text(morse):
    """Convert Morse code to text."""
    words = morse.strip().split(' / ')
    decoded_words = []
    for word in words:
        letters = word.split()
        decoded_word = ''.join(REVERSE_DICT.get(letter, '') for letter in letters)
        decoded_words.append(decoded_word)
    return ' '.join(decoded_words)

def voice_to_morse(self):
    """Capture voice input, convert it to English text, and then to Morse code."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        messagebox.showinfo("Voice Input", "Please speak now...")
        try:
            # Capture voice input
            audio = recognizer.listen(source, timeout=5)
            # Convert voice to English text
            english_text = recognizer.recognize_google(audio)
            messagebox.showinfo("Recognized Text", f"Recognized Text: {english_text}")
            
            # Convert English text to Morse code
            morse_code = text_to_morse(english_text)
            self.text_input.delete("1.0", "end")
            self.text_input.insert("1.0", english_text)  # Display English text in input box
            self.morse_output.config(state="normal")
            self.morse_output.delete("1.0", "end")
            self.morse_output.insert("1.0", morse_code)  # Display Morse code in output box
            self.morse_output.config(state="disabled")
        except sr.UnknownValueError:
            messagebox.showerror("Error", "Could not understand the audio.")
        except sr.RequestError as e:
            messagebox.showerror("Error", f"Could not request results; {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
