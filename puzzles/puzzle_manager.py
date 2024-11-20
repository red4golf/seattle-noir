from typing import Dict, List, Optional
import logging
from .cipher_puzzle import CipherPuzzle
from .radio_puzzle import RadioPuzzle
from .car_puzzle import CarPuzzle
from .morse_puzzle import MorsePuzzle
# We'll add other puzzle imports as we migrate them

class PuzzleManager:
    """Manages all puzzle instances and interactions."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.puzzles = {
            "cipher_puzzle": CipherPuzzle(),
            "radio_puzzle": RadioPuzzle(),
            "car_puzzle": CarPuzzle(),
            "morse_puzzle": MorsePuzzle()
        }
        self._last_state = {}

    def _backup_state(self, puzzle_name: str) -> None:
        """Backup the current state of a puzzle."""
        if puzzle_name in self.puzzles:
            self._last_state[puzzle_name] = self.puzzles[puzzle_name].get_state()

    def _restore_state(self, puzzle_name: str) -> None:
        """Restore puzzle state from backup."""
        if puzzle_name in self._last_state:
            self.puzzles[puzzle_name].restore_state(self._last_state[puzzle_name])

    def handle_puzzle(self, location: str, inventory: List[str], game_state: Dict) -> bool:
        """Handle puzzle attempt for a given location."""
        try:
            puzzle_map = {
                "evidence_room": "cipher_puzzle",
                "warehouse_office": "radio_puzzle",
                "smith_tower": "car_puzzle",
                "underground_tunnels": "morse_puzzle"
            }
            
            if location not in puzzle_map:
                print("There's no puzzle here.")
                return False
                
            puzzle_name = puzzle_map[location]
            if puzzle_name not in self.puzzles:
                self.logger.error(f"No handler for puzzle: {puzzle_name}")
                return False
            
            puzzle = self.puzzles[puzzle_name]
            
            # Backup current state
            self._backup_state(puzzle_name)
            
            try:
                # Check requirements
                missing_items = [item for item in puzzle.requirements 
                               if item not in inventory]
                if missing_items:
                    print(f"You need: {', '.join(missing_items)}")
                    return False
                    
                return puzzle.solve(inventory, game_state)
                
            except KeyboardInterrupt:
                print("\nPuzzle interrupted. Progress saved.")
                self._restore_state(puzzle_name)
                return False
                
            except Exception as e:
                self.logger.error(f"Error in puzzle {puzzle_name}: {e}")
                print("\nPuzzle error occurred. Progress saved.")
                self._restore_state(puzzle_name)
                return False
                
        except Exception as e:
            self.logger.error(f"Error handling puzzle: {e}")
            print("There was a problem with the puzzle.")
            return False

    def get_all_states(self) -> Dict:
        """Get states of all puzzles for saving."""
        return {name: puzzle.get_state() 
                for name, puzzle in self.puzzles.items()}
    
    def restore_all_states(self, states: Dict) -> None:
        """Restore all puzzle states."""
        for name, state in states.items():
            if name in self.puzzles:
                self.puzzles[name].restore_state(state)