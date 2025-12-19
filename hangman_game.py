import tkinter as tk
from tkinter import messagebox
import random

class HangmanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Hangman Game")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f8ff")
        
        # Word list for the game
        self.word_list = ["PYTHON", "JAVASCRIPT", "PROGRAMMING", "DEVELOPER", 
                         "COMPUTER", "ALGORITHM", "FUNCTION", "VARIABLE", 
                         "INTERFACE", "DATABASE", "NETWORK", "SECURITY"]
        
        # Game variables
        self.secret_word = ""
        self.guessed_letters = []
        self.max_attempts = 6
        self.attempts_left = self.max_attempts
        self.game_over = False
        
        # Hangman drawing stages (0-6)
        self.hangman_stages = [
            # Stage 0: empty
            """
            
            
            
            
            
            """,
            # Stage 1: head
            """
            
            
                O
                
                
            """,
            # Stage 2: head and body
            """
            
            
                O
                |
                
            """,
            # Stage 3: head, body, left arm
            """
            
            
                O
               /|
                
            """,
            # Stage 4: head, body, both arms
            """
            
            
                O
               /|\\
                
            """,
            # Stage 5: head, body, both arms, left leg
            """
            
            
                O
               /|\\
               / 
            """,
            # Stage 6: complete hangman (game over)
            """
            
            
                O
               /|\\
               / \\
            """
        ]
        
        # Setup UI
        self.setup_ui()
        
        # Start a new game
        self.start_new_game()
    
    def setup_ui(self):
        # Title
        title_label = tk.Label(self.root, text="HANGMAN GAME", font=("Arial", 28, "bold"), 
                               bg="#f0f8ff", fg="#2c3e50")
        title_label.pack(pady=10)
        
        # Hangman drawing area
        self.hangman_canvas = tk.Text(self.root, width=30, height=10, font=("Courier", 14),
                                      bg="#f0f8ff", fg="#2c3e50", relief="flat", borderwidth=0)
        self.hangman_canvas.pack(pady=10)
        
        # Word display
        self.word_display = tk.Label(self.root, text="", font=("Arial", 32, "bold"), 
                                     bg="#f0f8ff", fg="#2980b9")
        self.word_display.pack(pady=20)
        
        # Attempts display
        self.attempts_label = tk.Label(self.root, text="", font=("Arial", 16), 
                                       bg="#f0f8ff", fg="#e74c3c")
        self.attempts_label.pack(pady=5)
        
        # Guessed letters display
        self.guessed_label = tk.Label(self.root, text="", font=("Arial", 14), 
                                      bg="#f0f8ff", fg="#7f8c8d")
        self.guessed_label.pack(pady=5)
        
        # Keyboard frame
        keyboard_frame = tk.Frame(self.root, bg="#f0f8ff")
        keyboard_frame.pack(pady=20)
        
        # Create letter buttons
        self.letter_buttons = []
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        
        # First row (A-M)
        first_row = tk.Frame(keyboard_frame, bg="#f0f8ff")
        first_row.pack()
        
        for i, letter in enumerate(letters[:13]):
            btn = tk.Button(first_row, text=letter, width=4, height=2, font=("Arial", 12, "bold"),
                           bg="#3498db", fg="white", activebackground="#2980b9",
                           command=lambda l=letter: self.guess_letter(l))
            btn.pack(side=tk.LEFT, padx=2, pady=2)
            self.letter_buttons.append(btn)
        
        # Second row (N-Z)
        second_row = tk.Frame(keyboard_frame, bg="#f0f8ff")
        second_row.pack()
        
        for i, letter in enumerate(letters[13:]):
            btn = tk.Button(second_row, text=letter, width=4, height=2, font=("Arial", 12, "bold"),
                           bg="#3498db", fg="white", activebackground="#2980b9",
                           command=lambda l=letter: self.guess_letter(l))
            btn.pack(side=tk.LEFT, padx=2, pady=2)
            self.letter_buttons.append(btn)
        
        # Control buttons
        button_frame = tk.Frame(self.root, bg="#f0f8ff")
        button_frame.pack(pady=20)
        
        new_game_btn = tk.Button(button_frame, text="New Game", font=("Arial", 14, "bold"),
                                bg="#2ecc71", fg="white", padx=20, pady=10,
                                activebackground="#27ae60", command=self.start_new_game)
        new_game_btn.pack(side=tk.LEFT, padx=10)
        
        hint_btn = tk.Button(button_frame, text="Hint", font=("Arial", 14, "bold"),
                            bg="#f39c12", fg="white", padx=20, pady=10,
                            activebackground="#d68910", command=self.show_hint)
        hint_btn.pack(side=tk.LEFT, padx=10)
        
        quit_btn = tk.Button(button_frame, text="Quit", font=("Arial", 14, "bold"),
                            bg="#e74c3c", fg="white", padx=20, pady=10,
                            activebackground="#c0392b", command=self.root.quit)
        quit_btn.pack(side=tk.LEFT, padx=10)
    
    def start_new_game(self):
        # Reset game variables
        self.secret_word = random.choice(self.word_list).upper()
        self.guessed_letters = []
        self.attempts_left = self.max_attempts
        self.game_over = False
        
        # Reset UI
        self.update_hangman_drawing()
        self.update_word_display()
        self.update_attempts_display()
        self.update_guessed_display()
        
        # Enable all letter buttons
        for btn in self.letter_buttons:
            btn.config(state=tk.NORMAL, bg="#3498db")
        
        # Update title
        self.root.title(f"Hangman Game - Guess the Word!")
    
    def guess_letter(self, letter):
        if self.game_over or letter in self.guessed_letters:
            return
        
        # Add to guessed letters
        self.guessed_letters.append(letter)
        
        # Check if letter is in the secret word
        if letter not in self.secret_word:
            self.attempts_left -= 1
        
        # Update UI
        self.update_hangman_drawing()
        self.update_word_display()
        self.update_attempts_display()
        self.update_guessed_display()
        
        # Disable the guessed letter button
        for btn in self.letter_buttons:
            if btn["text"] == letter:
                if letter in self.secret_word:
                    btn.config(state=tk.DISABLED, bg="#2ecc71")
                else:
                    btn.config(state=tk.DISABLED, bg="#e74c3c")
                break
        
        # Check game status
        self.check_game_status()
    
    def update_hangman_drawing(self):
        stage_index = self.max_attempts - self.attempts_left
        self.hangman_canvas.delete(1.0, tk.END)
        self.hangman_canvas.insert(1.0, self.hangman_stages[stage_index])
    
    def update_word_display(self):
        display_word = ""
        for letter in self.secret_word:
            if letter in self.guessed_letters:
                display_word += letter + " "
            else:
                display_word += "_ "
        
        self.word_display.config(text=display_word.strip())
    
    def update_attempts_display(self):
        self.attempts_label.config(text=f"Attempts remaining: {self.attempts_left}")
    
    def update_guessed_display(self):
        guessed_text = "Guessed letters: " + ", ".join(sorted(self.guessed_letters))
        self.guessed_label.config(text=guessed_text)
    
    def check_game_status(self):
        # Check for win
        if all(letter in self.guessed_letters for letter in self.secret_word):
            self.game_over = True
            messagebox.showinfo("Congratulations!", f"You won! The word was: {self.secret_word}")
            self.root.title(f"Hangman Game - You won! Word: {self.secret_word}")
            return
        
        # Check for loss
        if self.attempts_left <= 0:
            self.game_over = True
            messagebox.showinfo("Game Over", f"You lost! The word was: {self.secret_word}")
            self.root.title(f"Hangman Game - You lost! Word: {self.secret_word}")
    
    def show_hint(self):
        # Find a letter in the secret word that hasn't been guessed yet
        unguessed_letters = [letter for letter in self.secret_word if letter not in self.guessed_letters]
        
        if unguessed_letters and not self.game_over:
            # Give a random hint
            hint_letter = random.choice(unguessed_letters)
            messagebox.showinfo("Hint", f"Try the letter: {hint_letter}")
        elif self.game_over:
            messagebox.showinfo("Hint", "Game is over. Start a new game!")
        else:
            messagebox.showinfo("Hint", "You've already guessed all letters!")

def main():
    root = tk.Tk()
    game = HangmanGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()