import os
import sys
import time
import logging
import json
import shutil
import textwrap
from typing import Tuple, Optional, Dict, Any, List
from functools import wraps
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
import config


# Configure root logger
logging.basicConfig(
    filename=config.LOG_FILE,
    level=logging.INFO,
    format=config.LOG_FORMAT
)

logger = logging.getLogger(__name__)

@dataclass
class SaveGameData:
    """Data structure for saved game state"""
    save_name: str
    save_date: str
    game_state: Dict[str, Any]
    location_states: Dict[str, Dict[str, Any]]
    version: str = "1.0.0"

    def __post_init__(self):
        """Initialize optional fields if they're None"""
        if self.location_states is None:
            self.location_states = {}

class DisplayManager:
    """Handles all display-related functionality in a centralized way."""
    
    @staticmethod
    def get_terminal_size() -> tuple[int, int]:
        """Get current terminal size with fallback values."""
        try:
            width, height = shutil.get_terminal_size()
            width = max(config.MIN_TERMINAL_WIDTH, 
                       min(width, config.MAX_TERMINAL_WIDTH))
            return width, height
        except Exception:
            return config.DEFAULT_TERMINAL_WIDTH, config.DEFAULT_TERMINAL_HEIGHT
    
    @staticmethod
    def wrap_text(text: str, width: Optional[int] = None, indent: int = 0) -> str:
        """Wrap text to fit terminal width with proper indentation."""
        if width is None:
            width, _ = DisplayManager.get_terminal_size()
        
        # Adjust width for indent
        effective_width = width - indent
        
        # Split into paragraphs
        paragraphs = [p.strip() for p in text.strip().split('\n\n')]
        wrapped_paragraphs = []
        
        for paragraph in paragraphs:
            # Normalize spaces
            paragraph = ' '.join(paragraph.split())
            
            # Wrap the paragraph
            wrapped = textwrap.fill(
                paragraph,
                width=effective_width,
                expand_tabs=True,
                replace_whitespace=True,
                break_long_words=False,
                break_on_hyphens=True,
                initial_indent=' ' * indent,
                subsequent_indent=' ' * indent
            )
            
            wrapped_paragraphs.append(wrapped)
        
        return '\n\n'.join(wrapped_paragraphs)
    
    @staticmethod
    def print_text(text: str, delay: Optional[float] = None, 
                  indent: int = 0, wrap: bool = True) -> None:
        """
        Print text with optional wrapping and slow printing effect.
        
        Args:
            text: Text to display
            delay: Delay between characters for slow printing
            indent: Number of spaces to indent text
            wrap: Whether to wrap text to terminal width
        """
        try:
            # Prepare the text
            display_text = DisplayManager.wrap_text(text, indent=indent) if wrap else text
            
            # Print with or without delay
            if delay:
                for char in display_text:
                    sys.stdout.write(char)
                    sys.stdout.flush()
                    time.sleep(delay)
                print()  # Add final newline
            else:
                print(display_text)
                
        except KeyboardInterrupt:
            print("\nDisplay interrupted.")
        except Exception as e:
            logging.error(f"Error displaying text: {e}")
            print("\nError displaying text.")
    
    @staticmethod
    def clear_screen() -> None:
        """Clear the terminal screen."""
        try:
            # Check if running in IDLE
            if 'idlelib.run' in sys.modules:
                print("\n" * 100)
                return
            
            # Use appropriate clear command based on OS
            os.system('cls' if os.name == 'nt' else 'clear')
        except Exception as e:
            logging.error(f"Error clearing screen: {e}")
            print("\n" * 100)  # Fallback
    
    @staticmethod
    def format_location_description(description: str, 
                                  exits: list[str], 
                                  items: list[str]) -> str:
        """Format a location description with exits and items."""
        try:
            if not description:
                raise ValueError("Invalid description")
            
            formatted = description.strip()
            
            if exits:
                formatted += f"\n\nExits: {', '.join(exits)}"
            
            if items:
                formatted += f"\n\nYou can see: {', '.join(items)}"
            
            return formatted
            
        except Exception as e:
            logging.error(f"Error formatting location description: {e}")
            return description  # Return original description on error

# Convenience functions that use DisplayManager
def clear_screen() -> None:
    """Clear the terminal screen."""
    DisplayManager.clear_screen()

def print_text(text: str, delay: Optional[float] = None, 
              indent: int = 0, wrap: bool = True) -> None:
    """Print text using DisplayManager."""
    DisplayManager.print_text(text, delay, indent, wrap)

