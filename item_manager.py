from typing import Dict, List, Optional, Set, Tuple
from datetime import datetime
import logging
import config

class ItemManager:
    def __init__(self):
        self.inventory: List[str] = []
        self.newspaper_pieces: int = config.INITIAL_GAME_STATE.get("newspaper_pieces", 0)
        self.discovered_combinations: Set[str] = set()
        self.removed_items: Set[str] = set()
           
             
    def take_item(self, item: str, location_items: List[str], game_state: Dict) -> bool:
        """Pick up an item from the current location."""
        try:
            if item not in location_items:
                print(f"There is no {item} here.")
                return False
        
            self.inventory.append(item)
            self.removed_items.add(item)  # Track that this item has been removed
        
            # Handle special items first
            if item == "badge":
                game_state["has_badge"] = True
                print("You clip the badge to your belt. Its familiar weight is reassuring.")
                logging.info("Badge taken and has_badge state set to True")
                return True
            
            # Then handle newspaper pieces
            if item.startswith("newspaper_piece_"):
                self.newspaper_pieces += 1
                print(f"You've found piece {self.newspaper_pieces} of 8 of the newspaper story.")
                if self.newspaper_pieces == 8:
                    game_state["found_all_newspaper_pieces"] = True
                    print("\nYou've collected all newspaper pieces!")
                    self.show_newspaper_story()
                return True
            
            # Generic message for all other items
            print(f"You take the {item}.")
            return True
        
        except Exception as e:
            logging.error(f"Error taking item {item}: {e}")
            print("There was a problem picking up the item.")
            return False
       
    def examine_item(self, item: str, location_items: List[str], game_state: Dict) -> None:
        """Examine an item in inventory or in the current location."""
        try:
            if item in self.inventory:
                if item in config.ITEM_DESCRIPTIONS:
                    print("\n" + config.ITEM_DESCRIPTIONS[item]["detailed"])
                    if item == "wallet" and not game_state.get("discovered_clue", False):
                        game_state["discovered_clue"] = True
                        print("\nThe business card seems suspicious. This could be a valuable lead.")
                    elif item == "coded_message" and not game_state.get("examined_code", False):
                        game_state["examined_code"] = True
                        print("\nThe code looks like it might be decipherable with the right tools...")
                else:
                    print(f"You examine the {item} closely but find nothing unusual.")
            elif item in location_items:
                print(f"You'll need to take the {item} first to examine it closely.")
            else:
                print(f"You don't see any {item} here.")
            
        except Exception as e:
            logging.error(f"Error examining item {item}: {e}")
            print("There was a problem examining the item.")

    def use_item(self, item: str, current_location: str, game_state: Dict) -> None:
        """Use an item from the inventory."""
        try:
            if item not in self.inventory:
                print("You don't have that item.")
                return
           
            item_data = config.ITEM_DESCRIPTIONS.get(item, {})
            use_effects = item_data.get("use_effects", {})
            valid_locations = item_data.get("use_locations", [])
       
            if current_location in use_effects or ("all" in use_effects and current_location in valid_locations):
                effect = use_effects.get(current_location, use_effects.get("all"))
                print("\n" + effect)
           
                if item_data.get("consumable", False):
                    self.inventory.remove(item)
                    print(f"You no longer have the {item}.")
           
                self._handle_special_item_effects(item, current_location, game_state)
            else:
                print(f"You can't use the {item} here effectively.")
           
        except Exception as e:
            logging.error(f"Error using item {item}: {e}")
            print("There was a problem using the item.")

    def _handle_special_item_effects(self, item: str, location: str, game_state: Dict) -> None:
        """Handle special effects when using certain items in specific locations."""
        try:
            special_effects = {
                ("badge", "smith_tower"): lambda: game_state.update({"has_badge_shown": True}),
                ("binoculars", "observation_deck"): lambda: game_state.update({"observed_suspicious_activity": True}),
                ("old_key", "suspicious_warehouse"): lambda: game_state.update({"warehouse_unlocked": True}),
                ("radio_manual", "warehouse_office"): lambda: game_state.update({"understood_radio": True})
        }
       
            effect = special_effects.get((item, location))
            if effect:
                effect()
           
        except Exception as e:
            logging.error(f"Error handling special effect for {item} at {location}: {e}")

    def combine_items(self, item1: str, item2: str, game_state: Dict) -> bool:
        """Attempt to combine two items from the inventory."""
        try:
            if item1 not in self.inventory or item2 not in self.inventory:
                print("You need both items in your inventory to combine them.")
                return False
           
            combo = frozenset([item1, item2])
            if combo in config.ITEM_COMBINATIONS and combo not in self.discovered_combinations:
                result = config.ITEM_COMBINATIONS[combo]
                print("\n" + result['description'])
           
                if result['removes_items']:
                    for item in result['removes_items']:
                        if item in self.inventory:
                            self.inventory.remove(item)
           
                game_state[result['result']] = True
                self.discovered_combinations.add(combo)
                return True
            elif combo in self.discovered_combinations:
                print("You've already discovered what these items reveal together.")
                return False
            else:
                print("These items can't be combined in any meaningful way.")
                return False
           
        except Exception as e:
            logging.error(f"Error combining items {item1} and {item2}: {e}")
            print("There was a problem combining the items.")
            return False

    def show_inventory(self) -> None:
        """Display the current inventory contents with basic descriptions."""
        try:
            if not self.inventory:
                print("Your inventory is empty.")
                return
           
            print("\nInventory:")
            for item in self.inventory:
                basic_desc = config.ITEM_DESCRIPTIONS.get(item, {}).get("basic", "No description available.")
                print(f"- {item}: {basic_desc}")
            print("\nTip: Use 'examine <item>' for a closer look.")
       
        except Exception as e:
            logging.error(f"Error showing inventory: {e}")
            print("There was a problem displaying the inventory.")

    def show_newspaper_story(self) -> None:
        """Display the complete newspaper story once all pieces are collected."""
        story = """
        SEATTLE POST-INTELLIGENCER, 1947
        
        MYSTERIOUS DISAPPEARANCES PLAGUE WATERFRONT
        
        A series of unexplained cargo disappearances has left Seattle Port Authority 
        officials baffled. The incidents, beginning shortly after the war's end, 
        have primarily involved medical supplies and machinery parts.
        
        Local stevedores report unusual night-time activities, but harbor patrol 
        investigations have yielded no concrete evidence. The recent conversion 
        of wartime shipping operations to civilian use has created opportunities 
        for those seeking to exploit the confusion.
        
        Port security chief Thomas McKinnon stated, "We're working closely with 
        the police department to resolve these incidents." Sources suggest possible 
        connections to similar cases in San Francisco and Vancouver.
        
        [Further investigation reveals possible connections to black market medical 
        supply operations taking advantage of post-war shortages and reconstruction 
        efforts across the Pacific coast.]
        """
        print("\nAs you piece together the newspaper clippings, a bigger picture emerges...")
        print(story)
        print("\nThis could be the breakthrough you needed in the case.")

    def get_inventory(self) -> List[str]:
        """Get the current inventory contents."""
        return self.inventory.copy()

    def has_item(self, item: str) -> bool:
        """Check if an item is in the inventory."""
        return item in self.inventory
    
    def get_inventory_state(self) -> Dict[str, any]:
        """Get the complete inventory state including removed items."""
        return {
            "inventory": self.inventory.copy(),
            "removed_items": list(self.removed_items),
            "newspaper_pieces": self.newspaper_pieces
        }
    
    def restore_inventory_state(self, state: Dict[str, any]) -> None:
        """Restore inventory state including removed items."""
        self.inventory = state.get("inventory", []).copy()
        self.removed_items = set(state.get("removed_items", []))
        self.newspaper_pieces = state.get("newspaper_pieces", 0)