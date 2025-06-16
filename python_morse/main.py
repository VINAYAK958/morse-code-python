import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pyttsx3  # Import the text-to-speech library
from alpha import VOLUME, DOT_LENGTH, FREQUENCY, text_to_morse, morse_to_text, play_morse_code
import time  # Import time for delays
import threading
import os
from datetime import datetime
import speech_recognition as sr  # Import the speech recognition library

import tkinter.messagebox as messagebox
# Set default values for global variables
VOLUME = 0.5       # Default volume (0.0 to 1.0)
DOT_LENGTH = 0.1   # Default dot length in seconds
FREQUENCY = 1000   # Default frequency in Hz

class MorseCodeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Morse Code Translator")
        self.root.minsize(800, 600)  # Set minimum window size
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        try:
            self.root.iconbitmap("morse_code_icon.ico")
        except Exception:
            print("Icon file not found. Skipping icon setup.")

        self.root.resizable(True, True) 
        self.tts_engine = pyttsx3.init()

        # Apply a theme
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", font=("Arial", 12))
        style.configure("TButton", font=("Arial", 12))
        style.configure("TEntry", font=("Arial", 18))
        style.configure("TScale", font=("Arial", 18))
        style.configure("TFrame", background="lightgrey")




        # Volume slider
        self.volume_label = ttk.Label(root, text="Volume (0.0 to 1.0):")
        self.volume_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.volume_value = tk.StringVar(value=f"{VOLUME:.2f}")
        self.volume_slider = ttk.Scale(root, from_=0.0, to=1.0, orient='horizontal', command=self.update_volume, length=300)
        self.volume_slider.set(VOLUME)  # Set default value
        self.volume_slider.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        self.volume_display = ttk.Label(root, textvariable=self.volume_value, width=6)
        self.volume_display.grid(row=0, column=2, padx=10, pady=5)



        # Speed slider
        self.speed_label = ttk.Label(root, text="Speed (DOT length in seconds):")
        self.speed_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.speed_value = tk.StringVar(value=f"{DOT_LENGTH:.2f}")
        self.speed_slider = ttk.Scale(root, from_=0.01, to=1.0, orient='horizontal', command=self.update_speed, length=300)
        self.speed_slider.set(DOT_LENGTH)  # Set default value
        self.speed_slider.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        self.speed_display = ttk.Label(root, textvariable=self.speed_value, width=6)
        self.speed_display.grid(row=1, column=2, padx=10, pady=5)




        # Frequency slider
        self.frequency_label = ttk.Label(root, text="Frequency (Hz):")
        self.frequency_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.frequency_value = tk.StringVar(value=f"{FREQUENCY}")
        self.frequency_slider = ttk.Scale(root, from_=100, to=2000, orient='horizontal', command=self.update_frequency, length=300)
        self.frequency_slider.set(FREQUENCY)  # Set default value
        self.frequency_slider.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        self.frequency_display = ttk.Label(root, textvariable=self.frequency_value, width=6)
        self.frequency_display.grid(row=2, column=2, padx=10, pady=5)




        # Text input for conversion with scrollbar
        self.text_input_label = ttk.Label(root, text="Enter text or Morse code:")
        self.text_input_label.grid(row=3, column=0, padx=10, pady=5, sticky="nw")
        self.text_input_frame = tk.Frame(root)
        self.text_input_frame.grid(row=3, column=1, padx=10, pady=5, sticky="ew")
        self.text_input_scrollbar = ttk.Scrollbar(self.text_input_frame, orient="vertical")
        self.text_input = tk.Text(self.text_input_frame, height=5, width=50, wrap="word", yscrollcommand=self.text_input_scrollbar.set)
        self.text_input_scrollbar.config(command=self.text_input.yview)
        self.text_input_scrollbar.pack(side="right", fill="y")
        self.text_input.pack(side="left", fill="both", expand=True)
        
        

        # clear button
        self.clear = ttk.Button(root, text="clear", command=self.clear_text)
        self.clear.grid(row=3, column=2, padx=5, pady=1, sticky="ew")


        # Morse code output with scrollbar
        self.morse_output_label = ttk.Label(root, text="Output (English Translation):")
        self.morse_output_label.grid(row=4, column=0, padx=10, pady=5, sticky="nw")
        self.morse_output_frame = tk.Frame(root)
        self.morse_output_frame.grid(row=4, column=1, padx=10, pady=5, sticky="ew")
        self.morse_output_scrollbar = ttk.Scrollbar(self.morse_output_frame, orient="vertical")
        self.morse_output = tk.Text(self.morse_output_frame, height=5, width=50, wrap="word", yscrollcommand=self.morse_output_scrollbar.set, state="disabled")
        self.morse_output_scrollbar.config(command=self.morse_output.yview)
        self.morse_output_scrollbar.pack(side="right", fill="y")
        self.morse_output.pack(side="left", fill="both", expand=True)
        self.voice_input_button = ttk.Button(root, text="Voice Input", command=self.voice_to_text)
        self.voice_input_button.grid(row=5, column=2, columnspan=3, padx=10, pady=5, sticky="ew")
        



        # Create a fixed blinking frame (initially white)
        self.blink_frame = tk.Frame(self.root, width=100, height=100, bg="white")
        self.blink_frame.grid(row=7, column=1, padx=10, pady=5)



        # Buttons for actions
        self.text_to_morse_button = ttk.Button(root, text="Convert to Morse", command=self.convert_to_morse)
        self.text_to_morse_button.grid(row=5, column=0, padx=10, pady=5, sticky="ew")



        self.morse_to_text_button = ttk.Button(root, text="Convert to Text", command=self.convert_to_text)
        self.morse_to_text_button.grid(row=5, column=1, padx=10, pady=5, sticky="ew")
        
        
        
        self.play_morse_button = ttk.Button(root, text="Play Morse Audio", command=self.play_morse_audio)
        self.play_morse_button.grid(row=6, column=0, padx=10, pady=5, sticky="ew")




        self.speak_button = ttk.Button(root, text="Speak", command=self.speak_text)
        self.speak_button.grid(row=6, column=1, padx=10, pady=5, sticky="ew")



        self.blink_button = ttk.Button(root,text="Blink Morse Code",command=lambda: self.blink_morse_code(self.get_morse_code_from_input()))
        self.blink_button.grid(row=7, column=0, padx=5, pady=5, sticky="ew")



        self.blink_and_audio_button = ttk.Button(root, text="Blink Morse Code with Audio", command=self.blink_and_audio_morse_code)
        self.blink_and_audio_button.grid(row=7, column=2, padx=5, pady=5, sticky="ew")




        self.quit_button = ttk.Button(root, text="Quit", command=root.quit)
        self.quit_button.grid(row=8, column=1, columnspan=2, padx=10, pady=5, sticky="ew")
        
        
        # font size spinbox        
        self.font_size_var = tk.IntVar(value=18)  # Default font size
        self.font_size_spinbox = tk.Spinbox(
            root, from_=8, to=40, width=10, textvariable=self.font_size_var, command=self.update_font_size
        )
        self.font_size_spinbox.grid(row=4, column=2, padx=12, pady=25, sticky="w")
        

        
        
        self.save_button = ttk.Button(root, text="Save", command=self.save_translation)
        self.save_button.grid(row=6, column=2, padx=10, pady=5, sticky="ew")

        self.load_button = ttk.Button(root, text="Load", command=self.load_translation)
        self.load_button.grid(row=6, column=3, padx=10, pady=5, sticky="ew")

    def save_translation(self):
        text = self.text_input.get("1.0", tk.END).strip()
        with open("saved_translation.txt", "w") as file:
            file.write(text)
        print("Translation saved to file.")  # Debugging statement

    def load_translation(self):
        
        try:
            with open("saved_translation.txt", "r") as file:
                loaded_text = file.read()
            self.text_input.delete(1.0, tk.END)  # Clear current text
            self.text_input.insert(tk.END, loaded_text)  # Insert loaded text
        except FileNotFoundError:
            print("No saved file found.")
   
        
        
        
        
        
                                                                                   
    def update_font_size(self):
        """Update the font size of the text input and output boxes."""
        size = self.font_size_var.get()
        new_font = ("Arial", size)

        # Update font for text input and output boxes only
        self.text_input.config(font=new_font)
        self.morse_output.config(font=new_font)


    
    def update_volume(self, value):
        global VOLUME
        VOLUME = float(value)
        self.volume_value.set(f"{VOLUME:.2f}")  # Update the displayed value
        print(f"Volume updated to: {VOLUME}")  # Debugging statement




    def update_speed(self, value):
        global DOT_LENGTH
        DOT_LENGTH = float(value)
        self.speed_value.set(f"{DOT_LENGTH:.2f}")  # Update the displayed value
        print(f"Speed (DOT length) updated to: {DOT_LENGTH}")  # Debugging statement




    def update_frequency(self, value):
        global FREQUENCY
        FREQUENCY = int(float(value))
        self.frequency_value.set(f"{FREQUENCY}")  # Update the displayed value
        print(f"Frequency updated to: {FREQUENCY}")  # Debugging statement




    def clear_text(self):
        """Clear the text input and output fields."""
        self.text_input.delete("1.0", "end")
        self.morse_output.config(state="normal")
        self.morse_output.delete("1.0", "end")
        self.morse_output.config(state="disabled")
        print("Text input and output cleared.")  # Debugging statement




    def convert_to_morse(self):
        text = self.text_input.get("1.0", "end").strip().upper()
        if not text:
            messagebox.showerror("Error", "Please enter text to convert.")
            return
        morse_code = text_to_morse(text)
        self.morse_output.config(state="normal")
        self.morse_output.delete("1.0", "end")
        self.morse_output.insert("1.0", morse_code)
        self.morse_output.config(state="disabled")




    def convert_to_text(self):
        morse_code = self.text_input.get("1.0", "end").strip()
        if not morse_code:
            messagebox.showerror("Error", "Please enter Morse code to convert.")
            return
        try:
            text = morse_to_text(morse_code)
            self.morse_output.config(state="normal")
            self.morse_output.delete("1.0", "end")
            self.morse_output.insert("1.0", text)
            self.morse_output.config(state="disabled")
        except ValueError as e:
            messagebox.showerror("Error", str(e))




    def play_morse_audio(self):
        """Play Morse code audio based on the input."""
        input_text = self.text_input.get("1.0", "end").strip()
        if not input_text:
            messagebox.showerror("Error", "Please enter text or Morse code to play.")
            return

        try:
            # Check if the input is valid Morse code
            if all(char in ".-/ " for char in input_text):
                # Play the Morse code audio directly
                play_morse_code(input_text, DOT_LENGTH, FREQUENCY, VOLUME)
            else:
                # Assume the input is English text, convert to Morse code
                morse_code = text_to_morse(input_text)
                self.morse_output.config(state="normal")
                self.morse_output.delete("1.0", "end")
                self.morse_output.insert("1.0", morse_code)
                self.morse_output.config(state="disabled")
                # Play the Morse code audio
                play_morse_code(morse_code, DOT_LENGTH, FREQUENCY, VOLUME)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")




    def blink_morse_code(self, morse_code):
        """Blink the fixed frame black and white based on Morse code."""
        def blink_sequence(index):
            if index >= len(morse_code):
                # Reset the frame to white after blinking is complete
                self.blink_frame.config(bg="white")
                return

            symbol = morse_code[index]
            if symbol == '.':
                self.blink_frame.config(bg="black")
                self.blink_frame.update()
                self.root.after(int(DOT_LENGTH * 1000), lambda: self.blink_frame.config(bg="white"))
                self.root.after(int(DOT_LENGTH * 2000), lambda: blink_sequence(index + 1))
            elif symbol == '-':
                self.blink_frame.config(bg="black")
                self.blink_frame.update()
                self.root.after(int(DOT_LENGTH * 3000), lambda: self.blink_frame.config(bg="white"))
                self.root.after(int(DOT_LENGTH * 4000), lambda: blink_sequence(index + 1))
            elif symbol == ' ':
                self.root.after(int(DOT_LENGTH * 3000), lambda: blink_sequence(index + 1))
            elif symbol == '/':
                self.root.after(int(DOT_LENGTH * 7000), lambda: blink_sequence(index + 1))

        # Start the blinking sequence
        blink_sequence(0)



    def get_morse_code_from_input(self):
        """Retrieve Morse code from the input field, converting English text if necessary."""
        input_text = self.text_input.get("1.0", "end").strip()
        if not input_text:
            messagebox.showerror("Error", "Please enter text or Morse code to blink.")
            return ""
        if not all(char in ".-/ " for char in input_text):
            return text_to_morse(input_text)  # Convert English text to Morse code
        return input_text  # Return Morse code directly



    def speak_text(self):
        """Speak the input text or Morse code."""
        input_text = self.text_input.get("1.0", "end").strip()
        if not input_text:
            messagebox.showerror("Error", "Please enter text or Morse code to speak.")
            return

        try:
            # Set the volume for the text-to-speech engine
            self.tts_engine.setProperty("volume", VOLUME)

            # Set the voice to Indian accent (Heera) if available
            voices = self.tts_engine.getProperty("voices")
            for voice in voices:
                if "zira" in voice.name.lower() or "heera" in voice.id.lower():
                    self.tts_engine.setProperty("voice", voice.id)
                    break

            # Check if the input is Morse code
            if all(char in ".-/ " for char in input_text):
                # Convert Morse code to English
                translated_text = morse_to_text(input_text)
                self.morse_output.config(state="normal")
                self.morse_output.delete("1.0", "end")
                self.morse_output.insert("1.0", translated_text)
                self.morse_output.config(state="disabled")
                # Speak the translated text
                self.tts_engine.say(translated_text)
            else:
                # Speak the English text directly
                self.tts_engine.say(input_text)

            self.tts_engine.runAndWait()
        except ValueError:
            messagebox.showerror("Error", "Invalid Morse code entered.")




    def blink_and_audio_morse_code(self):
        
        input_text = self.text_input.get("1.0", "end").strip()
        if not input_text:
            messagebox.showerror("Error", "Please enter text or Morse code to blink.")
            return

        # Convert to Morse if it's not already
        if not all(char in ".-/ " for char in input_text):
            morse_code = text_to_morse(input_text)
        else:
            morse_code = input_text

        def blink_and_play():
            for symbol in morse_code:
                if symbol == '.':
                    self.blink_frame.config(bg="black")
                    self.blink_frame.update()
                    play_morse_code(".", DOT_LENGTH, FREQUENCY, VOLUME)
                    time.sleep(DOT_LENGTH)
                    self.blink_frame.config(bg="white")
                    self.blink_frame.update()
                    time.sleep(DOT_LENGTH)
                elif symbol == '-':
                    self.blink_frame.config(bg="black")
                    self.blink_frame.update()
                    play_morse_code("-", DOT_LENGTH, FREQUENCY, VOLUME)
                    time.sleep(DOT_LENGTH * 3)
                    self.blink_frame.config(bg="white")
                    self.blink_frame.update()
                    time.sleep(DOT_LENGTH)
                elif symbol == ' ':
                    time.sleep(DOT_LENGTH * 3)
                elif symbol == '/':
                    time.sleep(DOT_LENGTH * 7)

            self.blink_frame.config(bg="white")

        # Run in a separate thread to prevent GUI freeze
        threading.Thread(target=blink_and_play).start()

    def voice_to_text(self):
        def recognize_speech():
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                try:
                    self.text_input.delete("1.0", "end")
                    self.text_input.insert("1.0", "Listening...")
                    self.root.update()

                    recognizer.adjust_for_ambient_noise(source, duration=1)
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)

                    text = recognizer.recognize_google(audio)

                    self.root.after(0, self.text_input.delete, "1.0", "end")
                    self.root.after(0, self.text_input.insert, "1.0", text)

                except sr.WaitTimeoutError:
                    self.root.after(0, self.text_input.delete, "1.0", "end")
                    self.root.after(0, self.text_input.insert, "1.0", "[Timeout: No speech detected]")
                except sr.UnknownValueError:
                    self.root.after(0, self.text_input.delete, "1.0", "end")
                    self.root.after(0, self.text_input.insert, "1.0", "[Could not understand audio]")
                except sr.RequestError as e:
                    self.root.after(0, self.text_input.delete, "1.0", "end")
                    self.root.after(0, self.text_input.insert, "1.0", f"[Error: {e}]")

        threading.Thread(target=recognize_speech).start()




if __name__ == "__main__":
    root = tk.Tk()
    app = MorseCodeGUI(root)
    root.mainloop()