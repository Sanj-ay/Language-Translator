import tkinter as tk
from tkinter import ttk, messagebox
from googletrans import Translator, LANGUAGES
import speech_recognition as sr

class TranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Language Translator")
        self.root.geometry("600x600")
        self.root.configure(bg="#baeef3")  # Set background color

        # Ensure the app closes completely when the window is closed
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Initialize the translator
        self.translator = Translator()

        # Create a style
        self.style = ttk.Style()
        self.style.configure("TCombobox", font=("Helvetica", 12), padding=5)
        self.style.configure("TButton", font=("Helvetica", 12), padding=5)

        # Create UI components
        self.create_widgets()

    def create_widgets(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg="#baeef3", padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Configure grid weights for responsiveness
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)

        # Source Language Section
        source_frame = tk.LabelFrame(main_frame, text="Source Language", bg="#64cfda", fg="black", padx=10, pady=10, font=("Helvetica", 13))
        source_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        source_frame.grid_rowconfigure(1, weight=1)  # Allow text area to expand

        self.source_lang = ttk.Combobox(source_frame, values=list(LANGUAGES.values()), state="readonly")
        self.source_lang.set("English")
        self.source_lang.pack(pady=5, fill=tk.X)

        self.source_text = tk.Text(source_frame, height=10, font=("Helvetica", 12), wrap=tk.WORD, bg="#FFCCCC")
        self.source_text.pack(pady=5, fill=tk.BOTH, expand=True)

        # Voice Recognition Button with green background
        self.recognize_button = tk.Button(source_frame, text="Speak", command=self.recognize_speech, bg="#23e194", fg="white", font=("Helvetica", 10))
        self.recognize_button.pack(pady=5)

        # Target Language Section
        target_frame = tk.LabelFrame(main_frame, text="Target Language", bg="#64cfda", fg="black", padx=10, pady=10, font=("Helvetica", 13))
        target_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        target_frame.grid_rowconfigure(1, weight=1)  # Allow text area to expand

        self.target_lang = ttk.Combobox(target_frame, values=list(LANGUAGES.values()), state="readonly")
        self.target_lang.set("Hindi")
        self.target_lang.pack(pady=5, fill=tk.X)

        self.translated_text = tk.Text(target_frame, height=10, font=("Helvetica", 12), wrap=tk.WORD, bg="#FFCCCC")
        self.translated_text.pack(pady=5, fill=tk.BOTH, expand=True)

        # Translate Button
        self.translate_button = tk.Button(main_frame, text="Translate", command=self.translate_text, bg="#23e194", fg="white")
        self.translate_button.grid(row=1, column=0, columnspan=2, pady=20)

    def recognize_speech(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            messagebox.showinfo("Info", "Please speak now...")
            audio = recognizer.listen(source)

            try:
                # Using Google Web Speech API to recognize speech
                text = recognizer.recognize_google(audio)
                self.source_text.delete("1.0", tk.END)  # Clear existing text
                self.source_text.insert(tk.END, text)  # Insert recognized text

            except sr.UnknownValueError:
                messagebox.showerror("Error", "Could not understand audio.")
            except sr.RequestError as e:
                messagebox.showerror("Error", f"Could not request results from Google Speech Recognition service; {e}")

    def translate_text(self):
        try:
            source_language = list(LANGUAGES.keys())[list(LANGUAGES.values()).index(self.source_lang.get().lower())]
            target_language = list(LANGUAGES.keys())[list(LANGUAGES.values()).index(self.target_lang.get().lower())]
            text_to_translate = self.source_text.get("1.0", tk.END).strip()

            if not text_to_translate:
                messagebox.showerror("Error", "Please enter text to translate.")
                return

            # Translate the text
            translated = self.translator.translate(text_to_translate, src=source_language, dest=target_language)
            self.translated_text.delete("1.0", tk.END)
            self.translated_text.insert(tk.END, translated.text)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def on_closing(self):
        # This method is called when the window is closed
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = TranslatorApp(root)
    root.mainloop()
