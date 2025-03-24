import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import random
from database import DatabaseManager
from quiz_logic import QuizGenerator

class MathQuizApp:
    def __init__(self, master):
        self.master = master
        master.title("🧮 Math Master Quiz 🎲")
        master.geometry("800x600")
        master.configure(bg='#2c3e50')

        # Database and Quiz Setup
        self.db_manager = DatabaseManager()
        self.quiz_generator = QuizGenerator()
        
        self.current_user = None
        self.current_quiz = None
        self.current_question_index = 0
        self.score = 0

        self.setup_ui()

    def setup_ui(self):
        """
        Set up the main user interface
        """
        # Title Label
        title_label = tk.Label(
            self.master, 
            text="🧮 Math Master Quiz 🎲", 
            font=('Arial', 24, 'bold'), 
            bg='#2c3e50', 
            fg='white'
        )
        title_label.pack(pady=20)

        # Frame for buttons
        button_frame = tk.Frame(self.master, bg='#2c3e50')
        button_frame.pack(expand=True)

        # Start Quiz Button
        start_button = tk.Button(
            button_frame, 
            text="Start New Quiz", 
            command=self.start_quiz,
            bg='#3498db', 
            fg='white', 
            font=('Arial', 16),
            activebackground='#2980b9'
        )
        start_button.pack(side=tk.LEFT, padx=10)

        # Leaderboard Button
        leaderboard_button = tk.Button(
            button_frame, 
            text="Leaderboard", 
            command=self.show_leaderboard,
            bg='#2ecc71', 
            fg='white', 
            font=('Arial', 16),
            activebackground='#27ae60'
        )
        leaderboard_button.pack(side=tk.LEFT, padx=10)

        # Quiz Frame (initially hidden)
        self.quiz_frame = tk.Frame(self.master, bg='#2c3e50')
        
        # Question Label
        self.question_label = tk.Label(
            self.quiz_frame, 
            text="", 
            font=('Arial', 20), 
            bg='#2c3e50', 
            fg='white'
        )
        self.question_label.pack(pady=20)

        # Answer Entry
        self.answer_entry = tk.Entry(
            self.quiz_frame, 
            font=('Arial', 18), 
            justify='center'
        )
        self.answer_entry.pack(pady=10)
        self.answer_entry.bind('<Return>', self.check_answer)

        # Submit Button
        submit_button = tk.Button(
            self.quiz_frame, 
            text="Submit Answer", 
            command=self.check_answer,
            bg='#e74c3c', 
            fg='white', 
            font=('Arial', 16)
        )
        submit_button.pack(pady=10)

    def start_quiz(self):
        """
        Start a new quiz
        """
        # Get username
        if not self.current_user:
            self.current_user = simpledialog.askstring(
                "Player Name", 
                "Enter your username:", 
                parent=self.master
            )
            if not self.current_user:
                return
            
            # Add player to database
            self.db_manager.add_player(self.current_user)

        # Generate quiz
        self.current_quiz = self.quiz_generator.generate_quiz()
        self.current_question_index = 0
        self.score = 0

        # Show quiz frame and hide main menu
        self.quiz_frame.pack(expand=True)
        
        # Load first question
        self.load_question()

    def load_question(self):
        """
        Load the current quiz question
        """
        if self.current_question_index < len(self.current_quiz):
            question = self.current_quiz[self.current_question_index]['question']
            self.question_label.config(text=f"Question {self.current_question_index + 1}: \n{question}")
            self.answer_entry.delete(0, tk.END)
        else:
            self.end_quiz()

    def check_answer(self, event=None):
        """
        Check the user's answer
        """
        try:
            user_answer = int(self.answer_entry.get())
            correct_answer = self.current_quiz[self.current_question_index]['answer']

            if user_answer == correct_answer:
                self.score += 1
                messagebox.showinfo("Correct!", "🎉 Great job! Your answer is correct.")
            else:
                messagebox.showinfo("Incorrect", f"❌ Sorry, the correct answer was {correct_answer}.")

            self.current_question_index += 1
            self.load_question()

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number.")

    def end_quiz(self):
        """
        End the quiz and show results
        """
        # Update player stats
        self.db_manager.update_player_stats(
            self.current_user, 
            self.score, 
            len(self.current_quiz)
        )

        # Show results
        result_message = f"""
        Quiz Complete! 🏆
        Player: {self.current_user}
        Score: {self.score}/{len(self.current_quiz)}
        Percentage: {(self.score/len(self.current_quiz))*100:.2f}%
        """
        messagebox.showinfo("Quiz Results", result_message)

        # Reset quiz state
        self.quiz_frame.pack_forget()

    def show_leaderboard(self):
        """
        Display top players in a new window
        """
        leaderboard_window = tk.Toplevel(self.master)
        leaderboard_window.title("🏆 Quiz Leaderboard")
        leaderboard_window.geometry("600x400")
        leaderboard_window.configure(bg='#2c3e50')

        # Leaderboard Label
        title_label = tk.Label(
            leaderboard_window, 
            text="Top Players", 
            font=('Arial', 20, 'bold'), 
            bg='#2c3e50', 
            fg='white'
        )
        title_label.pack(pady=10)

        # Treeview for leaderboard
        columns = ('Rank', 'Username', 'Highest Score', 'Total Games')
        tree = ttk.Treeview(leaderboard_window, columns=columns, show='headings')

        # Define headings
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor='center')

        # Fetch top players
        top_players = self.db_manager.get_top_players()
        for i, (username, score, games) in enumerate(top_players, 1):
            tree.insert('', 'end', values=(i, username, score, games))

        tree.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

def main():
    root = tk.Tk()
    app = MathQuizApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
