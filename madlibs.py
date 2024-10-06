import random
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Templates for different themes
TEMPLATES = {
    "adventure": "Once upon a time, a {adjective} {noun} decided to {verb} through the {place}. It was an experience they would never {verb2}.",
    "sci-fi": "In the year {year}, a {adjective} astronaut discovered a {noun} on planet {place}. It started to {verb}, and the crew was {emotion}.",
    "horror": "It was a {adjective} night when the {noun} appeared in the {place}. Everyone tried to {verb}, but it was too late."
}

# Lists for random suggestions
ADJECTIVES = ["spooky", "brave", "mysterious", "giant"]
NOUNS = ["dragon", "castle", "robot", "ghost"]
VERBS = ["run", "fly", "scream", "discover"]
PLACES = ["forest", "moon", "ocean", "cave"]
YEARS = ["2023", "2087", "3000"]
EMOTIONS = ["terrified", "amazed", "confused"]


# Create the main application window
class MadLibsApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Advanced Mad Libs Game")
        self.geometry("600x500")
        self.configure(bg="lightblue")

        # Load and display image
        self.image = Image.open("mad_libs_image.jpeg")  # Change to your image path
        self.image = self.image.resize((200, 200), Image.LANCZOS)  # Use LANCZOS for resizing
        self.photo = ImageTk.PhotoImage(self.image)
        self.image_label = tk.Label(self, image=self.photo, bg="lightblue")
        self.image_label.pack(pady=10)

        # Theme selection
        self.theme_label = tk.Label(self, text="Choose a theme:", bg="lightblue", font=("Helvetica", 16))
        self.theme_label.pack(pady=10)

        self.theme_var = tk.StringVar()
        self.theme_var.set("adventure")  # Default value
        self.theme_menu = tk.OptionMenu(self, self.theme_var, *TEMPLATES.keys())
        self.theme_menu.pack(pady=10)

        # Input fields
        self.inputs = {}
        for word_type in ["adjective", "noun", "verb", "place", "year", "emotion", "verb2"]:
            entry = tk.Entry(self, width=40)
            entry.pack(pady=5)
            entry.insert(0, f"Enter a {word_type}")  # Default prompt
            entry.bind("<FocusIn>", lambda e, w=word_type: self.clear_input(w))  # Clear prompt on focus
            self.inputs[word_type] = entry

        # Generate story button
        self.generate_button = tk.Button(self, text="Generate Story", command=self.generate_story, bg="orange",
                                         font=("Helvetica", 14))
        self.generate_button.pack(pady=20)
        self.generate_button.bind("<Enter>", self.on_hover_enter)
        self.generate_button.bind("<Leave>", self.on_hover_leave)

        # End game button
        self.end_game_button = tk.Button(self, text="End Game", command=self.quit, bg="red", font=("Helvetica", 14))
        self.end_game_button.pack(pady=10)

        # Result display
        self.result_text = tk.Text(self, wrap=tk.WORD, height=10, width=50, bg="white", font=("Helvetica", 12))
        self.result_text.pack(pady=10)

    def clear_input(self, word_type):
        """Clear the input field when focused."""
        if self.inputs[word_type].get() == f"Enter a {word_type}":
            self.inputs[word_type].delete(0, tk.END)  # Clear input field

    def on_hover_enter(self, event):
        """Change button color on hover."""
        event.widget.config(bg="lightcoral")

    def on_hover_leave(self, event):
        """Revert button color when not hovering."""
        event.widget.config(bg="orange")

    def generate_story(self):
        """Generate a story based on user input and selected theme."""
        theme = self.theme_var.get()
        if theme not in TEMPLATES:
            messagebox.showerror("Error", "Invalid theme selected.")
            return

        placeholders = {}

        # Collect inputs or random suggestions
        for word_type in ["adjective", "noun", "verb", "place", "year", "emotion", "verb2"]:
            input_value = self.inputs[word_type].get().strip()  # Get the trimmed input
            if not input_value or input_value.startswith("Enter a"):  # If the input is empty or default prompt
                placeholders[word_type] = self.get_random_word(word_type)  # Use random value
            else:
                placeholders[word_type] = input_value  # Use user input

        # Create the story using the selected template
        story = TEMPLATES[theme].format(**placeholders)
        self.result_text.delete(1.0, tk.END)  # Clear previous text

        # Animate text display
        self.animate_text(story)

    def get_random_word(self, word_type):
        """Get a random word from the appropriate list."""
        if word_type == "adjective":
            return random.choice(ADJECTIVES)
        elif word_type == "noun":
            return random.choice(NOUNS)
        elif word_type == "verb":
            return random.choice(VERBS)
        elif word_type == "place":
            return random.choice(PLACES)
        elif word_type == "year":
            return random.choice(YEARS)
        elif word_type == "emotion":
            return random.choice(EMOTIONS)
        elif word_type == "verb2":
            return random.choice(VERBS)  # Use the same list for verb2 for now
        return None

    def animate_text(self, story):
        """Animate the text display character by character."""
        self.result_text.delete(1.0, tk.END)  # Clear previous text
        for char in story + "\n":  # Adding a new line at the end for a nice finish
            self.result_text.insert(tk.END, char)  # Insert one character at a time
            self.result_text.update()  # Update the text widget
            self.after(50)  # Delay for animation effect


if __name__ == "__main__":
    app = MadLibsApp()
    app.mainloop()
