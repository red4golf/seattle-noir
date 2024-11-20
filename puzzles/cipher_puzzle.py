from typing import Dict, List, Set
import logging
from .base_puzzle import BasePuzzle

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
        self.attempts: int = 0

    @property
    def requirements(self) -> List[str]:
        return ["cipher_wheel"]

    def apply_cipher(self, text: str, shift: int, decrypt: bool = True) -> str:
        """
        Apply the cipher shift to text.
        
        Args:
            text: Text to encode/decode
            shift: Number of positions to shift
            decrypt: True for decoding, False for encoding
        """
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
        try:
            self.logger.info("Starting cipher puzzle")
            
            # Check for cipher wheel
            if "cipher_wheel" not in inventory:
                print("\nYou'll need the cipher wheel to decode these messages.")
                return False
            
            # If already solved main puzzle but not all ciphers
            if game_state.get("solved_cipher", False):
                print("\nYou've already decoded the main message, but there might be more to find.")
            
            print("\nExamining the cipher wheel, you see:")
            print("- An outer ring with the letters A through Z")
            print("- An inner ring that can be rotated to align with different letters")
            print("- Several encoded messages scratched into the desk:")
            
            # Show available encoded messages
            unsolved = [k for k in self.CIPHER_MESSAGES.keys() if k not in self.solved_ciphers]
            for k in unsolved:
                encoded, _ = self.CIPHER_MESSAGES[k]
                print(f"  {encoded}")
            
            # Main puzzle loop
            attempts = 0
            while attempts < 5:  # Limit attempts for game balance
                try:
                    command = input("\nEnter decoded message (or 'hint' for help, 'quit' to leave): ").upper()
                    
                    if command == 'QUIT':
                        return False
                    
                    if command == 'HINT':
                        if attempts < 2:
                            print("\nTry aligning different letters and looking for patterns.")
                            print("The text might be a local place or common word.")
                        else:
                            print("\nNotice how each letter might be shifted by the same amount...")
                        continue
                    
                    # Check against all unsolved messages
                    solved_this_attempt = False
                    for k in unsolved:
                        encoded, decoded = self.CIPHER_MESSAGES[k]
                        if command == decoded:
                            print(f"\nSuccess! You've decoded '{encoded}' to '{decoded}'!")
                            self.solved_ciphers.add(k)
                            solved_this_attempt = True
                            
                            # Handle specific solutions
                            if k == "initial" and not game_state.get("solved_cipher", False):
                                print("\nThis must be significant - it's the name of our city!")
                                game_state["solved_cipher"] = True
                            elif k == "second":
                                print("\nThe docks... this confirms the waterfront connection.")
                            elif k == "final":
                                print("\nRed Star - this matches what we heard about!")
                                if len(self.solved_ciphers) == len(self.CIPHER_MESSAGES):
                                    print("\nYou've decoded all the messages! The pattern is clear now.")
                            break
                    
                    if solved_this_attempt:
                        # Show remaining message count
                        remaining = len(self.CIPHER_MESSAGES) - len(self.solved_ciphers)
                        if remaining > 0:
                            print(f"\nThere are {remaining} more encoded messages to solve.")
                        return True
                    
                    # Wrong answer
                    attempts += 1
                    print(f"\nThat doesn't seem right. {5 - attempts} attempts remaining.")
                    
                    # Progressive hints
                    if attempts == 2:
                        print("\nHint: Each letter might be shifted by the same amount...")
                    elif attempts == 4:
                        print("\nHint: Try shifting each letter 7 positions...")
                    
                except ValueError as e:
                    self.logger.error(f"Error in cipher input: {e}")
                    print("\nPlease enter a valid message using only letters.")
            
            print("\nThe cipher wheel needs to be realigned. Try again later.")
            return False
            
        except Exception as e:
            self.logger.error(f"Error in cipher puzzle: {e}")
            print("\nThere was a problem with the cipher wheel. Try again later.")
            return False

    def get_state(self) -> Dict:
        """Get current puzzle state."""
        return {
            "solved_ciphers": list(self.solved_ciphers),
            "attempts": self.attempts
        }

    def restore_state(self, state: Dict) -> None:
        """Restore puzzle state."""
        self.solved_ciphers = set(state.get("solved_ciphers", []))
        self.attempts = state.get("attempts", 0)