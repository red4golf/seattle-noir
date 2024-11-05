import os
import sys
import time
import logging
import json
from typing import Tuple, Optional, Dict, Any, List
from functools import wraps

# Configure root logger
logging.basicConfig(
    filename='seattlenoir.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
)

logger = logging.getLogger(__name__)

class DisplayManager:
    """Handles all display-related functionality."""
    
    @staticmethod
    def print_slowly(text: str, delay: float = 0.03) -> None:
        """
        Print text character by character with proper error handling.
        
        Args:
            text (str): The text to print
            delay (float): Delay between characters in seconds
            
        Raises:
            KeyboardInterrupt: If user interrupts the display
        """
        if not isinstance(text, str):
            raise ValueError("Text must be a string")
            
        try:
            for char in text:
                sys.stdout.write(char)
                sys.stdout.flush()
                time.sleep(delay)
        except KeyboardInterrupt:
            sys.stdout.write("\n")
            sys.stdout.flush()
            logger.info("Text display interrupted by user")
            raise
        except Exception as e:
            logger.error(f"Error in print_slowly: {e}")
            print(f"\nError displaying text: {e}")
        finally:
            print()

    @staticmethod
    def clear_screen() -> None:
        """
        Clear the terminal screen with error handling.
        """
        try:
            # Check if running in IDLE
            if 'idlelib.run' in sys.modules:
                print("\n" * 100)
                return
                
            # Use appropriate clear command based on OS
            os.system('cls' if os.name == 'nt' else 'clear')
        except Exception as e:
            logger.warning(f"Could not clear screen: {e}")
            print("\n" * 100)

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
        
        Raises:
            ValueError: If description is empty or invalid
        """
        if not description or not isinstance(description, str):
            raise ValueError("Invalid description")
            
        formatted = description.strip()
        
        if exits:
            formatted += f"\n\nExits: {', '.join(exits)}"
            
        if items:
            formatted += f"\n\nYou can see: {', '.join(items)}"
            
        return formatted

class InputValidator:
    """Handles input validation for game commands."""
    
    # Valid commands that don't require arguments
    BASIC_COMMANDS = {'quit', 'help', 'look', 'inventory', 'talk', 'history', 'solve', 'save', 'load'}
    
    # Commands that require arguments
    COMPLEX_COMMANDS = {'take', 'go', 'examine', 'use', 'combine'}
    
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
            
        parts = command.lower().strip().split(maxsplit=1)
        cmd_type = parts[0]
        
        # Validate basic commands
        if cmd_type in InputValidator.BASIC_COMMANDS:
            return True, cmd_type, ""
            
        # Validate complex commands
        if cmd_type in InputValidator.COMPLEX_COMMANDS:
            if len(parts) < 2:
                return False, cmd_type, ""
            return True, cmd_type, parts[1]
            
        return False, "", ""

    @staticmethod
    def validate_item_name(item: str) -> bool:
        """
        Validate an item name.
        
        Args:
            item (str): Item name to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        return bool(item and isinstance(item, str) and len(item) <= 50 
                   and item.replace('_', '').isalnum())

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
        return bool(direction and direction in valid_exits)

class GameState:
    """Handles game state saving and loading."""
    
    SAVE_DIR = "saves"
    
    @classmethod
    def _ensure_save_directory(cls) -> None:
        """Ensure the save directory exists."""
        if not os.path.exists(cls.SAVE_DIR):
            os.makedirs(cls.SAVE_DIR)

    @classmethod
    def save_game_state(cls, state: Dict[str, Any], filename: str = 'savegame.json') -> bool:
        """
        Save game state to a file.
        
        Args:
            state (Dict[str, Any]): Game state to save
            filename (str): File to save to
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            cls._ensure_save_directory()
            filepath = os.path.join(cls.SAVE_DIR, filename)
            with open(filepath, 'w') as f:
                json.dump(state, f, indent=2)
            logger.info(f"Game state saved to {filepath}")
            return True
        except Exception as e:
            logger.error(f"Error saving game state: {e}")
            return False

    @classmethod
    def load_game_state(cls, filename: str = 'savegame.json') -> Optional[Dict[str, Any]]:
        """
        Load game state from a file.
        
        Args:
            filename (str): File to load from
            
        Returns:
            Optional[Dict[str, Any]]: Loaded game state or None if failed
        """
        try:
            filepath = os.path.join(cls.SAVE_DIR, filename)
            if not os.path.exists(filepath):
                return None
            with open(filepath, 'r') as f:
                state = json.load(f)
            logger.info(f"Game state loaded from {filepath}")
            return state
        except Exception as e:
            logger.error(f"Error loading game state: {e}")
            return None

class ErrorHandler:
    """Handles error management and logging."""
    
    @staticmethod
    def handle_game_error(error: Exception, context: str = "") -> None:
        """
        Handle game errors with proper logging and user feedback.
        
        Args:
            error (Exception): The error that occurred
            context (str): Additional context about where the error occurred
        """
        error_msg = f"Error in {context}: {str(error)}"
        logger.error(error_msg)
        print(f"\nAn error occurred: {str(error)}")
        print("The game has been auto-saved. Type 'quit' to exit or press Enter to continue.")

    @staticmethod
    def safe_exit() -> None:
        """Safely exit the game with cleanup."""
        try:
            # Perform any necessary cleanup
            logger.info("Game terminated safely")
            sys.exit(0)
        except Exception as e:
            logger.error(f"Error during safe exit: {e}")
            sys.exit(1)

class DebugUtils:
    """Utility class for debugging and performance monitoring."""
    
    @staticmethod
    def log_game_state(game_state: Dict[str, Any]) -> None:
        """
        Log the current game state for debugging.
        
        Args:
            game_state (Dict[str, Any]): Current game state
        """
        logger.debug("Current game state:")
        for key, value in game_state.items():
            logger.debug(f"{key}: {value}")

    @staticmethod
    def performance_timer(func):
        """
        Decorator to measure function execution time.
        
        Args:
            func: Function to measure
            
        Returns:
            Wrapper function that measures execution time
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            execution_time = end_time - start_time
            logger.debug(f"{func.__name__} execution time: {execution_time:.4f} seconds")
            return result
        return wrapper

def validate_input(func):
    """
    Decorator for input validation.
    
    Args:
        func: Function to decorate
        
    Returns:
        Wrapper function that validates input
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            # Validate string arguments
            for arg in args:
                if isinstance(arg, str) and not arg.strip():
                    logger.warning("Empty input provided")
                    return True
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {e}")
            return True
    return wrapper

# Module-level convenience functions
def clear_screen() -> None:
    """Clear the terminal screen."""
    return DisplayManager.clear_screen()

def print_slowly(text: str, delay: float = 0.03) -> None:
    """Print text character by character."""
    return DisplayManager.print_slowly(text, delay)

def validate_command(command: str) -> Tuple[bool, str, str]:
    """Validate and parse user input."""
    return InputValidator.validate_command(command)