class InputValidator:
    """Handles input validation for game commands."""
    
    # Valid commands that don't require arguments
    BASIC_COMMANDS = config.BASIC_COMMANDS
    
    # Commands that require arguments
    COMPLEX_COMMANDS = config.COMPLEX_COMMANDS
    
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
class SaveLoadManager:
    def __init__(self, save_dir: str):
        self.save_dir = Path(save_dir)
        self.save_dir.mkdir(exist_ok=True)
        self.logger = logging.getLogger(__name__)

    def save_game(self, game_instance: 'SeattleNoir', save_name: Optional[str] = None) -> bool:
        """Save the current game state to a file."""
        try:
            if not save_name:
                save_name = f"autosave_{int(time.time())}"
            
            # Create save data dictionary with all necessary state
            save_data = {
                'save_name': save_name,
                'save_date': datetime.now().isoformat(),
                'version': config.SAVE_FILE_VERSION,
                'game_state': game_instance.game_state,
                'current_location': game_instance.current_location,
                'location_states': game_instance.location_manager.get_location_states(),
                'inventory_state': game_instance.item_manager.get_inventory_state()
            }
            
            file_path = self.save_dir / f"{save_name}.json"
            
            with open(file_path, 'w') as f:
                json.dump(save_data, f, indent=2)
            
            self.logger.info(f"Game saved successfully to {file_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving game: {e}")
            return False

    def load_game(self, game_instance: 'SeattleNoir', save_name: str) -> bool:
        """Load a saved game state."""
        try:
            file_path = self.save_dir / f"{save_name}.json"
            if not file_path.exists():
                print(f"\nSave file not found: {save_name}")
                return False

            with open(file_path, 'r') as f:
                save_data = json.load(f)

            # Verify save data structure
            required_keys = {'game_state', 'current_location', 'location_states', 'inventory_state'}
            if not all(key in save_data for key in required_keys):
                raise ValueError("Save file is missing required data")

            # Restore game state
            game_instance.game_state = save_data['game_state']
            game_instance.current_location = save_data['current_location']
            
            # Restore location states
            game_instance.location_manager.current_location = save_data['current_location']
            game_instance.location_manager.restore_location_states(save_data['location_states'])
            
            # Restore inventory
            game_instance.item_manager.restore_inventory_state(save_data['inventory_state'])
            
            self.logger.info(f"Game loaded successfully from {file_path}")
            return True

        except Exception as e:
            self.logger.error(f"Error loading game: {str(e)}")
            return False

    def list_saves(self) -> List[Dict[str, Any]]:
        """List all available save files with metadata."""
        saves = []
        for save_file in self.save_dir.glob("*.json"):
            try:
                with open(save_file, 'r') as f:
                    save_data = json.load(f)
                    saves.append({
                        'name': save_data['save_name'],
                        'date': save_data['save_date'],
                        'location': save_data['current_location'],
                        'file_path': str(save_file)
                    })
            except Exception as e:
                self.logger.warning(f"Error reading save file {save_file}: {e}")
                continue
        
        return sorted(saves, key=lambda x: x['date'], reverse=True)
    
    def _verify_loaded_state(self, game_instance: 'SeattleNoir', save_data: SaveGameData) -> None:
        """
        Verify the integrity of loaded game state.
    
        Args:
            game_instance: Current game instance
            save_data: Loaded save data
        """
        try:
            # Verify current location is valid
            if game_instance.current_location not in game_instance.location_manager.locations:
                self.logger.error(f"Invalid current location: {game_instance.current_location}")
            
            # Verify inventory items exist
            for item in game_instance.item_manager.inventory:
                if item not in config.ITEM_DESCRIPTIONS:
                    self.logger.warning(f"Unknown item in inventory: {item}")
                
            # Check for any duplicate items (shouldn't exist in both inventory and locations)
            inventory_items = set(game_instance.item_manager.inventory)
            for location, data in game_instance.location_manager.locations.items():
                location_items = set(data.get("items", []))
                duplicates = inventory_items.intersection(location_items)
                if duplicates:
                    self.logger.warning(f"Found duplicate items in both inventory and location {location}: {duplicates}")
                
        except Exception as e:
            self.logger.error(f"Error verifying loaded state: {e}")

    def list_saves(self) -> List[Dict[str, Any]]:
        """
        List all available save files with metadata.
        
        Returns:
            List of dictionaries containing save file information
        """
        saves = []
        for save_file in self.save_dir.glob("*.json"):
            try:
                with open(save_file, 'r') as f:
                    save_data = json.load(f)
                saves.append({
                    'name': save_data['save_name'],
                    'date': save_data['save_date'],
                    'location': save_data['current_location'],
                    'file_path': str(save_file)
                })
            except Exception as e:
                self.logger.warning(f"Error reading save file {save_file}: {e}")
        
        return sorted(saves, key=lambda x: x['date'], reverse=True)

    def delete_save(self, save_name: str) -> bool:
        """
        Delete a save file.
        
        Args:
            save_name: Name of save to delete
            
        Returns:
            bool: True if deletion successful, False otherwise
        """
        try:
            file_path = self.save_dir / f"{save_name}.json"
            if file_path.exists():
                file_path.unlink()
                self.logger.info(f"Deleted save file: {file_path}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error deleting save file: {e}")
            return False

    def auto_save(self, game_instance: 'SeattleNoir') -> bool:
        """
        Create an automatic save of the current game state.
        
        Args:
            game_instance: Current game instance
            
        Returns:
            bool: True if autosave successful, False otherwise
        """
        try:
            # Create autosave name with timestamp
            save_name = f"autosave_{int(time.time())}"
            
            # Attempt to save
            if not self.save_game(game_instance, save_name):
                self.logger.error("Failed to create auto-save")
                return False
                
            # Clean up old auto-saves
            self._cleanup_old_autosaves()
            return True
            
        except Exception as e:
            self.logger.error(f"Error during auto-save: {e}")
            return False

    def _cleanup_old_autosaves(self, keep_count: int = config.MAX_AUTO_SAVES) -> None:
        """
        Clean up old auto-save files, keeping only the most recent ones.
        
        Args:
            keep_count: Number of recent auto-saves to keep (default: 5)
        """
        try:
            # Get all auto-save files
            autosaves = []
            for save_file in self.save_dir.glob("autosave_*.json"):
                try:
                    timestamp = int(save_file.stem.split('_')[1])
                    autosaves.append((timestamp, save_file))
                except (IndexError, ValueError):
                    # Handle files that don't match our naming pattern
                    continue
            
            # Sort by timestamp (newest first) and remove old ones
            autosaves.sort(reverse=True)
            
            # Keep the newest 'keep_count' saves, delete the rest
            for _, file_path in autosaves[keep_count:]:
                try:
                    file_path.unlink()
                    self.logger.info(f"Cleaned up old auto-save: {file_path}")
                except Exception as e:
                    self.logger.warning(f"Failed to delete old auto-save {file_path}: {e}")
                    
        except Exception as e:
            self.logger.error(f"Error during auto-save cleanup: {e}")

    def get_autosave_stats(self) -> Dict[str, Any]:
        """
        Get statistics about auto-saves.
        
        Returns:
            Dict containing auto-save statistics
        """
        try:
            autosaves = list(self.save_dir.glob("autosave_*.json"))
            total_size = sum(f.stat().st_size for f in autosaves)
            
            return {
                'count': len(autosaves),
                'total_size_bytes': total_size,
                'oldest': min(f.stat().st_mtime for f in autosaves) if autosaves else None,
                'newest': max(f.stat().st_mtime for f in autosaves) if autosaves else None,
            }
        except Exception as e:
            self.logger.error(f"Error getting auto-save stats: {e}")
            return {
                'count': 0,
                'total_size_bytes': 0,
                'oldest': None,
                'newest': None,
                'error': str(e)
            }

    def manage_saves(self, max_total_size_mb: float = config.MAX_SAVE_DIR_SIZE_MB) -> None:
        """
        Manage all save files to prevent excessive disk usage.
        
        Args:
            max_total_size_mb: Maximum total size of all saves in MB
        """
        try:
            all_saves = list(self.save_dir.glob("*.json"))
            total_size = sum(f.stat().st_size for f in all_saves)
            
            # If total size exceeds limit, remove old auto-saves first
            if total_size > max_total_size_mb * 1024 * 1024:
                self.logger.warning("Save directory size exceeds limit, cleaning up...")
                
                # Sort saves by modification time (oldest first)
                saves_by_time = sorted(
                    (f for f in all_saves if f.stem.startswith('autosave_')),
                    key=lambda f: f.stat().st_mtime
                )
                
                # Remove old auto-saves until we're under the limit
                for save_file in saves_by_time:
                    if total_size <= max_total_size_mb * 1024 * 1024:
                        break
                        
                    try:
                        size = save_file.stat().st_size
                        save_file.unlink()
                        total_size -= size
                        self.logger.info(f"Removed old auto-save to free space: {save_file}")
                    except Exception as e:
                        self.logger.error(f"Failed to remove old save {save_file}: {e}")
                        
        except Exception as e:
            self.logger.error(f"Error managing saves: {e}")

class ErrorHandler:
    # ... rest of the file continues as before ...
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