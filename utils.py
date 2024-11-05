import os
import sys
import time
import logging
from typing import Tuple, Optional, Dict, Any, List

# Configure logging
logging.basicConfig(
    filename='seattlenoir.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class DisplayManager:
    @staticmethod
    def print_slowly(text: str, delay: float = 0.03) -> None:
        """
        Print text character by character with proper error handling.
        
        Args:
            text (str): The text to print
            delay (float): Delay between characters in seconds
        """
        try:
            for char in text:
                sys.stdout.write(char)
                sys.stdout.flush()
                time.sleep(delay)
        except KeyboardInterrupt:
            print("\nOutput interrupted.")
            logging.info("Text display interrupted by user")
        except Exception as e:
            print(f"\nError displaying text: {e}")
            logging.error(f"Error in print_slowly: {e}")
        finally:
            print()

    @staticmethod
    def clear_screen() -> None:
        """Clear the terminal screen with error handling."""
        try:
            os.system('cls' if os.name == 'nt' else 'clear')
        except Exception as e:
            print("\n" * 100)
            logging.warning(f"Could not clear screen: {e}")

    @staticmethod
    def format_location_description(description: str, exits: List[str], items: List[str]) -> str:
        """
        Format a location description with exits and items.
        
        Args:
            description (str): Base location description
            exits (List[str]): Available exits
            items (List[str]): Items in the location
            
        Returns:
            str: Formatted description
        """
        formatted = description.strip()
        
        if exits:
            formatted += f"\n\nExits: {', '.join(exits)}"
            
        if items:
            formatted += f"\n\nYou can see: {', '.join(items)}"
            
        return formatted

class InputValidator:
    # Valid commands that don't require arguments
    BASIC_COMMANDS = {'quit', 'help', 'look', 'inventory', 'talk', 'history', 'solve'}
    
    # Commands that require arguments
    COMPLEX_COMMANDS = {'take', 'go', 'examine', 'use'}

    @staticmethod
    def validate_command(command: str) -> Tuple[bool, str, str]:
        """
        Validate and parse user input.
        
        Args:
            command (str): Raw user input
            
        Returns:
            Tuple[bool, str, str]: (is_valid, command_type, command_argument)
        """
        if not command or not isinstance(command, str):
            return False, "", ""
            
        command = command.lower().strip()
        
        # Handle basic commands
        if command in InputValidator.BASIC_COMMANDS:
            return True, command, ""
        
        # Handle complex commands
        parts = command.split(maxsplit=1)
        if len(parts) != 2 or parts[0] not in InputValidator.COMPLEX_COMMANDS:
            return False, "", ""
            
        return True, parts[0], parts[1]

    @staticmethod
    def validate_item_name(item: str) -> bool:
        """
        Validate an item name.
        
        Args:
            item (str): Item name to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        return bool(item and isinstance(item, str) and len(item) <= 50)

    @staticmethod
    def validate_direction(direction: str, valid_exits: List[str]) -> bool:
        """
        Validate a movement direction.
        
        Args:
            direction (str): Direction to validate
            valid_exits (List[str]): List of valid exits
            
        Returns:
            bool: True if valid, False otherwise
        """
        return direction in valid_exits

class GameState:
    @staticmethod
    def save_game_state(state: Dict[str, Any], filename: str = 'savegame.json') -> bool:
        """
        Save game state to a file.
        
        Args:
            state (Dict[str, Any]): Game state to save
            filename (str): File to save to
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            import json
            with open(filename, 'w') as f:
                json.dump(state, f)
            logging.info(f"Game state saved to {filename}")
            return True
        except Exception as e:
            logging.error(f"Error saving game state: {e}")
            return False

    @staticmethod
    def load_game_state(filename: str = 'savegame.json') -> Optional[Dict[str, Any]]:
        """
        Load game state from a file.
        
        Args:
            filename (str): File to load from
            
        Returns:
            Optional[Dict[str, Any]]: Loaded game state or None if failed
        """
        try:
            import json
            with open(filename, 'r') as f:
                state = json.load(f)
            logging.info(f"Game state loaded from {filename}")
            return state
        except Exception as e:
            logging.error(f"Error loading game state: {e}")
            return None

class ErrorHandler:
    @staticmethod
    def handle_game_error(error: Exception, context: str = "") -> None:
        """
        Handle game errors with proper logging and user feedback.
        
        Args:
            error (Exception): The error that occurred
            context (str): Additional context about where the error occurred
        """
        error_msg = f"Error in {context}: {str(error)}"
        logging.error(error_msg)
        print(f"\nAn error occurred: {str(error)}")
        print("The game has been auto-saved. Type 'quit' to exit or press Enter to continue.")

    @staticmethod
    def safe_exit() -> None:
        """Safely exit the game with cleanup."""
        try:
            # Perform any necessary cleanup
            logging.info("Game terminated safely")
            sys.exit(0)
        except Exception as e:
            logging.error(f"Error during safe exit: {e}")
            sys.exit(1)

# Debug utilities for development
class DebugUtils:
    @staticmethod
    def log_game_state(game_state: Dict[str, Any]) -> None:
        """
        Log the current game state for debugging.
        
        Args:
            game_state (Dict[str, Any]): Current game state
        """
        logging.debug("Current game state:")
        for key, value in game_state.items():
            logging.debug(f"{key}: {value}")

    @staticmethod
    def performance_timer(func):
        """
        Decorator to measure function execution time.
        
        Args:
            func: Function to measure
            
        Returns:
            Wrapper function that measures execution time
        """
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            execution_time = end_time - start_time
            logging.debug(f"{func.__name__} execution time: {execution_time:.4f} seconds")
            return result
        return wrapper

# Module-level functions for direct import
def clear_screen() -> None:
    """Clear the terminal screen."""
    return DisplayManager.clear_screen()

def print_slowly(text: str, delay: float = 0.03) -> None:
    """Print text character by character."""
    return DisplayManager.print_slowly(text, delay)

def validate_input(command: str) -> Tuple[bool, str, str]:
    """Validate and parse user input."""
    return InputValidator.validate_command(command)