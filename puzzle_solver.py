from typing import Dict, Optional, List
import random
import logging
import config

class PuzzleSolver:
    def __init__(self):
        self.morse_attempts: int = config.INITIAL_GAME_STATE["morse_attempts"]
        self.cipher_attempts: int = config.INITIAL_GAME_STATE["cipher_attempts"]
        self.radio_frequency: Optional[int] = None
        
        self.MORSE_CODE = {
            'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 
            'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 
            'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 
            'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 
            'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 
            'Z': '--..', ' ': '/'
        }

        # Define puzzle requirements and locations
        self.puzzle_requirements = {
            "warehouse_office": {
                "radio_puzzle": ["radio_manual"],
                "description": "The radio equipment looks operational. With the right frequency..."
            },
            "smith_tower": {
                "car_tracking": ["binoculars"],
                "description": "From this height, you could track vehicle movements in the streets below."
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

    def handle_puzzle(self, location: str, game_state: Dict) -> bool:
        """Main method to handle puzzles based on location."""
        try:
            if location not in self.puzzle_requirements:
                print("There are no puzzles to solve here.")
                return False

            puzzle_info = self.puzzle_requirements[location]
            print("\n" + puzzle_info["description"])

            # Get available puzzles for this location
            available_puzzles = list(puzzle_info.keys())
            available_puzzles.remove("description")  # Remove the description entry

            if not available_puzzles:
                print("No puzzles are available here right now.")
                return False

            # Check if puzzle is already solved
            puzzle_name = available_puzzles[0]  # Each location has one primary puzzle
            if game_state.get(f"solved_{puzzle_name}", False):
                print("You've already solved the puzzle here.")
                return True

            # Check required items
            required_items = puzzle_info[puzzle_name]
            if not all(item in game_state.get("inventory", []) for item in required_items):
                missing_items = [item for item in required_items if item not in game_state.get("inventory", [])]
                print(f"You need {', '.join(missing_items)} to solve this puzzle.")
                return False

            # Route to appropriate puzzle solver
            puzzle_handlers = {
                "radio_puzzle": self.solve_radio_puzzle,
                "car_tracking": self.solve_car_tracking,
                "cipher_puzzle": self.solve_cipher_puzzle,
                "morse_code": self.solve_morse_code
            }

            if puzzle_name in puzzle_handlers:
                return puzzle_handlers[puzzle_name](game_state.get("inventory", []), game_state)
            else:
                logging.error(f"No handler found for puzzle: {puzzle_name}")
                return False

        except Exception as e:
            logging.error(f"Error in puzzle handling: {e}")
            print("Something went wrong with the puzzle. Try again later.")
            return False

    def solve_radio_puzzle(self, inventory: list, game_state: Dict) -> bool:
        """Solve the radio frequency puzzle."""
        try:
            print("\nThe radio manual mentions emergency frequencies used during the war.")
            print("You notice numbers scratched into the desk: 1470 - 1290 - 1400")
            
            while True:
                try:
                    guess = input("\nWhat frequency would you like to tune to? (or 'quit' to leave) ").lower()
                    
                    if guess == "quit":
                        return False
                        
                    if not guess.isdigit():
                        print("Please enter a valid number.")
                        continue
                        
                    if guess == "1400":
                        print("\nThe radio crackles to life! Through the static, you hear:")
                        print("'...shipment arrives at midnight... dock 7... look for the red star...'")
                        game_state["solved_radio_puzzle"] = True
                        return True
                    else:
                        print("\nOnly static comes through. Maybe try another frequency?")
                        
                except ValueError:
                    print("Please enter a valid number.")

        except Exception as e:
            logging.error(f"Error in radio puzzle: {e}")
            return False

    def solve_cipher_puzzle(self, inventory: list, game_state: Dict) -> bool:
        """Solve the cipher wheel puzzle."""
        try:
            print("\nThe cipher wheel has letters around its edge. You notice some markings:")
            print("ZHLAASL = ??????")
            print("\nHint: This might be the name of our city...")
            
            while True:
                answer = input("Enter your decoded word (or 'quit' to leave): ").upper()
                
                if answer.lower() == "quit":
                    return False
                
                if answer == "SEATTLE":
                    print("\nThe wheel clicks! You've broken the code!")
                    game_state["solved_cipher"] = True
                    return True
                else:
                    self.cipher_attempts += 1
                    if self.cipher_attempts >= 3:
                        print("\nHint: Try shifting each letter by 7 positions...")
                    print("\nThat doesn't seem right. Try again.")

        except Exception as e:
            logging.error(f"Error in cipher puzzle: {e}")
            return False

    def solve_car_tracking(self, inventory: list, game_state: Dict) -> bool:
        """Solve the car tracking puzzle."""
        try:
            print("\nFrom this height, you can see several vehicles moving through the streets.")
            print("Your notes mention a blue sedan making regular deliveries.")
            
            pattern = random.choice(["NSEW", "NWSE", "SENW", "SWNE"])
            print("\nYou spot the blue sedan! Quick, track its movements!")
            print("Enter the direction pattern (N/S/E/W):")
            print("Example: If the car goes North, then East, enter: NE")
            
            while True:
                guess = input("Enter pattern (or 'quit' to leave): ").upper()
                
                if guess.lower() == "quit":
                    return False
                
                if not all(c in "NSEW" for c in guess):
                    print("Please use only N, S, E, or W letters.")
                    continue
                
                if guess == pattern:
                    print("\nYou've successfully tracked the car to its destination!")
                    game_state["tracked_car"] = True
                    return True
                else:
                    print("\nYou lost sight of the vehicle. Try again?")
                    print("Hint: The pattern has four directions.")

        except Exception as e:
            logging.error(f"Error in car tracking puzzle: {e}")
            return False

    def solve_morse_code(self, game_state: Dict) -> bool:
        """Solve the morse code puzzle."""
        try:
            morse_message = "... . -.-. .-. . - / .-. --- --- --"
            print("\nYou hear tapping from the walls. It seems to be morse code:")
            print(morse_message)
            print("\nHint: Each letter is separated by a space, words by '/'")
            
            while True:
                answer = input("\nWhat's the message? (or 'quit' to leave): ").upper()
                
                if answer.lower() == "quit":
                    return False
                
                if answer == "SECRET ROOM":
                    print("\nThe tapping suddenly stops. You notice a loose panel in the wall...")
                    game_state["found_secret_room"] = True
                    return True
                
                self.morse_attempts += 1
                if self.morse_attempts >= 3:
                    print("\nExtra hint: S = ... (three dots)")
                print("\nThe tapping continues. Maybe try decoding it again?")

        except Exception as e:
            logging.error(f"Error in morse code puzzle: {e}")
            return False

    def _validate_puzzle_input(self, user_input: str, valid_chars: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789") -> bool:
        """Validate user input for puzzles."""
        return all(char in valid_chars for char in user_input.upper())