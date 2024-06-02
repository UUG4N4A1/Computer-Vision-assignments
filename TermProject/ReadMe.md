# Hand-Tracking Tic-Tac-Toe

This project implements a hand-tracking-based Tic-Tac-Toe game using OpenCV and a custom hand-tracking module. Players can use their hands to draw 'X' and 'O' on a virtual game board displayed on the screen.

## Features
- Hand tracking to detect finger positions.
- Interactive Tic-Tac-Toe game board.
- Real-time display with FPS counter.
- Player turn indication and win detection.

## Requirements
- Python 3.x
- OpenCV
- NumPy
- MediaPipe
- A custom hand-tracking module (handTrackingModule.py)

## Installation

1. Install the required packages:

` pip install opencv-python numpy `

2. Ensure you have a webcam connected to your computer.

## Usage

1. Run the main script:

` python main.py `

2. Instructions for playing:

- Use your hand to interact with the game.
- Make sure your webcam is capturing your hand properly.
- The game will display your moves and indicate the winner.

## Code Explanation

### Initialization
The initialization function sets up the game board zones and drawing parameters for 'X' and 'O'.

### Finding Zones
The find_zone function determines which zone of the board a point (x, y) belongs to.

### Drawing the Field
The draw_field function draws the game board with grid lines and player turn indication.

### Drawing 'X' and 'O'
The drawXO function places 'X' or 'O' on the board based on the player's turn and updates the game state.

### Game Logic
The game_logic function checks for win conditions and returns the winner if there is one.

### Main Function
The main function initializes the game, captures video from the webcam, tracks hand positions, and updates the game state in real-time.

## Example Pictures: 





