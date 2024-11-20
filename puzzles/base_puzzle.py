from abc import ABC, abstractmethod
from typing import Dict, List, Optional
import logging

class BasePuzzle(ABC):
    """Abstract base class for all puzzles."""
    
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def solve(self, inventory: List[str], game_state: Dict) -> bool:
        """
        Attempt to solve the puzzle.
        
        Args:
            inventory: List of items the player has
            game_state: Current game state dictionary
            
        Returns:
            bool: True if puzzle was solved, False otherwise
        """
        pass
    
    @abstractmethod
    def get_state(self) -> Dict:
        """
        Get current puzzle state for saving.
        
        Returns:
            Dict: Current puzzle state
        """
        pass
    
    @abstractmethod
    def restore_state(self, state: Dict) -> None:
        """
        Restore puzzle state from saved game.
        
        Args:
            state: Dictionary containing puzzle state
        """
        pass
    
    @property
    @abstractmethod
    def requirements(self) -> List[str]:
        """Required items for this puzzle."""
        pass

    def validate_input(self, user_input: str, valid_chars: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ") -> bool:
        """
        Validate user input.
        
        Args:
            user_input: String to validate
            valid_chars: String of valid characters
            
        Returns:
            bool: True if input is valid
        """
        return all(char in valid_chars for char in user_input.upper())