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

PUZZLE_REQUIREMENTS = {
    "warehouse_office": {
        "radio_puzzle": ["radio_manual"],
        "description": "The radio equipment looks operational. With the right frequency..."
    },
    "evidence_room": {
        "cipher_puzzle": ["cipher_wheel"],
        "description": "The cipher wheel could help decode any encrypted messages."
    },
    "underground_tunnels": {
        "morse_code": [],
        "description": "You hear faint tapping sounds coming through the walls..."
    }
}

# Add to config.py
GAME_MESSAGES = {
    "NO_PUZZLE": "There are no puzzles to solve here.",
    "NO_PUZZLES_AVAILABLE": "No puzzles are available here right now.",
    "ALREADY_SOLVED": "You've already solved the puzzle here.",
    "PUZZLE_ERROR": "Something went wrong with the puzzle. Try again later.",
    "NO_HANDLER": "No handler found for puzzle:",
    "MISSING_ITEMS": "You need {items} to solve this puzzle."
}

# Add to config.py after existing configurations

# Item Combinations
ITEM_COMBINATIONS = {
    frozenset(['magnifying_glass', 'coded_message']): {
        'result': 'decoded_message',
        'description': "Using the magnifying glass, you notice tiny numbers written between the lines of the coded message. This could be important.",
        'removes_items': False
    },
    frozenset(['coffee', 'case_file']): {
        'result': 'case_insights',
        'description': "As you review the case file while drinking coffee, you notice patterns you missed before. The timeline of thefts corresponds with ship maintenance schedules.",
        'removes_items': ['coffee']
    },
    frozenset(['old_map', 'building_directory']): {
        'result': 'mapped_route',
        'description': "Comparing the old map with the building directory reveals a possible connection between the warehouse district and underground tunnels.",
        'removes_items': False
    },
    frozenset(['radio_manual', 'coded_message']): {
        'result': 'radio_frequency',
        'description': "The manual's frequency tables help you decode what appears to be a radio frequency hidden in the message.",
        'removes_items': False
    },
    frozenset(['evidence_log', 'shipping_manifest']): {
        'result': 'evidence_connection',
        'description': "Cross-referencing the evidence log with the shipping manifest reveals a pattern of missing medical supplies.",
        'removes_items': False
    },
    frozenset(['newspaper_piece_1', 'newspaper_piece_2']): {
        'result': 'partial_story_1',
        'description': "The pieces fit together, revealing more about the suspicious activities at the docks and early investigation efforts.",
        'removes_items': False
    },
    frozenset(['newspaper_piece_2', 'newspaper_piece_3']): {
        'result': 'partial_story_2',
        'description': "These pieces connect the timeline of events from the initial reports to the port authority's involvement.",
        'removes_items': False
    },
    frozenset(['newspaper_piece_3', 'newspaper_piece_4']): {
        'result': 'partial_story_3',
        'description': "The combined pieces shed light on connections between Seattle's port and other West Coast cities.",
        'removes_items': False
    }
}

