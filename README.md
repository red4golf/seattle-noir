# Seattle Noir: The Case of the Missing Shipment

A text-based detective adventure game set in 1947 Seattle, combining historical fiction with noir mystery elements.

## Description

Seattle Noir is an interactive fiction game where players take on the role of Detective Sarah/Sam Harper investigating a mysterious case in post-World War II Seattle. The game features:

- Historical accuracy with detailed depictions of 1947 Seattle locations
- Multiple puzzles to solve, including cipher codes and morse code challenges
- An intricate mystery involving smuggling operations
- Educational historical notes about Seattle's post-war period
- Classic text adventure gameplay mechanics

## Installation

1. Ensure you have Python 3.7+ installed on your system

2. Clone this repository:

```bash
git clone https://github.com/red4golf/seattle-noir.git
cd seattle-noir
```

3. Create a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

4. Install required packages:

```bash
pip install -r requirements.txt
```

## Usage

To start the game, run:

```bash
python game.py
```

### Commands

- `look`: Examine your surroundings
- `inventory`: Check your belongings
- `take [item]`: Pick up an item
- `go [direction]`: Move to a new location
- `examine [item]`: Look at an item closely
- `talk`: Speak to anyone present
- `use [item]`: Use an item in your inventory
- `history`: Learn historical facts about your location
- `solve`: Attempt to solve a puzzle in your location
- `help`: Show all available commands
- `quit`: Exit the game

## Game Structure

The game is organized around several key locations in historic Seattle:

- Police Station
- Pike Place Market
- Pioneer Square
- Smith Tower
- Underground tunnels
- Waterfront district

Each location contains historical details, items to collect, and potential clues to solve the mystery.

## Development

The game is built using Python's standard library and follows object-oriented programming principles. Key components include:

- `SeattleNoir` class: Main game engine
- Location-based navigation system
- Inventory management
- Puzzle mechanics
- Historical fact integration

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](LICENSE)

## Credits

- Game Design & Development: [Your Name]
- Historical Research: [Your Name]
- Testing: [Your Name]

## Project Status

This project is currently in active development. Future planned features include:

- Additional historical locations
- More complex puzzles
- Character interaction system
- Save game functionality
