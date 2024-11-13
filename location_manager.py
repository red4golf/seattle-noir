from typing import Dict, Optional, List
import json
import config

class LocationManager:
    def __init__(self):
        """Initialize the LocationManager with all game locations and routes."""
        self.current_location: str = config.STARTING_LOCATION
        self.trolley_position: int = 0
        
        # Initialize locations dictionary
        self.locations: Dict[str, dict] = {
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
                "description": "You're aboard one of Seattle's electric trolleys. The wooden seats and brass fixtures speak to an earlier era. Through the windows, you can see the city passing by.",
                "exits": {},  # This will be dynamically updated by handle_trolley
                "items": [],
                "first_visit": True,
                "historical_note": "Seattle's trolley system, dating from 1884, was instrumental in the city's early growth, connecting neighborhoods that were once separated by difficult terrain."
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
        
        # Initialize trolley routes
        self.trolley_routes = {
            0: {"description": "Downtown Stop", "exits": {"off": "pike_place"}},
            1: {"description": "Pioneer Square Stop", "exits": {"off": "pioneer_square"}},
            2: {"description": "Waterfront Stop", "exits": {"off": "waterfront"}},
            3: {"description": "Smith Tower Stop", "exits": {"off": "smith_tower"}}
        }

    def get_location_description(self) -> str:
        """Get the description of the current location."""
        location = self.locations[self.current_location]
        description = location["description"]

        # Add available exits
        exits = location["exits"]
        if exits:
            exit_list = ", ".join(exits.keys())
            description += f"\n\nExits: {exit_list}"
        
        # List items in the room
        items = location.get("items", [])
        if items:
            item_list = ", ".join(items)
            description += f"\n\nYou can see: {item_list}"
        
        return description

    def move_to_location(self, direction: str, game_state: Dict) -> bool:
        """
        Move to a new location if the direction is valid and requirements are met.
        
        Args:
            direction (str): The direction to move
            game_state (Dict): Current game state for checking requirements
            
        Returns:
            bool: True if movement was successful, False otherwise
        """
        if self.current_location not in self.locations:
            print(f"Error: Invalid current location '{self.current_location}'")
            return False

        current_location = self.locations[self.current_location]
        if direction not in current_location["exits"]:
            print("You can't go that way.")
            return False

        new_location = current_location["exits"][direction]
        
        # Check for special requirements
        if new_location in self.locations and "requires" in self.locations[new_location]:
            requirement = self.locations[new_location]["requires"]
            if not game_state.get(requirement, False):
                print(f"You can't access this area yet. You need to {requirement.replace('_', ' ')} first.")
                return False
        
        self.current_location = new_location
        
        # Handle first visit
        if self.locations[new_location]["first_visit"]:
            self.locations[new_location]["first_visit"] = False
            
        return True

    def handle_trolley(self) -> None:
        """Handle trolley movement and stops."""
        if self.current_location != "trolley":
            return
        
        current_stop = self.trolley_routes[self.trolley_position]
        print(f"\nCurrent Stop: {current_stop['description']}")
        
        # Update available exits
        self.locations["trolley"]["exits"] = current_stop["exits"]
        if self.trolley_position < 3:
            self.locations["trolley"]["exits"]["next"] = "trolley"
            self.trolley_position += 1
        else:
            print("This is the end of the line.")
            self.trolley_position = 0

    def show_historical_note(self, location: str) -> None:
        """Display historical information about the specified location."""
        if location in self.locations and "historical_note" in self.locations[location]:
            print(f"\nHistorical Note: {self.locations[location]['historical_note']}")
        else:
            print("No historical information available for this location.")

    def get_available_items(self) -> List[str]:
        """Get list of items in current location."""
        return self.locations[self.current_location].get("items", [])

    def remove_item(self, item: str) -> None:
        """Remove an item from the current location."""
        if "items" in self.locations[self.current_location]:
            items = self.locations[self.current_location]["items"]
            if item in items:
                items.remove(item)

    def handle_conversation(self, location: str, game_state: Dict) -> bool:
        """
        Handle conversations with NPCs at the current location.
        
        Args:
            location (str): Current location
            game_state (Dict): Current game state
            
        Returns:
            bool: True if conversation occurred, False otherwise
        """
        # Add conversation handlers for different locations here
        conversations = {
            "diner": self._handle_diner_conversation,
            "police_station": self._handle_police_conversation,
            "waterfront": self._handle_waterfront_conversation
        }
        
        handler = conversations.get(location)
        if handler:
            return handler(game_state)
        else:
            print("There's nobody here to talk to.")
            return False

    def _handle_diner_conversation(self, game_state: Dict) -> bool:
        print("\nThe waitress at the counter looks up as you approach...")
        # Add diner-specific conversation logic here
        return True

    def _handle_police_conversation(self, game_state: Dict) -> bool:
        print("\nYour fellow officers are busy with their own cases...")
        # Add police station-specific conversation logic here
        return True

    def _handle_waterfront_conversation(self, game_state: Dict) -> bool:
        print("\nA weathered dock worker pauses from his work...")
        # Add waterfront-specific conversation logic here
        return True