# Infinite Tetris

A minimalist Tetris clone built with [Pygame](https://www.pygame.org/). The goal of this project is to provide a simple, endlessly playable version of Tetris that you can hack on and extend.

## Features

- Classic tetromino shapes and board logic
- Smooth keyboard controls with autorepeat
- Endless gameplay – new pieces spawn indefinitely

## Requirements

- Python 3.10+
- Pygame (and other packages listed in `requirements.txt`)

## Installation

```bash
# (optional) create a virtual environment
python -m venv .venv
source .venv/bin/activate

# install dependencies
pip install -r requirements.txt
```

## Running the Game

```bash
python main.py
```

### Controls

- **Left / Right Arrow** – move piece horizontally
- **Down Arrow** – move piece down
- **Up Arrow** – rotate piece clockwise

## Screenshots

<!-- Replace these placeholders with your own images -->

![Gameplay Screenshot](docs/images/gameplay.png)

![Another Angle](docs/images/second-shot.png)

## Development Notes

A brain-rot version of Tetris that does not speed up. Made quickly so that I can play Tetris casually.
The code in `main.py` is intentionally compact and designed for learning and experimentation. Feel free to fork the project and add your own twists.

