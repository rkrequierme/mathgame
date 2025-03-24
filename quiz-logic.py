import random
import math

class QuizGenerator:
    def __init__(self, difficulty='medium', question_count=10):
        """
        Initialize quiz generator with difficulty and number of questions
        """
        self.difficulty = difficulty
        self.question_count = question_count
        self.operations = ['+', '-', '*', '/']
        
    def generate_question(self):
        """
        Generate a random math question based on difficulty
        """
        operation = random.choice(self.operations)
        
        if self.difficulty == 'easy':
            num1 = random.randint(1, 20)
            num2 = random.randint(1, 20)
        elif self.difficulty == 'medium':
            num1 = random.randint(10, 100)
            num2 = random.randint(10, 100)
        else:  # hard
            num1 = random.randint(50, 500)
            num2 = random.randint(50, 500)
        
        # Prevent division by zero and ensure integer division
        if operation == '/' and num2 == 0:
            num2 = random.randint(1, 10)
        
        # Ensure whole number division
        if operation == '/':
            num1 = num1 - (num1 % num2)
        
        question = f"{num1} {operation} {num2}"
        answer = self._calculate_answer(num1, num2, operation)
        
        return {
            'question': question,
            'answer': answer
        }
    
    def _calculate_answer(self, num1, num2, operation):
        """
        Calculate the correct answer for a math question
        """
        if operation == '+':
            return num1 + num2
        elif operation == '-':
            return num1 - num2
        elif operation == '*':
            return num1 * num2
        elif operation == '/':
            return num1 // num2  # Integer division
    
    def generate_quiz(self):
        """
        Generate a complete quiz with multiple questions
        """
        quiz = []
        for _ in range(self.question_count):
            quiz.append(self.generate_question())
        return quiz
