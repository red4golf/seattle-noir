from typing import Dict, List, Optional, Set, Tuple
from .base_puzzle import BasePuzzle
from utils import print_text
from input_validator import InputValidator

class MorsePuzzle(BasePuzzle):
    """
    Enhanced Morse code puzzle implementation.
    Players must decode messages tapped through the walls.
    """

    def __init__(self):
        # Initialize base puzzle features
        super().__init__()
        
        # Morse code lookup dictionary - standard International Morse Code
        self.MORSE_CODE = {
            'A': '.-',    'B': '-...',  'C': '-.-.', 'D': '-..', 
            'E': '.',     'F': '..-.',  'G': '--.',  'H': '....',
            'I': '..',    'J': '.---',  'K': '-.-',  'L': '.-..',
            'M': '--',    'N': '-.',    'O': '---',  'P': '.--.',
            'Q': '--.-',  'R': '.-.',   'S': '...',  'T': '-',
            'U': '..-',   'V': '...-',  'W': '.--',  'X': '-..-',
            'Y': '-.--',  'Z': '--..',  ' ': '/'
        }
        
         # Available messages with their associated data
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
        
        # Puzzle state variables
        self.solved_messages: Set[str] = set()
        self.current_message: Optional[str] = None
        
        # Override base puzzle settings if needed
        self.max_attempts = 5

    @property
    def requirements(self) -> List[str]:
        """No special items required for morse puzzle."""
        return []

    def _encode_message(self, text: str) -> str:
        """
        Convert text to Morse code.
        Used for verifying and generating morse code patterns.
        """
        with self.error_handler("morse encoding"):
            return ' '.join(self.MORSE_CODE.get(char, '') for char in text.upper())

    def _get_current_message(self) -> Tuple[str, str, str]:
        """
        Get a message that hasn't been solved yet.
        Returns tuple of (message_key, morse_code, clue).
        """
        for message, data in self.MESSAGES.items():
            if message not in self.solved_messages:
                return message, data["morse"], data["clue"]
        return "", "", ""

    def _provide_hint(self, message_key: str, attempt_number: int) -> None:
        """
        Provide progressive hints based on attempts.
        Hints become more specific as attempts increase.
        """
        message_data = self.MESSAGES[message_key]
        
        if attempt_number == 1:
            print_text(f"\nHint: {message_data['hint']}")
        elif attempt_number == 2:
            print_text("\nHint: Remember:")
            print_text("S = ... (three dots)")
            print_text("E = . (single dot)")
        elif attempt_number >= 3:
            # Show first letter decoded
            first_char = message_key[0]
            print_text(f"\nHint: The message starts with '{first_char}'")
            print_text(f"'{self.MORSE_CODE[first_char]}' decodes to '{first_char}'")

    def _display_puzzle_introduction(self, morse_code: str, clue: str) -> None:
        """
        Display the puzzle introduction and current message.
        Provides context and instructions to the player.
        """
        intro_text = f"""
        You hear tapping from the walls...
        It seems to be a message about {clue}:

        {morse_code}

        Morse Code Guide:
        - Letters are separated by spaces
        - Words are separated by '/'
        - '.' represents a dot (short tap)
        - '-' represents a dash (long tap)
        """
        print_text(intro_text)

    def _handle_correct_solution(self, message_key: str, game_state: Dict) -> bool:
        """
        Process a correct solution and update game state.
        Returns True if puzzle should continue, False if complete.
        """
        print_text(f"\n{self.MESSAGES[message_key]['success']}")
        self.solved_messages.add(message_key)
        
        # Update game state based on message
        if message_key == "SECRET ROOM":
            game_state["found_secret_room"] = True
            print_text("\nThis must be significant - a secret room in the underground!")
        
        # Check for remaining messages
        remaining = len(self.MESSAGES) - len(self.solved_messages)
        if remaining > 0:
            print_text(f"\nYou can still hear tapping... {remaining} more message(s) to decode.")
            return True
            
        return True

    def solve(self, inventory: List[str], game_state: Dict) -> bool:
        """
        Main puzzle solving logic.
        Implements the abstract method from BasePuzzle.
        """
        with self.error_handler("morse puzzle"):
            # Get next unsolved message
            message_key, morse_code, clue = self._get_current_message()
            if not message_key:
                print_text("\nYou've decoded all the messages in the walls.")
                return True

            self.current_message = message_key
            self._display_puzzle_introduction(morse_code, clue)
            
            # Main puzzle loop
            while self.attempts < self.max_attempts:
                try:
                    command = input("\nWhat's the message? (or 'hint'/'quit'): ").upper()
                    
                    if command == 'QUIT':
                        return False
                        
                    if command == 'HINT':
                        self._provide_hint(message_key, self.attempts)
                        continue
                    
                    # Validate input
                    if not InputValidator.validate_puzzle_input(
                        command, 
                        valid_chars="ABCDEFGHIJKLMNOPQRSTUVWXYZ ",
                        max_length=len(message_key) + 5
                    ):
                        print_text("\nPlease enter a valid message using letters and spaces.")
                        continue
                    
                    # Check solution
                    if command == message_key:
                        return self._handle_correct_solution(message_key, game_state)
                    
                    # Handle incorrect answer
                    if not self.increment_attempts():
                        break

                    # Offer hint on first failure
                    if self.attempts == 1:
                        print_text("Type 'hint' for help.")
                    
                except KeyboardInterrupt:
                    print_text("\nPuzzle attempt interrupted.")
                    return False

            print_text("\nThe tapping fades away. Try listening again later.")
            return False

    def get_state(self) -> Dict:
        """
        Get current puzzle state for saving.
        Extends base state from BasePuzzle.
        """
        state = super().get_state()
        state.update({
            "solved_messages": list(self.solved_messages),
            "current_message": self.current_message
        })
        return state

    def restore_state(self, state: Dict) -> None:
        """
        Restore puzzle state from saved game.
        Extends base state restoration from BasePuzzle.
        """
        super().restore_state(state)
        self.solved_messages = set(state.get("solved_messages", []))
        self.current_message = state.get("current_message")

    def get_morse_chart(self) -> str:
        """
        Return a formatted Morse code reference chart.
        Useful for helping players learn the code.
        """
        chart = "\nMORSE CODE REFERENCE:\n"
        for char, code in sorted(self.MORSE_CODE.items()):
            if char != ' ':
                chart += f"{char}: {code:6} "
                if char in 'EIMT':  # Common letters get special note
                    chart += "(common)"
                chart += "\n"
        return chart

    def get_debug_info(self) -> Dict:
        """
        Get debug information about current puzzle state.
        Useful for testing and debugging.
        """
        return {
            "solved_messages": list(self.solved_messages),
            "current_message": self.current_message,
            "attempts": self.attempts,
            "max_attempts": self.max_attempts
        }