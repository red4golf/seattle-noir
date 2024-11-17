from typing import Dict, Optional, List
from config import PUZZLE_REQUIREMENTS
from config import GAME_MESSAGES
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

        
    def handle_puzzle(self, location: str, game_state: Dict) -> bool:
        """Main method to handle puzzles based on location."""
        try:
            logging.info(f"Attempting puzzle at location: {location}")
        
            if location not in PUZZLE_REQUIREMENTS:
                print(GAME_MESSAGES["NO_PUZZLE"])
                return False

            puzzle_info = PUZZLE_REQUIREMENTS[location]
            print("\n" + puzzle_info["description"])

            available_puzzles = [key for key in puzzle_info.keys() if key != "description"]
            if not available_puzzles:
                logging.info("No puzzles available at location")
                print(GAME_MESSAGES["NO_PUZZLES_AVAILABLE"])
                return False

            puzzle_name = available_puzzles[0]
            if game_state.get(f"solved_{puzzle_name}", False):
                logging.info(f"Puzzle {puzzle_name} already solved")
                print(GAME_MESSAGES["ALREADY_SOLVED"])
                return True

            required_items = puzzle_info[puzzle_name]
            if not all(item in game_state.get("inventory", []) for item in required_items):
                missing_items = [item for item in required_items if item not in game_state.get("inventory", [])]
                logging.warning(f"Missing required items: {missing_items}")
                print(GAME_MESSAGES["MISSING_ITEMS"].format(items=', '.join(missing_items)))
                return False

            puzzle_handlers = {
                "radio_puzzle": self.solve_radio_puzzle,
                "car_tracking": self.solve_car_tracking,
                "cipher_puzzle": self.solve_cipher_puzzle,
                "morse_code": self.solve_morse_code
            }

            if puzzle_name not in puzzle_handlers:
                logging.error(f"{GAME_MESSAGES['NO_HANDLER']} {puzzle_name}")
                return False

            return puzzle_handlers[puzzle_name](game_state.get("inventory", []), game_state)

        except Exception as e:
            logging.error(f"Error in puzzle handling: {e}")
            print(GAME_MESSAGES["PUZZLE_ERROR"])
            return False

    def solve_radio_puzzle(self, inventory: list, game_state: Dict) -> bool:
        """Solve the radio frequency puzzle."""
        try:
            logging.info("Starting radio frequency puzzle")
            print("\nThe radio manual mentions emergency frequencies used during the war.")
            print("You notice numbers scratched into the desk: 1470 - 1290 - 1400")
       
            while True:
                try:
                    guess = input("\nWhat frequency would you like to tune to? (or 'quit' to leave) ").lower()
                    logging.info(f"Player guessed frequency: {guess}")
               
                    if guess == "quit":
                        logging.info("Player quit radio puzzle")
                        return False
                   
                    if not guess.isdigit():
                        logging.warning("Invalid frequency input")
                        print("Please enter a valid number.")
                        continue
                   
                    if guess == "1400":
                        logging.info("Player solved radio puzzle")
                        print("\nThe radio crackles to life! Through the static, you hear:")
                        print("'...shipment arrives at midnight... dock 7... look for the red star...'")
                        game_state["solved_radio_puzzle"] = True
                        return True
                    else:
                        logging.info("Incorrect frequency attempt")
                        print("\nOnly static comes through. Maybe try another frequency?")
                   
                except ValueError as ve:
                    logging.error(f"Value error in frequency input: {ve}")
                    print("Please enter a valid number.")

        except KeyboardInterrupt:
            logging.warning("Radio puzzle interrupted by user")
            print("\nPuzzle attempt interrupted")
            return False
        except Exception as e:
            logging.error(f"Error in radio puzzle: {e}")
            print(GAME_MESSAGES["PUZZLE_ERROR"])
            return False

    def solve_cipher_puzzle(self, inventory: list, game_state: Dict) -> bool:
        """Solve the cipher wheel puzzle."""
        try:
            logging.info("Starting cipher puzzle")
            print("\nThe cipher wheel has letters around its edge. You notice some markings:")
            print("ZHLAASL = ??????")
            print("\nHint: This might be the name of our city...")
        
            while True:
                try:
                    answer = input("Enter your decoded word (or 'quit' to leave): ").upper()
                    logging.info(f"Player attempt: {answer}")
                
                    if answer.lower() == "quit":
                        logging.info("Player quit cipher puzzle")
                        return False
                
                    if answer == "SEATTLE":
                        logging.info("Cipher puzzle solved")
                        print("\nThe wheel clicks! You've broken the code!")
                        game_state["solved_cipher"] = True
                        return True
                    else:
                        self.cipher_attempts += 1
                        logging.warning(f"Failed attempt {self.cipher_attempts}")
                        if self.cipher_attempts >= 3:
                            print("\nHint: Try shifting each letter by 7 positions...")
                        print("\nThat doesn't seem right. Try again.")

                except ValueError as ve:
                    logging.error(f"Value error in cipher input: {ve}")
                    print("Please enter valid letters only.")

        except KeyboardInterrupt:
            logging.warning("Cipher puzzle interrupted by user")
            print("\nPuzzle attempt interrupted")
            return False
        except Exception as e:
            logging.error(f"Error in cipher puzzle: {e}")
            print(GAME_MESSAGES["PUZZLE_ERROR"])
            return False

    def solve_car_tracking(self, inventory: list, game_state: Dict) -> bool:
        """Solve the car tracking puzzle."""
        try:
            logging.info("Starting car tracking puzzle")
            print("\nFrom this height, you can see several vehicles moving through the streets.")
            print("Your notes mention a blue sedan making regular deliveries.")
       
            pattern = random.choice(["NSEW", "NWSE", "SENW", "SWNE"])
            print("\nYou spot the blue sedan! Quick, track its movements!")
            print("Enter the direction pattern (N/S/E/W):")
            print("Example: If the car goes North, then East, enter: NE")
       
            while True:
                try:
                    guess = input("Enter pattern (or 'quit' to leave): ").upper()
                    logging.info(f"Player guessed pattern: {guess}")
               
                    if guess.lower() == "quit":
                        logging.info("Player quit car tracking puzzle")
                        return False
               
                    if not all(c in "NSEW" for c in guess):
                        logging.warning(f"Invalid direction input: {guess}")
                        print("Please use only N, S, E, or W letters.")
                        continue
               
                    if guess == pattern:
                        logging.info("Player successfully tracked car")
                        print("\nYou've successfully tracked the car to its destination!")
                        game_state["tracked_car"] = True
                        return True
                    else:
                        logging.info("Incorrect tracking pattern")
                        print("\nYou lost sight of the vehicle. Try again?")
                        print("Hint: The pattern has four directions.")

                except ValueError as ve:
                    logging.error(f"Value error in pattern input: {ve}")
                    print("Please enter valid directions.")

        except KeyboardInterrupt:
            logging.warning("Car tracking puzzle interrupted by user")
            print("\nPuzzle attempt interrupted")
            return False
        except Exception as e:
            logging.error(f"Error in car tracking puzzle: {e}")
            print(GAME_MESSAGES["PUZZLE_ERROR"])
            return False

    def solve_morse_code(self, game_state: Dict) -> bool:
        """Solve the morse code puzzle."""
        try:
            morse_message = "... . -.-. .-. . - / .-. --- --- --"
            logging.info("Starting morse code puzzle")
        
            print("\nYou hear tapping from the walls. It seems to be morse code:")
            print(morse_message)
            print("\nHint: Each letter is separated by a space, words by '/'")
        
            while True:
                answer = input("\nWhat's the message? (or 'quit' to leave): ").upper()
                logging.info(f"Player attempted answer: {answer}")
            
                if answer.lower() == "quit":
                    logging.info("Player quit morse puzzle")
                    return False
            
                if answer == "SECRET ROOM":
                    logging.info("Player solved morse puzzle")
                    game_state["found_secret_room"] = True
                    return True
            
                self.morse_attempts += 1
                logging.warning(f"Failed attempt {self.morse_attempts}")
            
                if self.morse_attempts >= 3:
                    print("\nExtra hint: S = ... (three dots)")
                print("\nThe tapping continues. Maybe try decoding it again?")

        except KeyboardInterrupt:
            logging.warning("Morse puzzle interrupted by user")
            print("\nPuzzle attempt interrupted")
            return False
        except Exception as e:
            logging.error(f"Error in morse code puzzle: {e}")
            print("\nSomething went wrong. Try again later.")
            return False

    def _validate_puzzle_input(self, user_input: str, valid_chars: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789") -> bool:
        """Validate user input for puzzles."""
        return all(char in valid_chars for char in user_input.upper())