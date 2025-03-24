import sqlite3
import os

class DatabaseManager:
    def __init__(self, db_name='math_quiz.db'):
        """
        Initialize database connection and create necessary tables
        """
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_tables()

    def connect(self):
        """
        Establish a connection to the SQLite database
        """
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            print("Database connection established successfully.")
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")

    def create_tables(self):
        """
        Create necessary tables for the quiz game
        """
        # Players table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            total_games INTEGER DEFAULT 0,
            total_score INTEGER DEFAULT 0,
            highest_score INTEGER DEFAULT 0
        )
        ''')

        # Quiz Results table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS quiz_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_id INTEGER,
            quiz_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            difficulty TEXT,
            score INTEGER,
            total_questions INTEGER,
            FOREIGN KEY(player_id) REFERENCES players(id)
        )
        ''')

        self.conn.commit()

    def add_player(self, username):
        """
        Add a new player to the database
        """
        try:
            self.cursor.execute('''
            INSERT OR IGNORE INTO players (username, total_games, total_score, highest_score) 
            VALUES (?, 0, 0, 0)
            ''', (username,))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.IntegrityError:
            print(f"Player {username} already exists.")
            return None

    def update_player_stats(self, username, score, total_questions):
        """
        Update player statistics after a quiz
        """
        try:
            # Get player ID
            self.cursor.execute('SELECT id FROM players WHERE username = ?', (username,))
            player_id = self.cursor.fetchone()[0]

            # Insert quiz result
            self.cursor.execute('''
            INSERT INTO quiz_results (player_id, difficulty, score, total_questions) 
            VALUES (?, ?, ?, ?)
            ''', (player_id, 'medium', score, total_questions))

            # Update player stats
            self.cursor.execute('''
            UPDATE players 
            SET total_games = total_games + 1, 
                total_score = total_score + ?, 
                highest_score = MAX(highest_score, ?)
            WHERE username = ?
            ''', (score, score, username))

            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error updating player stats: {e}")

    def get_top_players(self, limit=10):
        """
        Retrieve top players based on highest score
        """
        self.cursor.execute('''
        SELECT username, highest_score, total_games 
        FROM players 
        ORDER BY highest_score DESC 
        LIMIT ?
        ''', (limit,))
        return self.cursor.fetchall()

    def close(self):
        """
        Close database connection
        """
        if self.conn:
            self.conn.close()
            print("Database connection closed.")
