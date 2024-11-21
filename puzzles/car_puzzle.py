from typing import Dict, List, Optional, Set
import random
from .base_puzzle import BasePuzzle
from utils import print_text
from input_validator import InputValidator

class CarPuzzle(BasePuzzle):
    """
    Car tracking puzzle implementation. Players must identify the pattern
    of a suspicious vehicle's movements through the city.
    """

    def __init__(self):
        # Initialize base puzzle features (attempts, logging, etc.)
        super().__init__()
        
        # Define possible movement patterns with their descriptions
        self.PATTERNS = {
            "NSEW": "around the block clockwise",
            "NWSE": "through back alleys",
            "SENW": "counter-clockwise route",
            "SWNE": "zigzag pattern"
        }
        
        # Puzzle state variables - using Optional for clarity on nullable fields
        self.current_pattern: Optional[str] = None
        self.pattern_description: Optional[str] = None
        
        # Override base puzzle settings if needed
        self.max_attempts = 5  # Customize max attempts for this specific puzzle

    @property
    def requirements(self) -> List[str]:
        """Required items list - inherited from BasePuzzle."""
        return ["binoculars"]

    def _generate_pattern(self) -> None:
        """
        Generate a new movement pattern and description.
        Uses random.choice for pattern selection.
        """
        with self.error_handler("pattern generation"):
            self.current_pattern = random.choice(list(self.PATTERNS.keys()))
            self.pattern_description = self.PATTERNS[self.current_pattern]
            self.logger.info(f"Generated pattern: {self.current_pattern}")

    def _validate_direction_input(self, input_str: str) -> bool:
        """
        Validate user input for movement directions.
        Now uses InputValidator for consistent validation across puzzles.
        """
        return InputValidator.validate_puzzle_input(
            input_str, 
            valid_chars="NSEW",
            min_length=4,
            max_length=4
        )
    
    def _provide_hint(self, attempt_number: int) -> None:
        """
        Provide progressive hints based on number of attempts.
        Hints become more specific as attempts increase.
        """
        if attempt_number == 0:
            print_text("\nHint: The pattern contains four movements.")
        elif attempt_number == 1:
            print_text("\nHint: Watch for repeated directions.")
        elif attempt_number == 2:
            first_move = self.current_pattern[0]
            print_text(f"\nHint: The car starts by going {first_move}...")
        else:
            print_text("\nHint: The car seems to be making a complete circuit.")

    def _display_puzzle_introduction(self) -> None:
        """
        Display the initial puzzle description and instructions.
        Separated from solve() for better code organization.
        """
        intro_text = """
        From this height, you can see vehicles moving through the streets below.
        Your notes mention a blue sedan making regular deliveries.

        You spot the blue sedan! Quick, track its movements!
        The car appears to be following a specific pattern.

        Directions:
        - Use N (North), S (South), E (East), W (West)
        - Enter the full pattern you observe
        - Example: If the car goes North, then East, enter: NE
        """
        print_text(intro_text)

    def solve(self, inventory: List[str], game_state: Dict) -> bool:
        """
        Main puzzle solving logic. Implements the abstract method from BasePuzzle.
        Uses error handling and input validation.
        """
        # Use error handler from BasePuzzle
        with self.error_handler("car tracking puzzle"):
            # Check if already solved
            if game_state.get("tracked_car", False):
                print_text("\nYou've already tracked the car's route successfully.")
                print_text("However, you could observe for more suspicious activity.")
                return True

            # Check requirements using BasePuzzle property
            if "binoculars" not in inventory:
                print_text("\nYou'll need binoculars to track the vehicle effectively.")
                return False

            # Generate new pattern and display introduction
            self._generate_pattern()
            self._display_puzzle_introduction()

            # Main puzzle loop
            while self.attempts < self.max_attempts:
                try:
                    command = input("\nEnter movement pattern (or 'hint'/'quit'): ").upper()

                    if command == 'QUIT':
                        return False

                    if command == 'HINT':
                        self._provide_hint(self.attempts)
                        continue

                    # Validate input using our enhanced validation
                    if not self._validate_direction_input(command):
                        print_text("\nPlease use only N, S, E, or W to describe the pattern.")
                        continue

                    # Check solution
                    if command == self.current_pattern:
                        return self._handle_correct_solution(game_state)

                    # Handle incorrect answer using BasePuzzle method
                    if not self.increment_attempts():
                        return False

                    # Provide feedback on pattern length
                    if len(command) != len(self.current_pattern):
                        print_text(f"\nThe pattern seems to be {len(self.current_pattern)} moves long.")

                except KeyboardInterrupt:
                    print_text("\nPuzzle attempt interrupted.")
                    return False

            print_text("\nThe car has disappeared into traffic. Try again later.")
            return False

    def _handle_correct_solution(self, game_state: Dict) -> bool:
        """
        Handle correct puzzle solution and update game state.
        Separated from solve() for better organization.
        """
        print_text(f"\nSuccess! You've tracked the car {self.pattern_description}!")
        print_text("This route seems deliberately planned to avoid main streets.")
        game_state["tracked_car"] = True
        return True

    def get_state(self) -> Dict:
        """
        Get current puzzle state for saving.
        Extends base state from BasePuzzle.
        """
        state = super().get_state()  # Get base state
        state.update({
            "current_pattern": self.current_pattern,
            "pattern_description": self.pattern_description
        })
        return state

    def restore_state(self, state: Dict) -> None:
        """
        Restore puzzle state from saved game.
        Extends base state restoration from BasePuzzle.
        """
        super().restore_state(state)  # Restore base state
        self.current_pattern = state.get("current_pattern")
        self.pattern_description = state.get("pattern_description")

    def get_debug_info(self) -> Dict:
        """
        Get debug information about current puzzle state.
        Useful for testing and debugging.
        """
        return {
            "current_pattern": self.current_pattern,
            "description": self.pattern_description,
            "attempts": self.attempts,
            "max_attempts": self.max_attempts
        }