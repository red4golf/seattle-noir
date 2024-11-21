from typing import Dict, List, Set, Optional
import logging
from .base_puzzle import BasePuzzle
from utils import print_text
from input_validator import InputValidator

class CipherPuzzle(BasePuzzle):
    """Cipher wheel puzzle implementation."""

    def __init__(self):
        super().__init__()
        self.CIPHER_SHIFT = 7
        self.CIPHER_MESSAGES = {
            "initial": ("ZLHAASL", "SEATTLE"),  # City name
            "second": ("KVJRZ", "DOCKS"),       # Location clue
            "final": ("YLKZAHY", "REDSTAR")     # Final clue
        }
        self.solved_ciphers: Set[str] = set()
        # Note: removed self.attempts as it's now in BasePuzzle
        self.max_attempts = 5  # Override default from BasePuzzle if needed

    @property
    def requirements(self) -> List[str]:
        return ["cipher_wheel"]

    def apply_cipher(self, text: str, shift: int, decrypt: bool = True) -> str:
        """Apply the cipher shift to text."""
        with self.error_handler("cipher operation"):
            alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            shifted = alphabet[shift:] + alphabet[:shift]
            
            result = ""
            for char in text.upper():
                if char.isalpha():
                    if decrypt:
                        pos = shifted.index(char)
                        result += alphabet[pos]
                    else:
                        pos = alphabet.index(char)
                        result += shifted[pos]
                else:
                    result += char
            return result

    def solve(self, inventory: List[str], game_state: Dict) -> bool:
        """Implement the cipher wheel puzzle."""
        with self.error_handler("cipher puzzle"):
            # Check for cipher wheel
            if "cipher_wheel" not in inventory:
                print_text("\nYou'll need the cipher wheel to decode these messages.")
                return False

            # If already solved main puzzle but not all ciphers
            if game_state.get("solved_cipher", False):
                print_text("\nYou've already decoded the main message, but there might be more to find.")

            self._display_puzzle_introduction()
            
            # Show available encoded messages
            unsolved = [k for k in self.CIPHER_MESSAGES.keys() if k not in self.solved_ciphers]
            for k in unsolved:
                encoded, _ = self.CIPHER_MESSAGES[k]
                print_text(f"  {encoded}")

            # Main puzzle loop
            while self.attempts < self.max_attempts:
                try:
                    command = input("\nEnter decoded message (or 'hint' for help, 'quit' to leave): ").upper()
                    
                    if command == 'QUIT':
                        return False
                    
                    if command == 'HINT':
                        self._provide_hint(self.attempts)
                        continue
                    
                    if not InputValidator.validate_puzzle_input(command):
                        print_text("\nPlease use only letters for your answer.")
                        continue

                    # Check solution
                    if self._check_solution(command, game_state):
                        return True

                    # Wrong answer
                    if not self.increment_attempts():
                        return False

                except KeyboardInterrupt:
                    print_text("\nPuzzle attempt interrupted.")
                    return False

            print_text("\nThe cipher wheel needs to be realigned. Try again later.")
            return False

    def _display_puzzle_introduction(self) -> None:
        """Display the puzzle introduction text."""
        intro_text = """
        Examining the cipher wheel, you see:
        - An outer ring with the letters A through Z
        - An inner ring that can be rotated to align with different letters
        - Several encoded messages scratched into the desk:
        """
        print_text(intro_text)
            
        
    def _provide_hint(self, attempt_number: int) -> None:
        """Provide progressive hints based on attempts."""
        if attempt_number < 2:
            print_text("\nTry aligning different letters and looking for patterns.")
            print_text("The text might be a local place or common word.")
        else:
            print_text("\nNotice how each letter might be shifted by the same amount...")

    def _check_solution(self, command: str, game_state: Dict) -> bool:
        """Check if the provided solution is correct."""
        # Check against all unsolved messages
        for k in [k for k in self.CIPHER_MESSAGES.keys() if k not in self.solved_ciphers]:
            encoded, decoded = self.CIPHER_MESSAGES[k]
            if command == decoded:
                return self._handle_correct_solution(k, encoded, decoded, game_state)
        
        return False

    def _handle_correct_solution(self, key: str, encoded: str, decoded: str, game_state: Dict) -> bool:
        """Handle a correct solution for the puzzle."""
        print_text(f"\nSuccess! You've decoded '{encoded}' to '{decoded}'!")
        self.solved_ciphers.add(key)
        
        # Handle specific solutions
        if key == "initial" and not game_state.get("solved_cipher", False):
            print_text("\nThis must be significant - it's the name of our city!")
            game_state["solved_cipher"] = True
        elif key == "second":
            print_text("\nThe docks... this confirms the waterfront connection.")
        elif key == "final":
            print_text("\nRed Star - this matches what we heard about!")
            if len(self.solved_ciphers) == len(self.CIPHER_MESSAGES):
                print_text("\nYou've decoded all the messages! The pattern is clear now.")
        
        # Show remaining message count
        remaining = len(self.CIPHER_MESSAGES) - len(self.solved_ciphers)
        if remaining > 0:
            print_text(f"\nThere are {remaining} more encoded messages to solve.")
        
        return True

    def get_state(self) -> Dict:
        """Get current puzzle state."""
        state = super().get_state()  # Get base state
        state.update({
            "solved_ciphers": list(self.solved_ciphers)
        })
        return state

    def restore_state(self, state: Dict) -> None:
        """Restore puzzle state."""
        super().restore_state(state)  # Restore base state
        self.solved_ciphers = set(state.get("solved_ciphers", []))