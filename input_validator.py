from typing import Set, Dict, Optional, Any
import logging

class InputValidator:
    """Centralized input validation functionality."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    @staticmethod
    def validate_puzzle_input(input_str: str, 
                            valid_chars: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
                            min_length: int = 1,
                            max_length: int = 50) -> bool:
        """
        Validate input string for puzzles.
        
        Args:
            input_str: Input to validate
            valid_chars: String of allowed characters
            min_length: Minimum input length
            max_length: Maximum input length
            
        Returns:
            bool: True if input is valid
        """
        if not input_str:
            return False
            
        if not min_length <= len(input_str) <= max_length:
            return False
            
        return all(char in valid_chars for char in input_str.upper())
    
    @staticmethod
    def validate_direction(direction: str, valid_directions: Set[str]) -> bool:
        """
        Validate movement direction.
        
        Args:
            direction: Direction to validate
            valid_directions: Set of valid directions
            
        Returns:
            bool: True if direction is valid
        """
        return direction.lower().strip() in {d.lower() for d in valid_directions}
    
    @staticmethod
    def validate_command(command: str, valid_commands: Set[str]) -> bool:
        """
        Validate game command.
        
        Args:
            command: Command to validate
            valid_commands: Set of valid commands
            
        Returns:
            bool: True if command is valid
        """
        return command.lower().strip() in valid_commands
    
    @staticmethod
    def validate_item_name(item: str, max_length: int = 50) -> bool:
        """
        Validate item name.
        
        Args:
            item: Item name to validate
            max_length: Maximum allowed length
            
        Returns:
            bool: True if item name is valid
        """
        if not item or not isinstance(item, str):
            return False
            
        if len(item) > max_length:
            return False
            
        return item.replace('_', '').isalnum()