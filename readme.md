# Seattle Noir: A Text Adventure Game

Seattle Noir is a detective text adventure game set in 1947 post-war Seattle. Players take on the role of Detective Johnny Diamond investigating a mysterious case involving missing medical supplies, smuggling operations, and the city's historic underground tunnels.

## Features

- Rich, historically accurate setting in 1947 Seattle
- Complex puzzle-solving gameplay
- Multiple locations to explore including:
  - Pike Place Market
  - Pioneer Square
  - Smith Tower
  - Seattle Underground
  - Waterfront District
- Inventory system with combinable items
- Historical facts about Seattle's post-war era
- Morse code and cipher puzzles
- Branching dialogue system

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/seattle-noir.git
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

## Usage

Run the game:
```bash
python game_manager.py
```

Basic commands:
- `look`: Examine your surroundings
- `inventory`: Check your belongings
- `take [item]`: Pick up an item
- `go [direction]`: Move to a new location
- `examine [item]`: Look at an item closely
- `talk`: Speak to anyone present
- `use [item]`: Use an item in your inventory
- `combine [item1] [item2]`: Try to use two items together
- `history`: Learn historical facts about your location
- `solve`: Attempt to solve a puzzle in your location
- `help`: Show all available commands
- `quit`: Exit the game

## Development

The game is structured into several key components:
- `game_manager.py`: Main game loop and state management
- `location_manager.py`: Handles game locations and movement
- `item_manager.py`: Manages inventory and item interactions
- `puzzle_solver.py`: Handles various puzzle mechanics
- `utils.py`: Utility functions and helper classes

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments

- Inspired by classic text adventures and noir detective fiction
- Historical information sourced from Seattle Municipal Archives
- Special thanks to all contributors and testers
