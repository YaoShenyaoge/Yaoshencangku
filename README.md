# Snake Game

A classic Snake game implementation using Python and Pygame with smooth gameplay, multiple difficulty levels, and persistent high score tracking.

## Features

- **Classic Snake Gameplay**: Control the snake to eat food and grow longer
- **Multiple Difficulty Levels**: Easy, Medium, and Hard modes with adjustable speeds
- **Progressive Difficulty**: Speed increases slightly as your score grows
- **Score Tracking**: Current score display and persistent high score storage
- **Main Menu**: Intuitive menu system for starting games and selecting difficulty
- **Game Over Screen**: Shows final score and high score with restart option
- **Smooth Controls**: Arrow keys or WASD for intuitive snake control
- **Collision Detection**: Game ends when snake hits walls or itself

## Requirements

- Python 3.x
- Pygame library

## Installation

1. Clone or download this repository
2. Install the required dependencies:
   ```bash
   pip install pygame
   ```

## Running the Game

Execute the following command in the project directory:

```bash
python3 snake_game.py
```

## Game Controls

### Main Menu
- **S** - Start the game (go to difficulty selection)
- **Q** - Quit the game

### Difficulty Selection
- **1** - Select Easy mode (slower speed)
- **2** - Select Medium mode (normal speed)
- **3** - Select Hard mode (faster speed)
- **ESC** - Back to main menu

### During Gameplay
- **Arrow Keys** or **WASD** - Move the snake
  - **UP Arrow / W** - Move up
  - **DOWN Arrow / S** - Move down
  - **LEFT Arrow / A** - Move left
  - **RIGHT Arrow / D** - Move right

### Game Over Screen
- **R** - Restart the game (go to difficulty selection)
- **Q** or **ESC** - Return to main menu

## Game Mechanics

### Objective
Control the snake to eat the red food and grow as long as possible without hitting the walls or yourself.

### Starting Position
The snake starts with 3 segments in the center of the game board, facing right.

### Food
- Food appears at random locations on the grid
- Each piece of food eaten increases your score by 1
- The snake grows by 1 segment when eating food

### Game Board
- 20x20 grid game board
- Boundaries are at the edges of the window
- Game ends if the snake hits a boundary or itself

### Speed
- **Easy**: 5 moves per second
- **Medium**: 10 moves per second
- **Hard**: 15 moves per second

### High Score
- The highest score achieved is automatically saved to a `highscore.json` file
- High score persists between game sessions
- High score is displayed on the main menu, during gameplay, and on the game over screen

## Game Architecture

The game is implemented in a single file with the following components:

### Classes

#### `Direction` (Enum)
Represents the four cardinal directions and their corresponding movement vectors.

#### `Difficulty` (Enum)
Defines the three difficulty levels with their associated base speeds (moves per second).

#### `GameState` (Enum)
Represents the different states the game can be in: Menu, Difficulty Selection, Playing, and Game Over.

#### `SnakeGame`
The main game class handling all game logic, rendering, and state management.

**Key Methods:**
- `__init__()`: Initialize the game window, fonts, and game state
- `reset_game()`: Reset snake position, direction, score, and spawn food
- `spawn_food()`: Generate food at a random position not occupied by the snake
- `handle_input()`: Process keyboard input for different game states
- `update()`: Update game logic including snake movement and collision detection
- `check_collision()`: Detect collisions with walls and the snake itself
- `draw()`: Render the current game state
- `run()`: Main game loop

## File Structure

```
/home/engine/project/
├── snake_game.py          # Main game implementation
├── highscore.json         # High score storage (auto-generated)
└── README.md              # This file
```

## Technical Details

### Data Structures
- **Snake**: Implemented as a `deque` for efficient head insertion and tail removal
- **Food Position**: Stored as a tuple (x, y)
- **Direction/Movement**: Handled through enums with movement vectors

### Rendering
- 30x30 pixel cells on a 600x600 pixel window
- Dynamic font sizes for different UI elements
- Color-coded elements: Green for snake, Red for food, Yellow for accents

### Game Loop
- 60 FPS base frame rate
- Movement updates controlled by difficulty setting
- Smooth input handling without command queueing

## Troubleshooting

### Game window doesn't appear
- Ensure Pygame is properly installed: `pip install pygame`
- Check that your Python version is 3.x or later

### Controls not responding
- Make sure you're clicking on the game window to give it focus
- Only arrow keys or WASD are supported for snake movement

### High score not saving
- Check that the project directory is writable
- The `highscore.json` file will be created automatically in the game directory

## License

This project is open source and available for personal and educational use.

## Enjoy!

Have fun playing the Snake game! Challenge yourself to beat your high score across different difficulty levels!
