#!/Library/Frameworks/Python.framework/Versions/3.12/bin/python3
import tkinter as tk  # Importing the tkinter module for creating GUI applications
from tkinter import ttk, Text, END, StringVar  # Importing additional tkinter components for better styling and functionality
from googletrans import Translator, LANGUAGES  # Importing the Translator class for translation and LANGUAGES for language options

# BaseModel class for translation functionality
class BaseModel:
    def __init__(self):
        self.translator = Translator()  # Initialize the Google Translator object

    def translate(self, text, dest_language):
        # Abstract method to be implemented by subclasses for translation
        raise NotImplementedError("Subclasses should implement this method.")

# TranslationApp class inherits from BaseModel and ttk.Frame for GUI components
class TranslationApp(BaseModel, ttk.Frame):
    def __init__(self, parent=None):
        BaseModel.__init__(self)  # Call the constructor of BaseModel to initialize translation capabilities
        ttk.Frame.__init__(self, parent, padding="20 20 20 20")  # Initialize a frame with padding
        self.parent = parent  # Store the parent window
        self.initUI()  # Initialize the user interface

    def initUI(self):
        self.parent.title("SpeakEasy Translation App")  # Set the title of the window
        self.parent.configure(bg="#f0f0f0")  # Configure the background color of the window
        self.configure(style="TFrame")  # Apply style to the frame

        # Style configurations for the application
        style = ttk.Style()  # Create a style object for the application
        style.theme_use('clam')  # Use the 'clam' theme for the widgets
        style.configure("TFrame", background="#f0f0f0")  # Set the background color for the frame
        style.configure("TLabel", background="#f0f0f0", font=("Helvetica", 12))  # Configure label styles
        style.configure("TButton", font=("Helvetica", 12), padding=10)  # Configure button styles

        # Greeting label for the application
        greeting_label = ttk.Label(self, text="Welcome to SpeakEasy!", font=("Helvetica", 24, "bold"))
        greeting_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))  # Place greeting label in the grid

        # Input label for entering text
        input_label = ttk.Label(self, text="Enter text to translate:")
        input_label.grid(row=1, column=0, sticky="w", pady=(0, 5))  # Place input label in the grid

        # Text area for user input
        self.input_text = Text(self, height=6, width=50, font=("Helvetica", 12), wrap="word")
        self.input_text.grid(row=2, column=0, columnspan=2, pady=(0, 10), sticky="nsew")  # Place text area in the grid

        # Label for selecting target language
        self.language_label = ttk.Label(self, text="Translate to:")
        self.language_label.grid(row=3, column=0, sticky="w", pady=(0, 5))  # Place language label in the grid

        self.selected_language = StringVar(self)  # Create a StringVar to hold the selected language
        self.selected_language.set("Select Language")  # Set default value for language selection

        # Create a list of available languages with their full names and codes
        self.language_options = [(name.capitalize(), code) for code, name in LANGUAGES.items()]
        
        # Dropdown (Combobox) for language selection
        self.language_dropdown = ttk.Combobox(self, textvariable=self.selected_language, 
                                              values=[name for name, _ in self.language_options],
                                              state="readonly", font=("Helvetica", 12), width=30)
        self.language_dropdown.grid(row=3, column=1, sticky="e", pady=(0, 10))  # Place dropdown in the grid

        # Button to initiate translation
        translate_btn = ttk.Button(self, text="Translate", command=self.translate_text)
        translate_btn.grid(row=4, column=0, columnspan=2, pady=(0, 10))  # Place button in the grid

        # Label for displaying error messages
        self.error_label = ttk.Label(self, text="", foreground='red')
        self.error_label.grid(row=5, column=0, columnspan=2, pady=(0, 10))  # Place error label in the grid

        # Label for the translation output
        output_label = ttk.Label(self, text="Translation:")
        output_label.grid(row=6, column=0, sticky="w", pady=(0, 5))  # Place output label in the grid

        # Text area for displaying the translation output
        self.output_text = Text(self, height=6, width=50, state='disabled', 
                                bg='#e6f3ff', fg='#333333', font=("Helvetica", 12), 
                                wrap="word")
        self.output_text.grid(row=7, column=0, columnspan=2, sticky="nsew")  # Place output text area in the grid

        # Configure grid weights to allow resizing of components
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(7, weight=1)

    def translate_text(self):
        text = self.input_text.get("1.0", END).strip()  # Retrieve text from the input area
        dest_language = self.selected_language.get()  # Get the selected language from the dropdown
        self.error_label.config(text="")  # Clear any previous error messages

        # Check if the input text and selected language are valid
        if text and dest_language != "Select Language":
            # Find the corresponding language code for the selected language
            matching_codes = [code for name, code in self.language_options if name == dest_language]
            
            if matching_codes:  # Check if a matching code was found
                dest_language_code = matching_codes[0]  # Get the first matching code
                try:
                    translation = self.translate(text, dest_language_code)  # Call the translate method
                    self.display_result(translation)  # Display the translation result
                except Exception as e:
                    self.error_label.config(text="Translation error: " + str(e))  # Display any translation errors
            else:
                self.error_label.config(text="Invalid language selection.")  # Handle invalid language selections
        else:
            self.error_label.config(text="Please enter text and select a language.")  # Handle missing input

    def translate(self, text, dest_language):
        # Use the Google Translator to perform the translation
        translation = self.translator.translate(text, dest=dest_language)
        return translation.text  # Return the translated text

    def display_result(self, translation):
        self.output_text.config(state='normal')  # Enable editing to display the result
        self.output_text.delete("1.0", END)  # Clear any previous output
        self.output_text.insert(END, translation)  # Insert the new translation
        self.output_text.config(state='disabled')  # Disable editing to prevent user modification

# App class for running the Tkinter application
class App(tk.Tk):
    def __init__(self):
        super().__init__()  # Initialize the Tk class
        self.geometry("600x600")  # Set the initial window size
        self.app = TranslationApp(self)  # Create an instance of the TranslationApp class
        self.app.pack(fill=tk.BOTH, expand=True)  # Add the app frame to the window

# Main entry point to run the application
if __name__ == "__main__":
    app = App()  # Create an instance of the App class
    app.mainloop()  # Start the main event loop
