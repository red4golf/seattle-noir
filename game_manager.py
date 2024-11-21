from typing import Dict, List, Optional, Tuple
import logging
from location_manager import LocationManager
from item_manager import ItemManager
from utils import clear_screen, SaveLoadManager, print_text
from datetime import datetime
import config
from puzzles.puzzle_manager import PuzzleManager

def show_title_screen():
    """Display the game's title screen with complete title and cityscape."""
    title_art = r"""
════════════════════════════════════════════════════════════════════════════════════════

███████╗███████╗ █████╗ ████████╗████████╗██╗     ███████╗
██╔════╝██╔════╝██╔══██╗╚══██╔══╝╚══██╔══╝██║     ██╔════╝
███████║█████╗  ███████║   ██║      ██║   ██║     █████╗  
╚════██║██╔══╝  ██╔══██║   ██║      ██║   ██║     ██╔══╝  
███████║███████╗██║  ██║   ██║      ██║   ███████╗███████╗
╚══════╝╚══════╝╚═╝  ╚═╝   ╚═╝      ╚═╝   ╚══════╝╚══════╝

███╗   ██╗ ██████╗ ██╗██████╗ 
████╗  ██║██╔═══██╗██║██╔══██╗        A Detective Mystery
██╔██╗ ██║██║   ██║██║██████╔╝             Set in
██║╚██╗██║██║   ██║██║██╔══██╗         1947 Pacific
██║ ╚████║╚██████╔╝██║██║  ██║           Northwest
╚═╝  ╚═══╝ ╚═════╝ ╚═╝╚═╝  ╚═╝

                                      /-\
                                     /   \      Smith           
                                    /     \     Tower          /-\
                           /-\     |   |   |                  |   |
                          /   \    |   |   |                  |   |
                         /     \   |   |   |    Olympic       |   |     Medical
                     /--/   |   \  |   |   |    Hotel      /-|   |     Building
                    /   |   |    \ |   |   |              | ||   |        
                   /    |   |     \|   |   |           /--|-||   |-\
                  /|----|   |      |   |   |          |   | ||   | |    
                 //     |   |      |   |   |          |   | ||   | |
                //      |   |      |   |   |          |   | ||   | |    
               //       |   |      |   |   |          |   | ||   | |
        ______//________|___|______|___|___|__________|___| ||___| |_____________
        ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
                        Elliott Bay Waterfront

            "In a city of rain and secrets, not everyone tells the truth..."

════════════════════════════════════════════════════════════════════════════════════════
"""
    print(title_art)
    input("                    Press Enter to begin your investigation...")

