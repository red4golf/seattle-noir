import time
import sys
import os
import json
import random
from typing import Dict, List, Optional, Tuple

class SeattleNoir:
    def __init__(self):
        self.game_state = {
            "morse_attempts": 0,
            "car_tracking_attempts": 0,
            "has_badge": False,
            "found_wallet": False,
            "spoke_to_witness": False,
            "discovered_clue": False,
            "solved_cipher": False,
            "found_secret_room": False,
            "tracked_car": False,
            "solved_radio_puzzle": False,
            "completed_smith_tower": False,
            "found_all_newspaper_pieces": False
        }
        self.inventory: List[str] = []
        self.current_location: str = "police_station"
        self.newspaper_pieces = 0
        self.cipher_attempts = 0
        self.radio_frequency: Optional[int] = None
        self.trolley_position: int = 0

        self.locations: Dict[str, dict] = {
            "police_station": {
                "description": "You're in the Seattle Police Department headquarters, housed in the Public Safety Building on 4th Avenue. Built in 1909, this fortress-like building has seen its share of cases. The wooden walls are lined with wanted posters, and the smell of coffee fills the air. Your desk is covered with case files.",
                "exits": {"outside": "pike_place", "office": "captain_office", "basement": "evidence_room"},
                "items": ["badge", "case_file", "coffee"],
                "first_visit": True,
                "historical_note": "The Seattle Police Department played a crucial role during WWII, coordinating with the Coast Guard to protect the vital shipyards."
            },
            "evidence_room": {
                "description": "The basement evidence room is a maze of filing cabinets and shelves. A vintage radio sits on a desk, its dials beckoning to be tuned. You notice some frequencies written on a nearby notepad.",
                "exits": {"upstairs": "police_station"},
                "items": ["old_files", "radio_manual"],
                "first_visit": True,
                "puzzle": "radio_frequency"
            },
            "pike_place": {
                "description": "The famous Pike Place Market, opened in 1907, bustles with activity. Fish vendors call out their catches of the day, and the salty air mixes with the aroma of fresh bread. Japanese-American vendors' stalls stand empty - a sad reminder of the recent internment.",
                "exits": {"north": "police_station", "east": "alley", "south": "waterfront", "west": "vintage_shop"},
                "items": ["newspaper_piece_1", "fish_wrapper"],
                "first_visit": True,
                "historical_note": "Pike Place Market served as a crucial community hub during WWII rationing, when fresh food was scarce."
            },
            "vintage_shop": {
                "description": "Ye Olde Curiosity Shop, opened in 1899, is cramped with maritime artifacts and local oddities. A mysterious cipher wheel catches your eye among the curios.",
                "exits": {"east": "pike_place"},
                "items": ["cipher_wheel", "newspaper_piece_2"],
                "first_visit": True,
                "puzzle": "cipher"
            },
            "alley": {
                "description": "A narrow alley between brick buildings, typical of Seattle's original streets. Water drips from fire escapes above. Something catches your eye near a trash can. You hear the distant clang of the trolley.",
                "exits": {"west": "pike_place", "north": "diner", "east": "trolley_station"},
                "items": ["wallet", "newspaper_piece_3"],
                "first_visit": True
            },
            "trolley_station": {
                "description": "The trolley station is a hub of city movement. Seattle's electric trolley system, started in 1889, connects all major parts of the city. A route map shows several stops.",
                "exits": {"west": "alley", "board": "trolley"},
                "items": ["trolley_schedule"],
                "first_visit": True,
                "historical_note": "Seattle's trolley system was vital for wartime transportation when gasoline was rationed."
            },
            "trolley": {
                "description": "You're aboard one of Seattle's electric trolleys. The wooden seats and brass fittings speak of an earlier era.",
                "exits": {},  # Dynamic exits based on trolley_position
                "items": [],
                "first_visit": True
            },
            "smith_tower": {
                "description": "At 42 stories, the Smith Tower remains Seattle's tallest building. The ornate lobby features bronze fittings and marble floors. The elevator operator tips his hat as you enter.",
                "exits": {"outside": "pioneer_square", "elevator": "observation_deck"},
                "items": ["business_card"],
                "first_visit": True,
                "historical_note": "Completed in 1914, the Smith Tower has a hidden Chinese Room at the top, popular with sailors during WWII."
            },
            "observation_deck": {
                "description": "The observation deck offers a panoramic view of Seattle's harbor, bustling with wartime shipbuilding activity. Through binoculars, you can track suspicious vehicles below.",
                "exits": {"down": "smith_tower"},
                "items": ["binoculars"],
                "first_visit": True,
                "puzzle": "car_tracking"
            },
            "pioneer_square": {
                "description": "The heart of old Seattle. The square's Victorian architecture recalls the city's gold rush days. The iconic pergola, built in 1909, provides shelter from the rain.",
                "exits": {"north": "smith_tower", "west": "underground_tour", "east": "waterfront"},
                "items": ["newspaper_piece_4"],
                "first_visit": True,
                "historical_note": "Pioneer Square's underground tunnels were used for storage during WWII blackouts."
            },
            "underground_tour": {
                "description": "The ancient underground city beneath Pioneer Square. These subterranean passages were created when Seattle rebuilt atop the ruins of the 1889 fire.",
                "exits": {"east": "pioneer_square", "deeper": "secret_room"},
                "items": ["old_map", "newspaper_piece_5"],
                "first_visit": True,
                "historical_note": "Seattle's underground became a useful network during Prohibition and later for civil defense."
            },
            "secret_room": {
                "description": "A hidden room deep in Seattle's underground. Old crates and prohibition-era bottles line the walls. A mysterious ledger sits on a dusty desk.",
                "exits": {"back": "underground_tour"},
                "items": ["ledger", "key_to_warehouse"],
                "first_visit": True,
                "requires": "solved_cipher"
            },
            "waterfront": {
                "description": "The wooden boardwalk creaks under your feet. Cargo ships dot Elliott Bay, many being converted for war use. The smell of salt water mixes with industrial smoke.",
                "exits": {"north": "pike_place", "east": "warehouse", "south": "fishing_pier", "west": "pioneer_square"},
                "items": ["dock_schedule", "newspaper_piece_6"],
                "first_visit": True,
                "historical_note": "Seattle's waterfront was crucial for wartime shipbuilding and supply operations to Alaska."
            },
            "fishing_pier": {
                "description": "A long wooden pier stretches into Elliott Bay. Fishing boats bob in the water, their crews preparing for tomorrow's catch. A group of fishermen chat nearby.",
                "exits": {"north": "waterfront"},
                "items": ["fishing_log"],
                "first_visit": True
            },
            "warehouse": {
                "description": "The dimly lit warehouse is filled with wooden crates and the smell of fish. Footprints in the dust lead to a back office. Adding to the mystery, you notice morse code tapping from somewhere.",
                "exits": {"west": "waterfront", "north": "office", "trapdoor": "basement_hideout"},
                "items": ["torn_letter", "newspaper_piece_7"],
                "first_visit": True,
                "puzzle": "morse_code"
            },
            "office": {
                "description": "A small back office in the warehouse. Papers and files are strewn about, and a locked safe sits in the corner.",
                "exits": {"south": "warehouse"},
                "items": ["safe_key", "ledger"],
                "first_visit": True
            },
            "basement_hideout": {
                "description": "A secret basement under the warehouse. This appears to be where the smuggling operation has been coordinating their activities.",
                "exits": {"up": "warehouse"},
                "items": ["smuggling_plans", "coded_message"],
                "first_visit": True,
                "requires": "key_to_warehouse"
            },
            "diner": {
                "description": "The neon sign of 'Joe's Diner' flickers above. Inside, the chrome and red vinyl booths shine under fluorescent lights. A nervous witness sits in the corner. The radio plays hits from Glenn Miller.",
                "exits": {"south": "alley"},
                "items": ["coffee_cup", "newspaper_piece_8"],
                "first_visit": True,
                "historical_note": "Diners like this were gathering spots for war news and rationing information."
            },
            "captain_office": {
                "description": "Captain Morrison's office is neat and organized. A map of Seattle hangs on one wall, with several locations marked in red. A half-played game of solitaire sits on his desk.",
                "exits": {"outside": "police_station"},
                "items": ["map", "captain_notes"],
                "first_visit": True
            }
        }
        
        # Initialize trolley routes
        self.trolley_routes = {
            0: {"description": "Downtown Stop", "exits": {"off": "pike_place"}},
            1: {"description": "Pioneer Square Stop", "exits": {"off": "pioneer_square"}},
            2: {"description": "Waterfront Stop", "exits": {"off": "waterfront"}},
            3: {"description": "Smith Tower Stop", "exits": {"off": "smith_tower"}}
        }

    def clear_screen(self):
        """Clear the terminal screen."""
        try:
            os.system('cls' if os.name == 'nt' else 'clear')
        except:
            # If screen clearing fails, just print new lines
            print("\n" * 100)

    def print_slowly(self, text: str, delay: float = 0.03):
        """Print text character by character for dramatic effect."""
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()

    def show_help(self):
        """Display available commands to the player."""
        print("\nAvailable commands:")
        print("- look: Examine your surroundings")
        print("- inventory: Check your belongings")
        print("- take [item]: Pick up an item")
        print("- go [direction]: Move to a new location")
        print("- examine [item]: Look at an item closely")
        print("- talk: Speak to anyone present")
        print("- use [item]: Use an item in your inventory")
        print("- history: Learn historical facts about your location")
        print("- solve: Attempt to solve a puzzle in your location")
        print("- quit: Exit the game")
        print("- help: Show this help message")

    def show_intro(self):
        """Display the game's introduction."""
        self.clear_screen()
        intro_text = """
        Seattle Noir: The Case of the Missing Shipment
        ============================================
        
        Year: 1947
        
        The rain beats steadily against your office window at the Seattle Police Department. 
        You're Detective Sarah/Sam Harper (you choose), and a new case just landed on your desk.
        
        World War II may be over, but Seattle is still adjusting to peacetime. The shipyards 
        that once built warships now handle civilian cargo, and the city is growing faster 
        than ever. But something's not right down at the waterfront.
        
        A valuable medical shipment has disappeared, and rumors suggest it's connected to 
        something bigger. Your investigation will take you through Seattle's historic streets,
        from Pike Place Market to Pioneer Square's underground tunnels.
        
        Your job: Navigate the streets of 1947 Seattle, gather clues, and solve the mystery.
        But remember, in this city of rain and secrets, not everyone tells the truth...
        
        Type 'help' at any time to see available commands.
        """
        self.print_slowly(intro_text)
        input("\nPress Enter to begin your investigation...")

    def show_historical_note(self):
        """Display historical information about the current location."""
        if "historical_note" in self.locations[self.current_location]:
            print("\nHistorical Note:", self.locations[self.current_location]["historical_note"])
        else:
            print("\nNo historical information available for this location.")

    def solve_radio_puzzle(self):
        """Puzzle involving tuning the radio to the correct frequency."""
        if self.current_location != "evidence_room":
            print("There's nothing to solve here.")
            return

        if "radio_manual" not in self.inventory:
            print("You might need the radio manual first.")
            return

        print("\nThe radio manual mentions emergency frequencies used during the war.")
        print("You notice numbers scratched into the desk: 1470 - 1290 - 1400")
        
        guess = input("\nWhat frequency would you like to tune to? ")
        
        if guess == "1400":
            print("\nThe radio crackles to life! Through the static, you hear:")
            self.print_slowly("'...shipment arrives at midnight... dock 7... look for the red star...'")
            self.game_state["solved_radio_puzzle"] = True
        else:
            print("\nOnly static comes through. Maybe try another frequency?")

    def solve_cipher_puzzle(self):
        """Puzzle involving the cipher wheel."""
        if self.current_location != "vintage_shop" or "cipher_wheel" not in self.inventory:
            print("You need to be in the vintage shop with the cipher wheel to solve this puzzle.")
            return

        print("\nThe cipher wheel has letters around its edge. You notice some markings:")
        print("ZHLAASL = ??????")
        print("\nHint: This might be the name of our city...")
        
        answer = input("Enter your decoded word: ").upper()
        
        if answer == "SEATTLE":
            print("\nThe wheel clicks! You've broken the code!")
            self.game_state["solved_cipher"] = True
            self.locations["underground_tour"]["items"].append("secret_map")
        else:
            self.cipher_attempts += 1
            if self.cipher_attempts >= 3:
                print("\nHint: Try shifting each letter by 7 positions...")
            print("\nThat doesn't seem right. Try again.")

    def solve_car_tracking(self):
        """Puzzle for tracking suspicious vehicles from Smith Tower."""
        if self.current_location != "observation_deck" or "binoculars" not in self.inventory:
            print("You need to be at the observation deck with binoculars to track vehicles.")
            return

        print("\nFrom this height, you can see several vehicles moving through the streets.")
        print("Your notes mention a blue sedan making regular deliveries.")
        
        def generate_car_pattern():
            return random.choice(["NSEW", "NWSE", "SENW", "SWNE"])
        
        pattern = generate_car_pattern()
        print("\nYou spot the blue sedan! Quick, track its movements!")
        print("Enter the direction pattern (N/S/E/W):")
        
        guess = input().upper()
        
        if guess == pattern:
            print("\nYou've successfully tracked the car to its destination!")
            self.game_state["tracked_car"] = True
            self.locations["warehouse"]["items"].append("tire_tracks")
        else:
            print("\nYou lost sight of the vehicle. Maybe try again?")

  # Replace the entire solve_morse_code method with this corrected version:
        def solve_morse_code(self):
            """Puzzle involving decoding morse code."""
        if self.current_location != "warehouse":
            print("There's no morse code to decode here.")
            return

    # Morse code dictionary
        MORSE_CODE = {
            'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 
            'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 
            'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 
            'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 
            'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 
            'Z': '--..', ' ': '/'
        }

    # The secret message in morse code
        morse_message = "... . -.-. .-. . - / .-. --- --- --"
    
        print("\nYou hear tapping from the walls. It seems to be morse code:")
        print(morse_message)
    
        answer = input("\nWhat's the message? (hint: two words) ").upper()
    
        if answer == "SECRET ROOM":
            print("\nThe tapping suddenly stops. You notice a loose panel in the wall...")
            self.game_state["found_secret_room"] = True
            if "panel" not in self.locations["warehouse"]["exits"]:
                self.locations["warehouse"]["exits"]["panel"] = "basement_hideout"
            else:
                print("\nThe tapping continues. Maybe try decoding it again?")
                print("Hint: Each letter is separated by a space, words by '/'")
        # Show partial hint after multiple failed attempts
            if "morse_attempts" not in self.game_state:
                self.game_state["morse_attempts"] = 1
            else:
                self.game_state["morse_attempts"] += 1
            if self.game_state["morse_attempts"] >= 3:
                print("\nExtra hint: S = ... (three dots)")

    def handle_trolley(self):
        """Handle trolley movement and stops."""
        if self.current_location != "trolley":
            return
        
        current_stop = self.trolley_routes[self.trolley_position]
        print(f"\nCurrent Stop: {current_stop['description']}")
        
        # Update available exits
        self.locations["trolley"]["exits"] = {
            "off": current_stop["exits"]["off"],
            "next": "trolley"
        }
        
        if self.trolley_position < 3:
            print("The trolley can continue to the next stop.")
        else:
            print("This is the end of the line.")
            self.trolley_position = 0

    def collect_newspaper(self, piece):
        """Handle collection of newspaper pieces."""
        if piece.startswith("newspaper_piece_"):
            self.newspaper_pieces += 1
            if self.newspaper_pieces == 8:
                self.game_state["found_all_newspaper_pieces"] = True
                print("\nYou've collected all newspaper pieces!")
                self.show_newspaper_story()

    def show_newspaper_story(self):
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
        connections to similar cases in San Francisco and Vancouver...
        """
        self.print_slowly(story)

    def use_item(self, item: str):
        """Use an item from the inventory."""
        if item not in self.inventory:
            print("You don't have that item.")
            return
            
        special_items = {
            "cipher_wheel": self.solve_cipher_puzzle,
            "binoculars": self.solve_car_tracking,
            "radio_manual": self.solve_radio_puzzle,
            "key_to_warehouse": lambda: print("Try using this at the warehouse entrance."),
            "map": lambda: print("The map shows several locations marked in red, including some warehouses.")
        }
        
        if item in special_items:
            special_items[item]()
        else:
            print(f"You can't use the {item} right now.")

    def check_game_progress(self) -> bool:
        """Check if the player has solved the case."""
        required_items = {
            "torn_letter",
            "dock_schedule",
            "wallet",
            "smuggling_plans",
            "coded_message"
        }
        
        required_states = {
            "spoke_to_witness",
            "discovered_clue",
            "solved_cipher",
            "solved_radio_puzzle",
            "found_secret_room",
            "tracked_car"
        }
        
        if all(item in self.inventory for item in required_items) and \
           all(self.game_state[state] for state in required_states):
            return True
        return False

    def show_ending(self):
        """Display the game's ending."""
        ending_text = """
        Congratulations, Detective!
        
        As the pieces come together, the full scope of the operation becomes clear. 
        The missing medical supplies were part of a larger smuggling ring using 
        Seattle's historic underground tunnels and converted wartime shipping routes.
        
        Your investigation has uncovered:
        - The secret warehouse operation
        - The underground tunnel network
        - The coded communication system
        - The connection to post-war medical supply shortages
        
        Thanks to your detective work, the Seattle PD raids the smuggling operation. 
        The recovered supplies will now reach their intended destinations, helping 
        hospitals still dealing with the aftermath of the war.
        
        Captain Morrison personally commends your work: "Outstanding detective work, 
        Harper. You've shown that even in peacetime, Seattle needs heroes who can 
        uncover the truth."
        
        As the rain continues to fall outside your office window, you know that
        Seattle is a little safer tonight, thanks to your determination and skill.
        
        THE END
        
        Historical Note: In the post-WWII period, Seattle's transformation from a 
        wartime industrial center to a civilian port created unique challenges for 
        law enforcement. The city's complex network of underground tunnels, dating 
        back to the Great Seattle Fire of 1889, often featured in criminal activities 
        of the era.
        """
        self.print_slowly(ending_text)
    
    # Add these missing methods before the process_command method:

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
        items = location["items"]
        if items:
            item_list = ", ".join(items)
            description += f"\n\nYou can see: {item_list}"
        
        return description

    def take_item(self, item: str):
        """Pick up an item from the current location."""
        if item not in self.locations[self.current_location]["items"]:
            print(f"There is no {item} here.")
            return
        
        self.inventory.append(item)
        self.locations[self.current_location]["items"].remove(item)
        print(f"Taken: {item}")

    # Special case for badge
        if item == "badge":
            self.game_state["has_badge"] = True
        elif item == "wallet":
            self.game_state["found_wallet"] = True
        return

    def examine_item(self, item: str):
        """Examine an item in inventory or in the current location."""
        if item in self.inventory:
            if item == "badge":
                print("Your detective's badge, recently polished. Number 738.")
            elif item == "wallet":
                print("A worn leather wallet. Inside you find a business card for 'Maritime Imports Ltd.'")
                self.game_state["discovered_clue"] = True
            elif item == "cipher_wheel":
                print("A complex wheel with rotating alphabets. Might be useful for decoding messages.")
            elif item == "newspaper_piece_1":
                print("A torn piece of newspaper mentioning suspicious activities at the docks.")
            else:
                print(f"You examine the {item} closely but find nothing unusual.")
        elif item in self.locations[self.current_location]["items"]:
            print(f"You'll need to take the {item} first to examine it closely.")
        else:
            print(f"You don't see any {item} here.")

    def move_to_location(self, direction: str):
        """Move to a new location."""
        if direction not in self.locations[self.current_location]["exits"]:
            print("You can't go that way.")
            return

        new_location = self.locations[self.current_location]["exits"][direction]

    # Check for special requirements
        if new_location in self.locations and "requires" in self.locations[new_location]:
            requirement = self.locations[new_location]["requires"]
            if not self.game_state.get(requirement, False):
                print(f"You can't access the {new_location} yet. You need to {requirement} first.")
                return
    
        self.current_location = new_location
        #print("\n" + self.get_location_description())

    # Handle first visit
        if self.locations[self.current_location]["first_visit"]:
            self.locations[self.current_location]["first_visit"] = False
        print("\n" + self.get_location_description())
        return True
        
        
    def talk(self):
        """Talk to characters in the current location."""
        if self.current_location == "diner":
            if not self.game_state["spoke_to_witness"]:
                print("\nThe nervous witness tells you about strange activities at the waterfront.")
                print("'Every night, around midnight. They think nobody's watching, but I see them...'")
                self.game_state["spoke_to_witness"] = True
            else:
                print("\nThe witness has nothing more to add.")
        
        elif self.current_location == "fishing_pier":
            print("\nThe fishermen mention unusual nighttime activities around warehouse 7.")
            
        elif self.current_location == "captain_office":
            print("\nCaptain Morrison briefs you on recent suspicious activities around the waterfront.")
            
        else:
            print("\nThere's nobody here to talk to.")

    def process_command(self, command: str):
        """Process player commands."""
        command = command.lower().strip()
    
        if command == "quit":
            print("Thanks for playing!")
            return False
        
        elif command == "help":
            self.show_help()
        
        elif command == "look":
            print("\n" + self.get_location_description())
        
        elif command == "inventory":
            if self.inventory:
                print("You are carrying:", ", ".join(self.inventory))
            else:
                print("You aren't carrying anything.")
            
        elif command.startswith("take "):
            item = command[5:]
            self.take_item(item)
            self.collect_newspaper(item)
            
        elif command.startswith("go "):
            direction = command[3:]
            if direction == "next" and self.current_location == "trolley":
                self.trolley_position = (self.trolley_position + 1) % 4
                self.handle_trolley()
            else:
                self.move_to_location(direction)
            
        elif command.startswith("examine "):
            item = command[8:]
            self.examine_item(item)
            
        elif command == "talk":
            self.talk()
        
        elif command == "history":
            self.show_historical_note()
        
        elif command == "solve":
            if self.current_location == "evidence_room":
                self.solve_radio_puzzle()
            elif self.current_location == "vintage_shop":
                self.solve_cipher_puzzle()
            elif self.current_location == "observation_deck":
                self.solve_car_tracking()
            elif self.current_location == "warehouse":
                self.solve_morse_code()
            else:
                print("There's nothing to solve here.")
            
        elif command.startswith("use "):
            item = command[4:]
            self.use_item(item)
        
        else:
            print("I don't understand that command. Type 'help' for a list of commands.")
        
        return True

    def play(self):
        """Main game loop."""
        self.show_intro()
    
        playing = True
        while playing:
            if self.current_location == "trolley":
                self.handle_trolley()
        
        # Show current location description
            print("\n" + self.get_location_description())
        
        # Get and process player command
            command = input("\nWhat would you like to do? ").lower().strip()
            playing = self.process_command(command)
        
        # Check if the player has solved the case
            if self.check_game_progress():
                self.show_ending()
                playing = False
if __name__ == "__main__":
    game = SeattleNoir()
    game.play()