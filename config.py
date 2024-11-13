# config.py

from pathlib import Path
from typing import Dict, Any

# File System Settings
SAVE_DIR = Path("saves")
LOG_FILE = "seattle_noir.log"
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"

# Game Settings
AUTO_SAVE_INTERVAL = 300  # seconds (5 minutes)
MAX_SAVE_FILES = 5
MAX_AUTO_SAVES = 3
MAX_SAVE_DIR_SIZE_MB = 50.0

# Display Settings
TEXT_DELAY = 0.03  # seconds between characters for slow text
MIN_TERMINAL_WIDTH = 40
MAX_TERMINAL_WIDTH = 120
DEFAULT_TERMINAL_WIDTH = 80
DEFAULT_TERMINAL_HEIGHT = 24

# Game State Constants
REQUIRED_ITEMS = {
    "torn_letter",
    "dock_schedule",
    "wallet",
    "smuggling_plans",
    "coded_message"
}

REQUIRED_STATES = {
    "spoke_to_witness",
    "discovered_clue",
    "solved_cipher",
    "solved_radio_puzzle",
    "found_secret_room",
    "tracked_car",
    "evidence_connection",
    "decoded_message",
    "mapped_route"
}

# Command Settings
BASIC_COMMANDS = {
    'quit', 'help', 'look', 'inventory', 'talk',
    'history', 'solve', 'save', 'load', 'saves'
}

COMPLEX_COMMANDS = {
    'take', 'go', 'examine', 'use', 'combine'
}

# Initial Game State
INITIAL_GAME_STATE: Dict[str, Any] = {
    "cipher_attempts": 3,
    "inventory": [],
    "current_location": 'start',
    "morse_attempts": 0,
    "car_tracking_attempts": 0,
    "has_badge": False,
    "has_badge_shown": False,
    "found_wallet": False,
    "spoke_to_witness": False,
    "discovered_clue": False,
    "solved_cipher": False,
    "found_secret_room": False,
    "tracked_car": False,
    "solved_radio_puzzle": False,
    "completed_smith_tower": False,
    "found_all_newspaper_pieces": False,
    "warehouse_unlocked": False,
    "understood_radio": False,
    "observed_suspicious_activity": False,
    "case_insights": False,
    "evidence_connection": False,
    "decoded_message": False,
    "radio_frequency": False,
    "mapped_route": False
}

# Starting Location
STARTING_LOCATION = "police_station"

# Version Information
GAME_VERSION = "1.0.0"
SAVE_FILE_VERSION = "1.0.0"