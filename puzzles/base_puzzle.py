from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
import logging
from contextlib import contextmanager

class BasePuzzle(ABC):
    """Abstract base class for all puzzles."""
    
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.attempts = 0
        self.max_attempts = 5  # Default value, can be overridden
        self.solved = False

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
            Dict containing the puzzle's current state
        """
        return {
            "attempts": self.attempts,
            "max_attempts": self.max_attempts,
            "solved": self.solved,
            # Add any additional common state here
        }
    
    @abstractmethod
    def restore_state(self, state: Dict) -> None:
        """
        Restore puzzle state from saved game.
        
        Args:
            state: Dictionary containing puzzle state
        """
        self.attempts = state.get("attempts", 0)
        self.max_attempts = state.get("max_attempts", 5)
        self.solved = state.get("solved", False)
    
    @property
    @abstractmethod
    def requirements(self) -> List[str]:
        """Required items for this puzzle."""
        pass
    
    def validate_input(self, user_input: str, 
                      valid_chars: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ") -> bool:
        """
        Validate user input.
        
        Args:
            user_input: String to validate
            valid_chars: String of valid characters
            
        Returns:
            bool: True if input is valid
        """
        if not user_input:
            return False
        return all(char in valid_chars for char in user_input.upper())
    @contextmanager
    def error_handler(self, operation: str):
        """
        Context manager for standardized error handling.
        
        Args:
            operation: Name of the operation being performed
            
        Yields:
            None
        """
        try:
            yield
        except Exception as e:
            self.logger.error(f"Error in {operation}: {e}")
            print(f"\nThere was a problem with {operation}. Please try again.")
    
    def increment_attempts(self) -> bool:
        """
        Increment attempt counter and check if max attempts reached.
        
        Returns:
            bool: True if more attempts available, False if max reached
        """
        self.attempts += 1
        remaining = self.max_attempts - self.attempts
        
        if remaining <= 0:
            print("\nYou've run out of attempts. Try again later.")
            return False
            
        print(f"\n{remaining} attempts remaining.")
        return True
    
    def reset_attempts(self) -> None:
        """Reset attempt counter."""
        self.attempts = 0