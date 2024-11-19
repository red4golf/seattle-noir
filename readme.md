# Seattle Noir: A Text Adventure Game

Seattle Noir is a detective text adventure game set in 1947 post-war Seattle. Players take on the role of Detective Johnny Diamond investigating a mysterious case involving missing medical supplies, smuggling operations, and the city's historic underground tunnels.

## Features

- Rich, historically accurate setting in 1947 Seattle
- Complex puzzle-solving gameplay including:
  - Morse code decoding
  - Radio frequency puzzles
  - Car surveillance challenges
  - Cipher decryption
- Multiple locations to explore including:
  - Pike Place Market
  - Pioneer Square
  - Smith Tower
  - Seattle Underground
  - Waterfront District
  - Warehouse District
- Advanced inventory system with:
  - Combinable items
  - Context-sensitive item usage
  - Detailed item descriptions
- Historic trolley system for transportation
- Auto-save functionality
- Historical facts about Seattle's post-war era
- Comprehensive save/load system with multiple save slots

## Installation

1. Clone the repository:
```bash
git clone https://github.com/red4golf/seattle-noir.git
cd seattle-noir
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Game Commands

### Basic Commands
- `look`: Examine your surroundings
- `inventory`: Check your belongings
- `help`: Display available commands
- `history`: Learn historical facts about your location
- `quit`: Exit the game

### Movement & Investigation
- `go [direction]`: Move to a new location
- `take [item]`: Pick up an item
- `examine [item]`: Look at an item closely
- `talk`: Speak to anyone present
- `solve`: Attempt to solve a puzzle in your location

### Item Interaction
- `use [item]`: Use an item in your inventory
- `combine [item1] [item2]`: Try to use two items together

### Save System
- `save [name]`: Save your game with optional name
- `load [name]`: Load a saved game
- `saves`: List available save files

### Trolley System
When on the trolley:
- `next`: Move to next stop
- `off`: Exit at current stop
- `status`: View route information
- `history`: Learn about current stop

## Game Features

### Auto-Save System
- Automatic saves every 5 minutes
- Maintains last 3 auto-saves
- Maximum save directory size of 50MB
- Manual saves preserved separately from auto-saves

### Inventory Management
- No size limit on inventory
- Detailed item descriptions with basic and detailed views
- Context-sensitive item usage based on location
- Strategic item combinations unlock new clues

### Location System
- Historically accurate depictions of 1947 Seattle
- Dynamic location descriptions
- Location-specific historical information
- Required conditions for accessing certain areas

### Puzzle System
- Multiple puzzle types:
  - Radio frequency tuning
  - Vehicle surveillance
  - Cipher decoding
  - Morse code translation
- Progressive difficulty
- Multiple solution attempts allowed
- Required items for specific puzzles

## Development

### Project Structure
```
seattle-noir/
├── game_manager.py     # Main game loop and state management
├── location_manager.py # Location and movement handling
├── item_manager.py     # Inventory and item interactions
├── puzzle_solver.py    # Puzzle mechanics and solutions
├── trolley_system.py   # Trolley transportation system
├── utils.py           # Utility functions and helpers
└── config.py          # Game configuration and constants
```

### Key Components
- **Game Manager**: Controls game flow, command processing, and state management
- **Location Manager**: Handles movement, location descriptions, and accessibility
- **Item Manager**: Manages inventory, item combinations, and usage
- **Puzzle Solver**: Implements various puzzle mechanics and validation
- **Trolley System**: Manages the historic trolley transportation
- **Utils**: Provides display, input handling, and save/load functionality

### Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

#### Development Guidelines
- Use type hints for all function parameters and returns
- Add logging for significant game events and errors
- Maintain consistent error handling patterns
- Update configuration in `config.py` rather than hardcoding values
- Follow existing naming conventions
- Add appropriate docstrings for all new functions

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments

- Inspired by classic text adventures and noir detective fiction
- Historical information sourced from Seattle Municipal Archives
- Special thanks to all contributors and testers

## Version Information

Current Version: 1.0.0
Save File Version: 1.0.0
