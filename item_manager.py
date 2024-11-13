from typing import Dict, List, Optional, Set, Tuple
from datetime import datetime
import logging
import config

class ItemManager:
    def __init__(self):
        self.inventory: List[str] = []
        self.newspaper_pieces: int = config.INITIAL_GAME_STATE.get("newspaper_pieces", 0)
        self.discovered_combinations: Set[str] = set()
        
        # Define valid item combinations and their results
        self.item_combinations = {
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
            # Add newspaper combinations
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
        
        # Detailed item descriptions with historical context
        self.item_descriptions = {
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

    

    def take_item(self, item: str, location_items: List[str], game_state: Dict) -> bool:
        """Pick up an item from the current location."""
        if item not in location_items:
            print(f"There is no {item} here.")
            return False
        
        self.inventory.append(item)
        
        # Special case for badge and wallet
        if item in config.REQUIRED_ITEMS:
            game_state[f"found_{item}"] = True
            
        # Check for newspaper pieces
        if item.startswith("newspaper_piece_"):
            self.newspaper_pieces += 1
            print(f"You've found piece {self.newspaper_pieces} of 8 of the newspaper story.")
            if self.newspaper_pieces == 8:
                game_state["found_all_newspaper_pieces"] = True
                print("\nYou've collected all newspaper pieces!")
                self.show_newspaper_story()
        else:
            print(f"You take the {item}.")
        
        return True

    def examine_item(self, item: str, location_items: List[str], game_state: Dict) -> None:
        """Examine an item in inventory or in the current location."""
        if item in self.inventory:
            if item in self.item_descriptions:
                print("\n" + self.item_descriptions[item]["detailed"])
                # Check for special examination effects
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

    def use_item(self, item: str, current_location: str, game_state: Dict) -> None:
        """Use an item from the inventory."""
        if item not in self.inventory:
            print("You don't have that item.")
            return
            
        # Check if item has special use effects for this location
        item_data = self.item_descriptions.get(item, {})
        use_effects = item_data.get("use_effects", {})
        valid_locations = item_data.get("use_locations", [])
        
        if current_location in use_effects or ("all" in use_effects and current_location in valid_locations):
            effect = use_effects.get(current_location, use_effects.get("all"))
            print("\n" + effect)
            
            # Handle consumable items
            if item_data.get("consumable", False):
                self.inventory.remove(item)
                print(f"You no longer have the {item}.")
            
            # Handle special item effects
            self._handle_special_item_effects(item, current_location, game_state)
        else:
            print(f"You can't use the {item} here effectively.")

    def _handle_special_item_effects(self, item: str, location: str, game_state: Dict) -> None:
        """Handle special effects when using certain items in specific locations."""
        special_effects = {
            ("badge", "smith_tower"): lambda: game_state.update({"has_badge_shown": True}),
            ("binoculars", "observation_deck"): lambda: game_state.update({"observed_suspicious_activity": True}),
            ("old_key", "suspicious_warehouse"): lambda: game_state.update({"warehouse_unlocked": True}),
            ("radio_manual", "warehouse_office"): lambda: game_state.update({"understood_radio": True})
        }
        
        effect = special_effects.get((item, location))
        if effect:
            effect()

    def combine_items(self, item1: str, item2: str, game_state: Dict) -> bool:
        """Attempt to combine two items from the inventory."""
        if item1 not in self.inventory or item2 not in self.inventory:
            print("You need both items in your inventory to combine them.")
            return False
            
        combo = frozenset([item1, item2])
        if combo in self.item_combinations and combo not in self.discovered_combinations:
            result = self.item_combinations[combo]
            print("\n" + result['description'])
            
            # Remove consumed items if specified
            if result['removes_items']:
                for item in result['removes_items']:
                    if item in self.inventory:
                        self.inventory.remove(item)
            
            # Add combination result to game state
            game_state[result['result']] = True
            self.discovered_combinations.add(combo)
            return True
        elif combo in self.discovered_combinations:
            print("You've already discovered what these items reveal together.")
            return False
        else:
            print("These items can't be combined in any meaningful way.")
            return False

    def show_inventory(self) -> None:
        """Display the current inventory contents with basic descriptions."""
        if not self.inventory:
            print("Your inventory is empty.")
            return
            
        print("\nInventory:")
        for item in self.inventory:
            basic_desc = self.item_descriptions.get(item, {}).get("basic", "No description available.")
            print(f"- {item}: {basic_desc}")
        print("\nTip: Use 'examine <item>' for a closer look.")

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