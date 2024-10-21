import tkinter as tk
from tkinter import messagebox

# Global variables
player = 'X'  # Human is 'X'
ai = 'O'  # AI is 'O'
board = [['' for _ in range(3)] for _ in range(3)]

# Function to check for a winner
def check_winner():
    # Check rows, columns, and diagonals
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != '':
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != '':
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] != '':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != '':
        return board[0][2]
    return None

# Function to check for a draw
def check_draw():
    for row in board:
        if '' in row:
            return False
    return True

# Minimax algorithm for AI decision-making
def minimax(depth, is_maximizing):
    winner = check_winner()
    if winner == ai:
        return 1
    elif winner == player:
        return -1
    elif check_draw():
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == '':
                    board[i][j] = ai
                    score = minimax(depth + 1, False)
                    board[i][j] = ''
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == '':
                    board[i][j] = player
                    score = minimax(depth + 1, True)
                    board[i][j] = ''
                    best_score = min(score, best_score)
        return best_score

# AI's move
def ai_move():
    best_score = -float('inf')
    move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == '':
                board[i][j] = ai
                score = minimax(0, False)
                board[i][j] = ''
                if score > best_score:
                    best_score = score
                    move = (i, j)
    if move:
        row, col = move
        buttons[row][col].config(text=ai, state="disabled", disabledforeground="#1e88e5")
        board[row][col] = ai
        check_game_over()

# Check if the game is over
def check_game_over():
    winner = check_winner()
    if winner:
        messagebox.showinfo("Game Over", f"'{winner}' wins!")
        reset_board()
    elif check_draw():
        messagebox.showinfo("Game Over", "It's a draw!")
        reset_board()

# Handle human player's move
def player_move(row, col):
    if board[row][col] == '':
        buttons[row][col].config(text=player, state="disabled", disabledforeground="#e53935")
        board[row][col] = player
        check_game_over()
        ai_move()

# Reset the board for a new game
def reset_board():
    global board
    board = [['' for _ in range(3)] for _ in range(3)]
    for row in range(3):
        for col in range(3):
            buttons[row][col].config(text='', state="normal")

# Create the main application window
root = tk.Tk()
root.title("Tic-Tac-Toe: Human vs AI 🤖")
root.geometry("400x450")
root.configure(bg="#e1f5fe")

# Title label
title = tk.Label(root, text="Tic-Tac-Toe", font=("Arial", 24, "bold"), bg="#4fc3f7", fg="white")
title.pack(pady=10)

# Frame for the board
board_frame = tk.Frame(root, bg="#e1f5fe")
board_frame.pack()

# Create 3x3 grid of buttons
buttons = [[None for _ in range(3)] for _ in range(3)]
for i in range(3):
    for j in range(3):
        button = tk.Button(board_frame, text='', font=("Arial", 20), width=5, height=2,
                           command=lambda i=i, j=j: player_move(i, j), bg="#b3e5fc")
        button.grid(row=i, column=j, padx=5, pady=5)
        buttons[i][j] = button

# Reset button
reset_button = tk.Button(root, text="Reset Game", font=("Arial", 14), bg="#4fc3f7", fg="white", command=reset_board)
reset_button.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()
