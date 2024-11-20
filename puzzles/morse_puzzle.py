from typing import Dict, List, Optional, Set, Tuple
from .base_puzzle import BasePuzzle

class MorsePuzzle(BasePuzzle):
    """Morse code puzzle implementation."""

    def __init__(self):
        super().__init__()
        
        # Morse code lookup dictionary
        self.MORSE_CODE = {
            'A': '.-',    'B': '-...',  'C': '-.-.', 'D': '-..',
            'E': '.',     'F': '..-.',  'G': '--.',  'H': '....',
            'I': '..',    'J': '.---',  'K': '-.-',  'L': '.-..',
            'M': '--',    'N': '-.',    'O': '---',  'P': '.--.',
            'Q': '--.-',  'R': '.-.',   'S': '...',  'T': '-',
            'U': '..-',   'V': '...-',  'W': '.--',  'X': '-..-',
            'Y': '-.--',  'Z': '--..',  ' ': '/'
        }
        
        # Available messages with their clues
        self.MESSAGES = {
            "SECRET ROOM": {
                "morse": "... . -.-. .-. . - / .-. --- --- --",
                "clue": "A hidden location",
                "hint": "Think about where something might be concealed...",
                "success": "The tapping reveals a hidden area!"
            },
            "DOCK SEVEN": {
                "morse": "... . ...- . -. / -.. --- -.-. -.-",
                "clue": "A specific location",
                "hint": "Where ships might be found...",
                "success": "Another location revealed through the code!"
            }
        }
        
        self.attempts: int = 0
        self.max_attempts: int = 5
        self.solved_messages: Set[str] = set()
        self.current_message: Optional[str] = None

    @property
    def requirements(self) -> List[str]:
        return []  # No items required for morse puzzle

    def _encode_message(self, text: str) -> str:
        """Convert text to Morse code."""
        return ' '.join(self.MORSE_CODE.get(char, '') for char in text.upper())

    def _get_current_message(self) -> Tuple[str, str, str]:
        """Get a message that hasn't been solved yet."""
        for message, data in self.MESSAGES.items():
            if message not in self.solved_messages:
                return message, data["morse"], data["clue"]
        return "", "", ""

    def _provide_hint(self, message_key: str, attempt_number: int) -> None:
        """Provide progressive hints based on attempts."""
        message_data = self.MESSAGES[message_key]
        
        if attempt_number == 1:
            print(f"\nHint: {message_data['hint']}")
        elif attempt_number == 2:
            print("\nHint: Remember:")
            print("S = ... (three dots)")
            print("E = . (single dot)")
        elif attempt_number >= 3:
            # Show first letter decoded
            first_char = message_key[0]
            print(f"\nHint: The message starts with '{first_char}'")
            print(f"'{self.MORSE_CODE[first_char]}' decodes to '{first_char}'")

    def solve(self, inventory: List[str], game_state: Dict) -> bool:
        """Implement the Morse code puzzle."""
        try:
            self.logger.info("Starting Morse code puzzle")

            # Get next unsolved message
            message_key, morse_code, clue = self._get_current_message()
            if not message_key:
                print("\nYou've decoded all the messages in the walls.")
                return True

            self.current_message = message_key
            
            print("\nYou hear tapping from the walls...")
            print(f"It seems to be a message about {clue}:")
            print(f"\n{morse_code}")
            print("\nMorse Code Guide:")
            print("- Letters are separated by spaces")
            print("- Words are separated by '/'")
            print("- '.' represents a dot (short tap)")
            print("- '-' represents a dash (long tap)")
            
            attempts = 0
            while attempts < self.max_attempts:
                try:
                    command = input("\nWhat's the message? (or 'hint'/'quit'): ").upper()
                    
                    if command == 'QUIT':
                        return False
                        
                    if command == 'HINT':
                        self._provide_hint(message_key, attempts)
                        continue
                    
                    if command == message_key:
                        print(f"\n{self.MESSAGES[message_key]['success']}")
                        self.solved_messages.add(message_key)
                        
                        # Update game state based on message
                        if message_key == "SECRET ROOM":
                            game_state["found_secret_room"] = True
                            print("\nThis must be significant - a secret room in the underground!")
                        
                        # Check if more messages remain
                        remaining = len(self.MESSAGES) - len(self.solved_messages)
                        if remaining > 0:
                            print(f"\nYou can still hear tapping... {remaining} more message(s) to decode.")
                        
                        return True
                    
                    # Wrong answer
                    attempts += 1
                    remaining = self.max_attempts - attempts
                    print(f"\nThat doesn't seem right. {remaining} attempts remaining.")
                    
                    # Offer hint on first failure
                    if attempts == 1:
                        print("Type 'hint' for help.")
                    
                except ValueError as e:
                    self.logger.error(f"Invalid input: {e}")
                    print("\nPlease enter a valid message using letters and spaces.")
            
            print("\nThe tapping fades away. Try listening again later.")
            return False
            
        except Exception as e:
            self.logger.error(f"Error in Morse code puzzle: {e}")
            print("Something interrupted the tapping. Try again later.")
            return False

    def get_state(self) -> Dict:
        """Get current puzzle state."""
        return {
            "attempts": self.attempts,
            "solved_messages": list(self.solved_messages),
            "current_message": self.current_message
        }

    def restore_state(self, state: Dict) -> None:
        """Restore puzzle state."""
        self.attempts = state.get("attempts", 0)
        self.solved_messages = set(state.get("solved_messages", []))
        self.current_message = state.get("current_message")

    def get_morse_chart(self) -> str:
        """Return a formatted Morse code reference chart."""
        chart = "\nMORSE CODE REFERENCE:\n"
        for char, code in sorted(self.MORSE_CODE.items()):
            if char != ' ':
                chart += f"{char}: {code:6} "
                if char in 'EIMT':  # Common letters get special note
                    chart += "(common)"
                chart += "\n"
        return chart