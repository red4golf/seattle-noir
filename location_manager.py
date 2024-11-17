from typing import Dict, Optional, List
import json
import logging
import config

class LocationManager:
    def __init__(self):
        """Initialize the LocationManager with all game locations and routes."""
        self.current_location: str = config.STARTING_LOCATION
        self.trolley_position: int = 0
        self.trolley_routes=config.TROLLEY_ROUTES
        
        self.locations = config.LOCATIONS
        self.trolley_location = config.TROLLEY_ROUTES
        self.locations = config.LOCATIONS.copy()  # Make a deep copy of the initial locations
        self.original_items = {}  # Store original item locations
        # Store the original item configurations
        for location, data in self.locations.items():
            self.original_items[location] = data.get("items", []).copy()
        
        
    def get_location_description(self) -> str:
        """Get the description of the current location."""
        try:
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
        
        except KeyError as e:
            logging.error(f"Invalid location reference: {self.current_location}")
            return "Error: Location not found."
        except Exception as e:
            logging.error(f"Error getting location description: {e}")
            return "Error: Could not get location description."
    
    def move_to_location(self, direction: str, game_state: Dict) -> bool:
        """
        Move to a new location if the direction is valid and requirements are met.
    
        Args:
            direction (str): The direction to move
            game_state (Dict): Current game state for checking requirements
        
        Returns:
            bool: True if movement was successful, False otherwise
        """
        try:
            if self.current_location not in self.locations:
                logging.error(f"Invalid current location '{self.current_location}'")
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
        
        except Exception as e:
            logging.error(f"Error moving to location: {e}")
            print("There was a problem moving to that location.")
            return False
    
    def handle_trolley(self) -> None:
        """Handle trolley movement and stops."""
        try:
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
           
        except KeyError as e:
            logging.error(f"Invalid trolley position: {self.trolley_position}")
            print("There seems to be a problem with the trolley route.")
        except Exception as e:
            logging.error(f"Error handling trolley: {e}")
            print("There was a problem with the trolley system.")

    def show_historical_note(self, location: str) -> None:
        """Display historical information about the specified location."""
        try:
            if location in self.locations and "historical_note" in self.locations[location]:
                print(f"\nHistorical Note: {self.locations[location]['historical_note']}")
            else:
                print("No historical information available for this location.")
           
        except Exception as e:
            logging.error(f"Error showing historical note for {location}: {e}")
            print("There was a problem accessing the historical information.")

    def get_available_items(self) -> List[str]:
        """Get list of items in current location."""
        try:
            return self.locations[self.current_location].get("items", [])
        except KeyError:
            logging.error(f"Failed to get items - invalid location: {self.current_location}")
            return []
        except Exception as e:
            logging.error(f"Error getting available items: {e}")
            return []

    def remove_item(self, item: str) -> None:
        """Remove an item from the current location."""
        try:
            if "items" in self.locations[self.current_location]:
                items = self.locations[self.current_location]["items"]
                if item in items:
                    items.remove(item)
                    logging.info(f"Removed {item} from {self.current_location}")
        except Exception as e:
            logging.error(f"Error removing item {item} from {self.current_location}: {e}")

    def handle_conversation(self, location: str, game_state: Dict) -> bool:
        """
        Handle conversations with NPCs at the current location.
   
        Args:
            location (str): Current location
            game_state (Dict): Current game state
       
        Returns:
            bool: True if conversation occurred, False otherwise
        """
        try:
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
           
        except Exception as e:
            logging.error(f"Error handling conversation at {location}: {e}")
            print("There was a problem starting the conversation.")
            return False

    def _handle_diner_conversation(self, game_state: Dict) -> bool:
        try:
            print("\nThe waitress at the counter looks up as you approach...")
            return True
        except Exception as e:
            logging.error(f"Error in diner conversation: {e}")
            return False

    def _handle_police_conversation(self, game_state: Dict) -> bool:
        try:
            print("\nYour fellow officers are busy with their own cases...")
            return True
        except Exception as e:
            logging.error(f"Error in police station conversation: {e}")
            return False

    def _handle_waterfront_conversation(self, game_state: Dict) -> bool:
        try:
            print("\nA weathered dock worker pauses from his work...")
            return True
        except Exception as e:
            logging.error(f"Error in waterfront conversation: {e}")
        return False
    def get_location_states(self) -> Dict[str, Dict[str, any]]:
        """Get the current state of all locations."""
        try:
            return {
                location: {
                    "items": self.locations[location].get("items", []).copy(),
                    "first_visit": self.locations[location].get("first_visit", True)
                }
                for location in self.locations
            }
        except Exception as e:
            logging.error(f"Error getting location states: {e}")
            return {}

    def restore_location_states(self, location_states: Dict[str, Dict[str, any]]) -> None:
        """
        Restore location states from saved data.
    
        Args:
            location_states: Dictionary containing saved state of locations
        """
        try:
            for location, state in location_states.items():
                if location in self.locations:
                    # Simply restore the saved state for each location
                    self.locations[location]["items"] = state.get("items", []).copy()
                    self.locations[location]["first_visit"] = state.get("first_visit", True)
        except Exception as e:
            logging.error(f"Error restoring location states: {e}")