# Item Descriptions
ITEM_DESCRIPTIONS = {
    "badge": {
        "basic": "Your detective's badge, recently polished. Number 738.",
        "detailed": "A Seattle Police Department detective's badge, its silver surface showing slight wear. The design dates from the 1930s reform era, featuring the city seal and your number: 738. It carries the weight of responsibility and authority in post-war Seattle.",
        "use_locations": ["smith_tower", "warehouse_district", "suspicious_warehouse"],
        "use_effects": {"smith_tower": "The security guard examines your badge and nods respectfully, granting you access."}
    },
    "case_file": {
        "basic": "A detailed file about recent cargo thefts at the waterfront.",
        "detailed": "A thick manila folder containing reports of cargo thefts. The papers inside smell of tobacco smoke from the briefing room. Post-war shipping records show an alarming pattern of medical supply disappearances.",
        "use_locations": ["police_station", "captain_office"],
        "use_effects": {"police_station": "You review the file carefully, noting key details about the cargo theft pattern."}
    },
    "magnifying_glass": {
        "basic": "A standard-issue detective's magnifying glass.",
        "detailed": "A well-maintained magnifying glass with a brass frame and wooden handle. The kind of tool that reveals the details others miss. Its glass is pristine, perfect for examining evidence closely.",
        "use_locations": ["evidence_room", "warehouse_office"],
        "use_effects": {"evidence_room": "You use the magnifying glass to examine evidence more closely."}
    },
    "coffee": {
        "basic": "A cup of the station's notoriously strong coffee.",
        "detailed": "A cup of coffee from the station's ancient percolator. The ceramic mug has a chip on the rim and bears the faded SPD logo. The coffee is strong enough to wake the dead - just the way Seattle's finest like it.",
        "use_locations": ["all"],
        "use_effects": {"all": "You drink the strong coffee, feeling more alert and focused."},
        "consumable": True
    },
    "newspaper_piece_1": {
        "basic": "A torn piece of newspaper mentioning suspicious activities at the docks.",
        "detailed": "A torn section of the Seattle Post-Intelligencer. The visible date shows last Tuesday. The article mentions unusual night-time activities at Pier 48. Coffee stains mark the corners.",
        "use_locations": ["police_station", "evidence_room"],
        "use_effects": {"evidence_room": "You carefully file the newspaper piece as evidence."}
    },
    "newspaper_piece_2": {
        "basic": "A torn newspaper piece about port authority investigations.",
        "detailed": "Another piece of the Seattle Post-Intelligencer. This section details the port authority's initial investigation and mentions several missing shipments.",
        "use_locations": ["police_station", "evidence_room"],
        "use_effects": {"evidence_room": "You carefully file the newspaper piece as evidence."}
    },
    "newspaper_piece_3": {
        "basic": "A newspaper fragment discussing harbor patrol findings.",
        "detailed": "This piece of the article focuses on harbor patrol reports and their unsuccessful attempts to catch perpetrators in the act.",
        "use_locations": ["police_station", "evidence_room"],
        "use_effects": {"evidence_room": "You carefully file the newspaper piece as evidence."}
    },
    "newspaper_piece_4": {
        "basic": "A newspaper section about West Coast connections.",
        "detailed": "This piece mentions similar incidents in other West Coast ports, suggesting a larger operation.",
        "use_locations": ["police_station", "evidence_room"],
        "use_effects": {"evidence_room": "You carefully file the newspaper piece as evidence."}
    },
    "old_key": {
        "basic": "A rusty key found in the underground tunnels.",
        "detailed": "An old brass key, its surface darkened with age. The worn teeth and distinctive craft suggest it dates back to the early 1900s. The head bears a faint marking: 'W.D.' - Warehouse District?",
        "use_locations": ["suspicious_warehouse", "warehouse_district"],
        "use_effects": {"suspicious_warehouse": "The key fits perfectly in the lock, though it takes some effort to turn."}
    },
    "radio_manual": {
        "basic": "A technical manual for police radio equipment.",
        "detailed": "A well-worn technical manual dated 1945. Pages of frequency tables and operation codes, some marked with recent pencil annotations. The cover bears the seal of the War Department.",
        "use_locations": ["police_station", "warehouse_office"],
        "use_effects": {"warehouse_office": "You reference the manual's frequency tables while examining the radio equipment."}
    },
    "coded_message": {
        "basic": "A message written in some kind of code.",
        "detailed": "A piece of paper with lines of seemingly random letters and numbers. The paper quality and typewriter font suggest recent origin. Certain characters have subtle marks beneath them.",
        "use_locations": ["police_station", "evidence_room", "warehouse_office"],
        "use_effects": {"police_station": "You begin analyzing the coded message, noting patterns in the text."}
    },
    "binoculars": {
        "basic": "A pair of high-quality binoculars.",
        "detailed": "Military-surplus binoculars with 'U.S.N. 1944' stamped on the side. The optics are excellent - perfect for surveillance. They're heavy but well-balanced, with leather neck strap.",
        "use_locations": ["observation_deck", "waterfront"],
        "use_effects": {
            "observation_deck": "From this height, the binoculars give you a clear view of suspicious activity at the docks.",
            "waterfront": "You observe several workers making suspicious exchanges near Pier 48."
        }
    }
}

