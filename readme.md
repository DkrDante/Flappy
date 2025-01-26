# Flappy Bird AI using NEAT

This project is an implementation of the Flappy Bird game integrated with a neural network using the NEAT (NeuroEvolution of Augmenting Topologies) algorithm. The AI learns to play Flappy Bird by evolving its strategies over generations.

## Features

- Flappy Bird gameplay.
- AI-controlled birds using NEAT.
- Dynamic pipe generation.
- High-score tracking.
- Visualization of AI learning progress.

## Prerequisites

Ensure you have the following installed:

- Python 3.7 or higher
- pip (Python package manager)

## Installation Guide

Follow these steps to set up and run the project:

### 1. Clone the Repository

```bash
git clone https://github.com/DkrDante/Flappy
cd flappy
```

### 2. Add Game Assets

Ensure the following image files are in the `imgs` directory:

- `pipe.png`
- `bg.png`
- `bird1.png`, `bird2.png`, `bird3.png`
- `base.png`

### 3. Configure NEAT

Ensure the `config-feedforward.txt` file is present in the project directory. This file contains the NEAT configuration for the neural network.

### 4. Run the Game

To start the game, execute:

```bash
python flappy_bird.py
```

## How it Works

1. **Initialization**: The AI birds are initialized with random weights and biases.
2. **Fitness Evaluation**: Each bird's performance is evaluated based on its ability to pass through pipes.
3. **Evolution**: NEAT evolves the neural networks by applying mutations and crossover to improve performance over generations.
4. **Game Loop**: The game loop updates the birds' positions, checks for collisions, and renders the graphics.

## Key Files

- `flappy_bird.py`: Main game logic and AI integration.
- `config-feedforward.txt`: Configuration for the NEAT algorithm.
- `imgs/`: Directory containing game assets.
- `requirements.txt`: List of Python dependencies.

## Controls

- The AI controls the birds automatically.
- Use `ESC` or close the window to quit the game.

## Notes

- Modify the NEAT configuration file (`config-feedforward.txt`) to tweak the neural network parameters.
- The game will save the best-performing neural network to a file named `best.pickle` if the score exceeds 20.

## Dependencies

The project uses the following Python libraries:

- `pygame`: For game development.
- `neat-python`: For implementing the NEAT algorithm.
- `pickle`: For saving and loading the best-performing neural network.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgments

- Inspired by the Flappy Bird game.
- Uses the NEAT algorithm for AI evolution.

---

Enjoy the game and watch the AI learn to master Flappy Bird!