class SeattleNoir:
    """Main game manager class that orchestrates the Seattle Noir detective game."""
    
    def __init__(self):
        """Initialize the game state and managers."""
        self.game_state = config.INITIAL_GAME_STATE.copy()
        
        # Initialize managers
        self.location_manager = LocationManager()
        self.puzzle_manager = PuzzleManager()
        self.item_manager = ItemManager()
        self.save_load_manager = SaveLoadManager(config.SAVE_DIR)
        self.last_save_time = datetime.now()
        self.auto_save_interval = config.AUTO_SAVE_INTERVAL
        
        # Game state properties
        self.newspaper_pieces = 0
        self.current_location = config.STARTING_LOCATION
        
        # Configure logging
        logging.basicConfig(
            filename=config.LOG_FILE,
            level=logging.INFO,
            format=config.LOG_FORMAT
        )

    def show_intro(self) -> None:
        """Display the game's introduction sequence."""
        clear_screen()
        show_title_screen()  
    
        # Check for existing saves
        saves = self.save_load_manager.list_saves()
        if saves:
            print("\nFound existing saves:")
            for save in saves:
                print(f"- {save['name']} ({save['date']})")
                print(f"  Location: {save['location']}")
        
            while True:
                choice = input("\nWould you like to load a save? (enter save name or 'new' for new game): ").strip().lower()
                if choice == 'new':
                    break
                elif choice in [save['name'] for save in saves]:
                    if self.save_load_manager.load_game(self, choice):
                        print(f"\nLoaded save: {choice}")
                        print("\n" + self.location_manager.get_location_description())
                        return  # Skip intro text if loading a save
                    else:
                        print("\nFailed to load save.")
                else:
                    print("\nInvalid save name. Enter a save name from the list or 'new' for new game.")
    
        # Show intro text for new game
        intro_text = """
        The rain beats steadily against your office window at the Seattle Police Department. 
        You're Detective Johnny Diamond, and a new case just landed on your desk.
    
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
        print_text(intro_text, delay=0.03)
        input("\nPress Enter to begin your investigation...")



    def show_help(self) -> None:
        """Display available commands to the player."""
        print("\nAvailable commands:")
        print("- look: Examine your surroundings")
        print("- inventory: Check your belongings")
        print("- take [item]: Pick up an item")
        print("- go [direction]: Move to a new location")
        print("- examine [item]: Look at an item closely")
        print("- talk: Speak to anyone present")
        print("- use [item]: Use an item in your inventory")
        print("- combine [item1] [item2]: Try to use two items together")
        print("- history: Learn historical facts about your location")
        print("- solve: Attempt to solve a puzzle in your location")
        print("- quit: Exit the game")
        print("- save [name]: Save your game")
        print("- load [name]: Load a saved game")
        print("- saves: List available saves")
        print("- help: Show this help message")

    def handle_save_load_commands(self, command: str) -> bool:
        """Handle save/load related commands."""
        cmd_parts = command.split()
        cmd_type = cmd_parts[0]

        if cmd_type == "save":
            save_name = cmd_parts[1] if len(cmd_parts) > 1 else None
            if self.save_load_manager.save_game(self, save_name):
                print("\nGame saved successfully.")
            else:
                print("\nFailed to save game.")
            return True

        elif cmd_type == "load":
            if len(cmd_parts) < 2:
                print("\nPlease specify a save name to load.")
                return True
            
            save_name = cmd_parts[1]
            if self.save_load_manager.load_game(self, save_name):
                print(f"\nLoaded save: {save_name}")
                print("\n" + self.location_manager.get_location_description())
            else:
                print("\nFailed to load save.")
            return True

        elif cmd_type == "saves":
            saves = self.save_load_manager.list_saves()
            if not saves:
                print("\nNo save files found.")
                return True
            
            print("\nAvailable saves:")
            for save in saves:
                print(f"- {save['name']} ({save['date']})")
                print(f"  Location: {save['location']}")
            return True

        return False

    def check_auto_save(self) -> None:
        """Check if it's time for an auto-save and manage save files."""
        current_time = datetime.now()
        if (current_time - self.last_save_time).total_seconds() >= config.AUTO_SAVE_INTERVAL:
            try:
                # Manage saves first
                self.save_load_manager.manage_saves(config.MAX_SAVE_DIR_SIZE_MB)
            
                # Then create new auto-save
                if self.save_load_manager.auto_save(self):
                    self.last_save_time = current_time
                
            except Exception as e:
                logging.error(f"Auto-save error: {e}")

    def process_command(self, command: str) -> bool:
        """Process player commands and return False if quitting, True otherwise."""
        try:
            # Store command for trolley system
            self.location_manager.last_command = command

            # Split the command into parts
            parts = command.split()
            if not parts:
                print("Please enter a command. Type 'help' for options.")
                return True

            cmd_type = parts[0].lower()
            cmd_args = parts[1:] if len(parts) > 1 else [""]

            # Handle save/load commands first
            if cmd_type in ('save', 'load', 'saves'):
                return self.handle_save_load_commands(command)
            
            # Special trolley commands
            if self.current_location == "trolley" and cmd_type in ["status", "history", "look", "next"]:
                self.location_manager.handle_trolley()
                return True

            # Handle combine command separately due to multiple arguments
            if cmd_type == "combine":
                if len(cmd_args) != 2:
                    print("Combine command requires two items. Example: combine map compass")
                    return True
                return (self.item_manager.combine_items(cmd_args[0], cmd_args[1], self.game_state), True)[1]

            if command.startswith('solve'):
                try:
                    return self.puzzle_manager.handle_puzzle(
                        self.current_location,
                        self.item_manager.get_inventory(),
                        self.game_state
                    )
                except Exception as e:
                    logging.error(f"Error in puzzle: {e}")
                    print("\nPuzzle system error. Your progress has been saved.")
                    return True

            # Single argument commands
            command_handlers = {
                "quit": lambda: False,
                "help": lambda: (self.show_help(), True)[1],
                "look": lambda: (print("\n" + self.location_manager.get_location_description()), True)[1],
                "inventory": lambda: (self.item_manager.show_inventory(), True)[1],
                "take": lambda: (self.handle_take_command(cmd_args[0]), True)[1],
                "go": lambda: self.handle_movement_command(cmd_args[0]),
                "examine": lambda: (self.item_manager.examine_item(cmd_args[0], self.location_manager.get_available_items(), self.game_state), True)[1],
                "talk": lambda: (self.handle_talk_command(), True)[1],
                "history": lambda: (self.location_manager.show_historical_note(self.current_location), True)[1],
                "use": lambda: (self.item_manager.use_item(cmd_args[0], self.current_location, self.game_state), True)[1]
            }

            if cmd_type not in command_handlers:
                print("Invalid command. Type 'help' for a list of commands.")
                return True

            result = command_handlers[cmd_type]()
            self.check_auto_save()
            return result

        except Exception as e:
            logging.error(f"Error processing command '{command}': {e}")
            print(f"An error occurred: {e}")
            print("Type 'help' for a list of valid commands.")
            return True
    
    def handle_take_command(self, item: str) -> None:
        """Handle the take command and update game state accordingly."""
        available_items = self.location_manager.get_available_items()
        result = self.item_manager.take_item(item, available_items, self.game_state)
        if result:
            self.location_manager.remove_item(item)
            

    def handle_movement_command(self, direction: str) -> bool:
        """Handle movement commands and location transitions."""
        if direction == "next" and self.current_location == "trolley":
            self.location_manager.handle_trolley()
            return True
        
        if self.location_manager.move_to_location(direction, self.game_state):
            self.current_location = self.location_manager.current_location
            print("\n" + self.location_manager.get_location_description())
            return True
        return True

    def handle_talk_command(self) -> None:
        """Handle conversations with NPCs and update game state."""
        result = self.location_manager.handle_conversation(
            self.current_location,
            self.game_state
        )
        if result and self.current_location == "diner":
            self.game_state["spoke_to_witness"] = True

    def check_game_progress(self) -> bool:
        """Check if the player has solved the case."""
        return (all(self.item_manager.has_item(item) for item in config.REQUIRED_ITEMS) and
                all(self.game_state[state] for state in config.REQUIRED_STATES))

    
    def show_ending(self) -> None:
        """Display the game's ending sequence."""
        ending_text = """
        Congratulations, Detective Diamond!
        
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
        Diamond. You've shown that even in peacetime, Seattle needs heroes who can 
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
        print_text(ending_text)

    def play(self) -> None:
        """Main game loop."""
        try:
            self.show_intro()
            # Show initial location description after intro
            print("\n" + self.location_manager.get_location_description())
        
            playing = True
            while playing:
                try:
                    # Check win condition
                    if self.check_game_progress():
                        self.show_ending()
                        print("\nType 'quit' to exit or continue exploring.")
                
                    # Handle special locations
                    if self.current_location == "trolley":
                        self.location_manager.handle_trolley()
                
                    # Get and process player command
                    command = input("\nWhat would you like to do? ").lower().strip()
                    if not command:
                        print("Please enter a command. Type 'help' for options.")
                        continue
                    
                    playing = self.process_command(command)
                    
                except KeyboardInterrupt:
                    print("\nGame paused. Type 'quit' to exit or press Enter to continue.")
                    try:
                        if input().lower().strip() == 'quit':
                            playing = False
                    except:
                        continue
                except Exception as e:
                    logging.error(f"Error in game loop: {e}")
                    print(f"\nAn error occurred: {e}")
                    print("Type 'quit' to exit or press Enter to continue.")
                    if input().lower().strip() == 'quit':
                        playing = False

        except Exception as e:
            logging.error(f"Critical game error: {e}")
            print(f"\nCritical error occurred: {e}")
        finally:
            print("\nThanks for playing Seattle Noir!")
            self.cleanup()

    def cleanup(self) -> None:
        """Cleanup method to handle any necessary resource cleanup when the game ends."""
        try:
            logging.info("Game session ended normally")
        except Exception as e:
            logging.error(f"Cleanup error: {e}")
            print(f"Error during cleanup: {e}")

if __name__ == "__main__":
    game = SeattleNoir()
    game.play()