# Add to config.py after existing configurations

LOCATIONS = {
    "police_station": {
        "description": "You're in the Seattle Police Department headquarters, housed in the Public Safety Building on 4th Avenue. Built in 1909, this fortress-like building has seen its share of cases. The wooden walls are lined with wanted posters, and the smell of coffee fills the air. Your desk is covered with case files.",
        "exits": {"outside": "pike_place", "office": "captain_office", "basement": "evidence_room"},
        "items": ["badge", "case_file", "coffee"],
        "first_visit": True,
        "historical_note": "The Seattle Police Department played a crucial role during WWII, coordinating with the Coast Guard to protect the vital shipyards."
    },
    "pike_place": {
        "description": "The bustling Pike Place Market stretches before you. Even in the post-war era, it's a hive of activity. Fishmongers call out their daily catches, and the aroma of fresh produce fills the air. The historic clock reads 10:45.",
        "exits": {"north": "police_station", "south": "pioneer_square", "east": "trolley_stop", "west": "waterfront"},
        "items": ["newspaper_piece_1", "apple"],
        "first_visit": True,
        "historical_note": "Pike Place Market, opened in 1907, served as a crucial connection between local farmers and urban customers during the war years."
    },
    "pioneer_square": {
        "description": "The historic heart of Seattle surrounds you. Red brick buildings from the late 1800s line the streets. The iconic pergola stands as a testament to the city's past. Underground tour guides share tales of the city's history with passing tourists.",
        "exits": {"north": "pike_place", "east": "smith_tower", "underground": "underground_tunnels"},
        "items": ["newspaper_piece_2", "old_map"],
        "first_visit": True,
        "historical_note": "Pioneer Square was Seattle's first neighborhood, rebuilt in brick after the Great Seattle Fire of 1889."
    },
    "waterfront": {
        "description": "The busy waterfront docks stretch along Elliott Bay. Cargo ships load and unload their wares, while seagulls wheel overhead. The salty air carries the sounds of maritime commerce.",
        "exits": {"east": "pike_place", "north": "warehouse_district"},
        "items": ["newspaper_piece_3", "dock_schedule"],
        "first_visit": True,
        "historical_note": "Seattle's waterfront was a crucial link in the Pacific theater during WWII, handling military supplies and shipbuilding."
    },
    "warehouse_district": {
        "description": "Rows of industrial warehouses line the street. The smell of salt water mingles with diesel fuel. Workers move cargo between buildings and the nearby docks.",
        "exits": {"south": "waterfront", "north": "suspicious_warehouse"},
        "items": ["newspaper_piece_5", "shipping_manifest"],
        "first_visit": True,
        "historical_note": "The warehouse district expanded rapidly during WWII to handle increased military shipping."
    },
    "suspicious_warehouse": {
        "description": "This warehouse looks abandoned at first glance, but you notice signs of recent activity. The windows are covered, and fresh tire tracks mark the entrance.",
        "exits": {"south": "warehouse_district", "enter": "warehouse_interior"},
        "items": [],
        "first_visit": True,
        "historical_note": "Many warehouses were converted from military to civilian use after the war, creating opportunities for illegal operations.",
        "requires": "has_warehouse_key"
    },
    "warehouse_interior": {
        "description": "Inside the warehouse, you find evidence of an organized operation. Crates are stacked systematically, and a office area is set up in the corner.",
        "exits": {"exit": "suspicious_warehouse", "office": "warehouse_office"},
        "items": ["newspaper_piece_6", "manifest_book"],
        "first_visit": True,
        "historical_note": "The interior layout matches standard military supply warehouse designs from the war."
    },
    "warehouse_office": {
        "description": "A small office with a desk, filing cabinet, and radio equipment. Papers are scattered across the desk, some partially burned.",
        "exits": {"main": "warehouse_interior"},
        "items": ["coded_message", "radio_manual"],
        "first_visit": True,
        "historical_note": "Radio equipment like this was commonly used for coordinating military shipments during the war."
    },
    "captain_office": {
        "description": "Captain Morrison's office is neat and orderly. A large window overlooks the street below, and citations line the walls. His desk holds a radio and several urgent reports.",
        "exits": {"out": "police_station"},
        "items": ["case_briefing"],
        "first_visit": True,
        "historical_note": "The office has been occupied by every Seattle Police Captain since 1909."
    },
    "evidence_room": {
        "description": "Metal shelving units fill this basement room. Evidence boxes from various cases are carefully catalogued and stored. A work table sits in the center for examining items.",
        "exits": {"up": "police_station"},
        "items": ["evidence_log", "magnifying_glass"],
        "first_visit": True,
        "historical_note": "The evidence room's organization system was modernized during the 1930s reform era."
    },
    "trolley_stop": {
        "description": "A covered trolley stop with a wooden bench. A route map shows stops throughout the city. The tracks gleam in the light.",
        "exits": {"board": "trolley", "west": "pike_place"},
        "items": ["trolley_schedule"],
        "first_visit": True,
        "historical_note": "Seattle's trolley system, started in 1884, was essential for connecting the city's neighborhoods."
    },
    "trolley": {
        "description": "",  # Empty string since we'll use TrolleySystem's messages
        "exits": {},  # Will be dynamically updated
        "items": [],
        "first_visit": True,
        "historical_note": "Seattle's trolley system, dating from 1884, was instrumental in the city's early growth."
    },
    "smith_tower": {
        "description": "The famous Smith Tower rises above you, its white terra cotta gleaming. Once the tallest building west of the Mississippi, it still commands respect. The elegant lobby features intricate bronze and marble work.",
        "exits": {"west": "pioneer_square", "elevator": "observation_deck"},
        "items": ["building_directory"],
        "first_visit": True,
        "historical_note": "Completed in 1914, the Smith Tower remained the tallest building on the West Coast until the Space Needle was built in 1962.",
        "requires": "has_badge"
    },
    "observation_deck": {
        "description": "The Chinese Room and observation deck offer a panoramic view of Seattle. The ornate ceiling and carved woodwork contrast with the modern city visible through the windows.",
        "exits": {"elevator": "smith_tower"},
        "items": ["newspaper_piece_7", "binoculars"],
        "first_visit": True,
        "historical_note": "The Chinese Room's furniture was a gift from the Empress of China."
    },
    "underground_tunnels": {
        "description": "The infamous Seattle Underground stretches before you. Brick-lined passages and remnants of old storefronts tell the story of the city's resurrection after the Great Fire. The air is cool and damp.",
        "exits": {"up": "pioneer_square", "north": "secret_warehouse"},
        "items": ["newspaper_piece_4", "old_key"],
        "first_visit": True,
        "historical_note": "These tunnels were created when Seattle raised its streets one to two stories after the Great Fire of 1889."
    },
    "secret_warehouse": {
        "description": "A hidden storage area connected to the underground tunnels. Crates marked with medical symbols are stacked against the walls. A makeshift office contains detailed records.",
        "exits": {"south": "underground_tunnels"},
        "items": ["newspaper_piece_8", "smuggling_plans"],
        "first_visit": True,
        "historical_note": "The underground areas were occasionally used for illegal storage during Prohibition.",
        "requires": "found_secret_entrance"
    }
}

# Add trolley routes configuration
TROLLEY_ROUTES = {
    0: {"description": "Downtown Stop", "exits": {"off": "pike_place"}},
    1: {"description": "Pioneer Square Stop", "exits": {"off": "pioneer_square"}},
    2: {"description": "Waterfront Stop", "exits": {"off": "waterfront"}},
    3: {"description": "Smith Tower Stop", "exits": {"off": "smith_tower"}}
}

# Version Information
GAME_VERSION = "1.0.0"
SAVE_FILE_VERSION = "1.0.0"