"""
Puzzle package initialization.
Provides access to puzzle classes and manager.
"""

from .base_puzzle import BasePuzzle
from .cipher_puzzle import CipherPuzzle
from .car_puzzle import CarPuzzle
from .morse_puzzle import MorsePuzzle
from .radio_puzzle import RadioPuzzle
from .puzzle_manager import PuzzleManager

__all__ = [
    'BasePuzzle',
    'CipherPuzzle',
    'CarPuzzle',
    'MorsePuzzle',
    'RadioPuzzle',
    'PuzzleManager'
]

# Version information
__version__ = '1.1.0'

# Package metadata
__author__ = 'Charles Einarson'
__email__ = 'red4golf@gmail.com'
__description__ = 'A collection of interactive puzzles for the Seattle Noir game'

# Feature flags
FEATURES = {
    'enhanced_error_handling': True,
    'improved_state_management': True,
    'debug_mode': False
}