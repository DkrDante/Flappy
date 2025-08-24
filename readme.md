# 🐦 Enhanced Flappy Bird with AI Training

A comprehensive Flappy Bird implementation featuring both human gameplay and AI training using the NEAT (NeuroEvolution of Augmenting Topologies) algorithm.

## 🎮 Features

### Core Gameplay

- **Classic Flappy Bird mechanics** with smooth physics
- **Human playable mode** with high score tracking
- **AI training mode** using NEAT algorithm
- **Multiple difficulty levels** that scale with performance
- **Power-up system** (shields, slow motion, double points)

### AI & Machine Learning

- **NEAT algorithm implementation** for neural network evolution
- **Real-time AI training visualization**
- **Neural network analysis tools**
- **Training statistics and progress tracking**
- **Best AI model saving and loading**

### User Interface

- **Main menu system** with multiple game modes
- **Settings configuration** with persistent storage
- **Leaderboard system** with player statistics
- **AI network visualization** tools
- **Training progress graphs**

## 🚀 Getting Started

### Prerequisites

```bash
pip install pygame neat-python matplotlib numpy
```

### Installation

1. Clone the repository
2. Install dependencies
3. Run the main menu:

```bash
# Graphical Menu (Recommended)
python menu.py

# Command Line Launcher (Alternative)
python launcher.py
```

## 📁 Project Structure

```
flappy/
├── flappy_bird.py          # Main AI training game
├── human_mode.py           # Human playable version
├── menu.py                 # Graphical main menu system
├── launcher.py             # Command-line launcher
├── settings.py             # Settings configuration
├── leaderboard.py          # Leaderboard system
├── ai_analyzer.py          # AI analysis tools
├── visualize.py            # NEAT visualization
├── config-feedforward.txt  # NEAT configuration
├── best.pickle            # Best trained AI model
├── imgs/                  # Game assets
└── README.md              # This file
```

## 🎯 Game Modes

### 1. Human Mode (`human_mode.py`)

- Classic Flappy Bird gameplay
- High score tracking
- Restart functionality
- Space bar to jump

### 2. AI Training Mode (`flappy_bird.py`)

- NEAT algorithm training
- Population evolution
- Fitness tracking
- Automatic model saving

### 3. AI Analyzer (`ai_analyzer.py`)

- Analyze trained AI networks
- Visualize neural network structure
- View training statistics
- Performance analysis

### 4. Leaderboard (`leaderboard.py`)

- View high scores and statistics
- Filter by game mode
- Player performance tracking
- Persistent score storage

### 5. Settings (`settings.py`)

- Configure game options
- Adjust AI parameters
- Customize difficulty levels
- Persistent settings storage

## ⚙️ Settings

### Game Settings

- **Difficulty**: Easy, Normal, Hard
- **Sound**: On/Off toggle
- **Music Volume**: 0.3 - 0.9
- **AI Population Size**: 50 - 200
- **AI Speed**: 5 - 20
- **Show Lines**: Visualize AI decision making
- **Auto Save**: Automatic progress saving

### Controls

#### Menu Navigation

- **Arrow Keys**: Navigate menu options
- **Number Keys (1-6)**: Quick selection
- **Enter/Space**: Confirm selection
- **ESC**: Exit/Back

#### Game Controls

- **Space**: Jump (in game)
- **ESC**: Exit game

## 🤖 AI Training

### NEAT Configuration

The AI uses a feedforward neural network with:

- **2 Input nodes**: Bird Y position, Distance to pipe
- **1 Output node**: Jump decision
- **Population size**: Configurable (default: 100)
- **Fitness function**: Distance traveled + pipes passed

### Training Process

1. Initialize random population
2. Evaluate fitness for each bird
3. Select best performers
4. Crossover and mutate
5. Repeat for specified generations

### Visualization

- Real-time training progress
- Neural network structure display
- Fitness evolution graphs
- Species diversity tracking

## 📊 Leaderboard System

### Features

- **Top 10 scores** tracking
- **Mode filtering** (Human/AI/All)
- **Player statistics**
- **Date and time stamps**
- **Persistent storage**

### Score Categories

- **Human Mode**: Manual gameplay scores
- **AI Mode**: Best AI performance scores
- **All**: Combined leaderboard

## 🔧 Customization

### Adding New Features

1. **Power-ups**: Modify `enhanced_game.py`
2. **Difficulty levels**: Adjust pipe generation in `Pipe` class
3. **AI inputs**: Modify input nodes in NEAT config
4. **Visual effects**: Add to drawing functions

### Configuration Files

- `config-feedforward.txt`: NEAT algorithm parameters
- `game_settings.json`: User preferences
- `leaderboard.json`: Score data
- `best.pickle`: Trained AI model

## 📈 Performance Tips

### For AI Training

- Start with smaller population (50-100)
- Use moderate mutation rates
- Monitor fitness stagnation
- Save best models regularly

### For Human Play

- Practice timing and rhythm
- Learn pipe patterns
- Use power-ups strategically
- Focus on consistency

## 🐛 Troubleshooting

### Common Issues

1. **Missing images**: Ensure `imgs/` folder contains all assets
2. **NEAT import error**: Install `neat-python` package
3. **Performance issues**: Reduce AI population size
4. **Save file errors**: Check file permissions

### Debug Mode

Enable debug features by modifying:

- `DRAW_LINES = True` in `flappy_bird.py`
- Increase AI speed for faster training
- Add console logging for detailed output

## 🤝 Contributing

### Adding Features

1. Fork the repository
2. Create feature branch
3. Implement changes
4. Test thoroughly
5. Submit pull request

### Suggested Enhancements

- **Sound effects and music**
- **More power-up types**
- **Multiplayer mode**
- **Advanced AI algorithms**
- **Mobile support**
- **Level editor**

## 📝 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Original Flappy Bird game concept
- NEAT algorithm by Kenneth Stanley
- Pygame community
- Open source contributors

---

**Happy Flapping! 🐦✨**
