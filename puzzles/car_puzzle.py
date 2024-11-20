from typing import Dict, List, Optional, Set
import random
from .base_puzzle import BasePuzzle

class CarPuzzle(BasePuzzle):
    """Car tracking puzzle implementation."""

    def __init__(self):
        super().__init__()
        
        # Possible car movement patterns
        self.PATTERNS = {
            "NSEW": "around the block clockwise",
            "NWSE": "through back alleys",
            "SENW": "counter-clockwise route",
            "SWNE": "zigzag pattern"
        }
        
        # Track current game state
        self.current_pattern: Optional[str] = None
        self.attempts: int = 0
        self.max_attempts: int = 5
        self.pattern_description: Optional[str] = None

    @property
    def requirements(self) -> List[str]:
        return ["binoculars"]

    def _generate_pattern(self) -> None:
        """Generate a new movement pattern and description."""
        self.current_pattern = random.choice(list(self.PATTERNS.keys()))
        self.pattern_description = self.PATTERNS[self.current_pattern]
        self.logger.info(f"Generated pattern: {self.current_pattern}")

    def _validate_direction_input(self, input_str: str) -> bool:
        """Validate that input contains only valid directions."""
        return all(char in "NSEW" for char in input_str.upper())

    def solve(self, inventory: List[str], game_state: Dict) -> bool:
        """Implement the car tracking puzzle."""
        try:
            self.logger.info("Starting car tracking puzzle")
            
            # Check if already solved
            if game_state.get("tracked_car", False):
                print("\nYou've already tracked the car's route successfully.")
                print("However, you could observe for more suspicious activity.")
            
            # Generate new pattern
            self._generate_pattern()
            
            print("\nFrom this height, you can see vehicles moving through the streets below.")
            print("Your notes mention a blue sedan making regular deliveries.")
            print("\nYou spot the blue sedan! Quick, track its movements!")
            print("The car appears to be following a specific pattern.")
            print("\nDirections:")
            print("- Use N (North), S (South), E (East), W (West)")
            print("- Enter the full pattern you observe")
            print("- Example: If the car goes North, then East, enter: NE")
            
            attempts = 0
            while attempts < self.max_attempts:
                try:
                    command = input("\nEnter movement pattern (or 'hint'/'quit'): ").upper()
                    
                    if command == 'QUIT':
                        return False
                        
                    if command == 'HINT':
                        self._provide_hint(attempts)
                        continue
                    
                    if not self._validate_direction_input(command):
                        print("\nPlease use only N, S, E, or W to describe the pattern.")
                        continue
                    
                    # Check pattern
                    if command == self.current_pattern:
                        print(f"\nSuccess! You've tracked the car {self.pattern_description}!")
                        print("This route seems deliberately planned to avoid main streets.")
                        game_state["tracked_car"] = True
                        return True
                    
                    # Wrong pattern
                    attempts += 1
                    remaining = self.max_attempts - attempts
                    print(f"\nYou lost sight of the vehicle. {remaining} attempts remaining.")
                    
                    # Provide feedback on length
                    if len(command) != len(self.current_pattern):
                        print(f"The pattern seems to be {len(self.current_pattern)} moves long.")
                    
                except ValueError as e:
                    self.logger.error(f"Invalid input: {e}")
                    print("\nPlease enter a valid pattern using N, S, E, W.")
            
            print("\nThe car has disappeared into traffic. Try again later.")
            return False
            
        except Exception as e:
            self.logger.error(f"Error in car tracking puzzle: {e}")
            print("Something went wrong with the observation. Try again later.")
            return False

    def _provide_hint(self, attempt_number: int) -> None:
        """Provide progressive hints based on number of attempts."""
        if attempt_number == 0:
            print("\nHint: The pattern contains four movements.")
        elif attempt_number == 1:
            print("\nHint: Watch for repeated directions.")
        elif attempt_number == 2:
            first_move = self.current_pattern[0]
            print(f"\nHint: The car starts by going {first_move}...")
        else:
            print("\nHint: The car seems to be making a complete circuit.")

    def get_state(self) -> Dict:
        """Get current puzzle state."""
        return {
            "attempts": self.attempts,
            "current_pattern": self.current_pattern,
            "pattern_description": self.pattern_description
        }

    def restore_state(self, state: Dict) -> None:
        """Restore puzzle state."""
        self.attempts = state.get("attempts", 0)
        self.current_pattern = state.get("current_pattern")
        self.pattern_description = state.get("pattern_description")

    def get_debug_info(self) -> Dict:
        """Get debug information about current puzzle state."""
        return {
            "current_pattern": self.current_pattern,
            "description": self.pattern_description,
            "attempts": self.attempts,
            "max_attempts": self.max_attempts
        }