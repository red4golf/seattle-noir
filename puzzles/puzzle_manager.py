from typing import Dict, List, Optional
import logging
from contextlib import contextmanager
from utils import print_text
from .cipher_puzzle import CipherPuzzle
from .radio_puzzle import RadioPuzzle
from .morse_puzzle import MorsePuzzle

class PuzzleManager:
    """Enhanced puzzle manager with improved error handling and state management."""
    
    def __init__(self):
        """Initialize puzzle instances and state tracking."""
        self.logger = logging.getLogger(__name__)
        
        # Initialize all puzzle instances
        self.puzzles = {
            "cipher_puzzle": CipherPuzzle(),
            "radio_puzzle": RadioPuzzle(),
            "morse_puzzle": MorsePuzzle()
        }

        # Map locations to their corresponding puzzles
        self.puzzle_map = {
            "evidence_room": "cipher_puzzle",
            "warehouse_office": "radio_puzzle",
            "underground_tunnels": "morse_puzzle"
        }
        
        # State management
        self._last_state = {}

    @contextmanager
    def error_handler(self, operation: str):
        """Context manager for standardized error handling."""
        try:
            yield
        except Exception as e:
            self.logger.error(f"Error in puzzle manager {operation}: {e}")
            print_text(f"\nThere was a problem with {operation}. Progress has been saved.")
            # Restore last known good state
            self._restore_last_state()

    def _backup_state(self, puzzle_name: str) -> None:
        """
        Backup the current state of a puzzle.
        
        Args:
            puzzle_name: Name of the puzzle to backup
        """
        if puzzle_name in self.puzzles:
            self._last_state[puzzle_name] = self.puzzles[puzzle_name].get_state()
            self.logger.debug(f"Backed up state for {puzzle_name}")

    def _restore_last_state(self) -> None:
        """Restore all puzzles to their last known good state."""
        for puzzle_name, state in self._last_state.items():
            if puzzle_name in self.puzzles:
                self.puzzles[puzzle_name].restore_state(state)
                self.logger.debug(f"Restored state for {puzzle_name}")

    def handle_puzzle(self, location: str, inventory: List[str], game_state: Dict) -> bool:
        """
        Handle puzzle attempt for a given location.
        
        Args:
            location: Current game location
            inventory: Player's inventory
            game_state: Current game state
            
        Returns:
            bool: True if puzzle was solved, False otherwise
        """
        with self.error_handler("puzzle handling"):
            # Check if location has a puzzle
            if location not in self.puzzle_map:
                print_text("There's no puzzle here.")
                return False
                
            puzzle_name = self.puzzle_map[location]
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
                    items_str = ", ".join(missing_items)
                    print_text(f"\nYou need: {items_str}")
                    return False
                    
                # Attempt to solve puzzle
                result = puzzle.solve(inventory, game_state)
                
                # If puzzle was solved, update any related game state
                if result:
                    self._handle_puzzle_completion(puzzle_name, game_state)
                
                return result
                
            except KeyboardInterrupt:
                print_text("\nPuzzle interrupted. Progress saved.")
                self._restore_last_state()
                return False
                
            except Exception as e:
                self.logger.error(f"Error in puzzle {puzzle_name}: {e}")
                print_text("\nPuzzle error occurred. Progress saved.")
                self._restore_last_state()
                return False

    def _handle_puzzle_completion(self, puzzle_name: str, game_state: Dict) -> None:
        """
        Handle any additional game state updates when a puzzle is completed.
        
        Args:
            puzzle_name: Name of the completed puzzle
            game_state: Current game state to update
        """
        completion_handlers = {
            "cipher_puzzle": lambda: game_state.update({"cipher_mastery": True}),
            "radio_puzzle": lambda: game_state.update({"radio_expert": True}),
            "morse_puzzle": lambda: game_state.update({"morse_proficiency": True})
        }
        
        handler = completion_handlers.get(puzzle_name)
        if handler:
            handler()
            self.logger.info(f"Updated game state for {puzzle_name} completion")

    def get_all_states(self) -> Dict:
        """
        Get states of all puzzles for saving.
        
        Returns:
            Dict containing all puzzle states
        """
        return {name: puzzle.get_state() 
                for name, puzzle in self.puzzles.items()}
    
    def restore_all_states(self, states: Dict) -> None:
        """
        Restore all puzzle states.
        
        Args:
            states: Dictionary of puzzle states to restore
        """
        for name, state in states.items():
            if name in self.puzzles:
                self.puzzles[name].restore_state(state)
                self.logger.debug(f"Restored state for {name}")

    def get_available_puzzles(self, location: str) -> List[str]:
        """
        Get list of available puzzles at current location.
        
        Args:
            location: Current game location
            
        Returns:
            List of available puzzle names
        """
        return [self.puzzle_map[location]] if location in self.puzzle_map else []

    def get_puzzle_requirements(self, location: str) -> List[str]:
        """
        Get required items for puzzles at current location.
        
        Args:
            location: Current game location
            
        Returns:
            List of required item names
        """
        if location in self.puzzle_map:
            puzzle_name = self.puzzle_map[location]
            if puzzle_name in self.puzzles:
                return self.puzzles[puzzle_name].requirements
        return []

    def get_debug_info(self) -> Dict:
        """
        Get debug information about all puzzles.
        
        Returns:
            Dict containing debug info for all puzzles
        """
        return {
            name: puzzle.get_debug_info() 
            for name, puzzle in self.puzzles.items()
            if hasattr(puzzle, 'get_debug_info')
        }