from typing import Dict, List, Set, Tuple
import random
from .base_puzzle import BasePuzzle
from utils import print_text
from input_validator import InputValidator

class RadioPuzzle(BasePuzzle):
    """
    Enhanced radio frequency puzzle implementation.
    Players must tune to correct frequencies to intercept suspicious transmissions.
    """

    def __init__(self):
        # Initialize base puzzle features
        super().__init__()
        
        # Define frequency ranges for different radio bands
        self.RADIO_RANGES = {
            "emergency": (1400, 1500),
            "police": (1200, 1300),
            "civilian": (1000, 1100)
        }
        
        # Define possible messages for each band
        self.RADIO_MESSAGES = {
            "emergency": [
                ("...urgent shipment tonight... dock 7... look for red star...",
                 "Emergency broadcast about suspicious shipment"),
                ("...medical supplies... warehouse district... midnight...",
                 "Emergency alert about medical supplies"),
            ],
            "police": [
                ("...patrol units report to waterfront... suspicious activity...",
                 "Police dispatch about waterfront"),
                ("...all units... warehouse district... maintain surveillance...",
                 "Police alert about warehouse"),
            ],
            "civilian": [
                ("...weather forecast: heavy rain expected... port closing early...",
                 "Civilian broadcast about weather"),
                ("...dock workers union meeting... discussing night shifts...",
                 "Civilian broadcast about dock workers"),
            ]
        }
        
        # Puzzle state variables
        self.active_frequencies = self._generate_frequencies()
        self.found_frequencies: Set[str] = set()
        
        # Override base puzzle settings
        self.max_attempts = 8  # More attempts for this puzzle due to its nature

    @property
    def requirements(self) -> List[str]:
        """Required items for this puzzle."""
        return ["radio_manual"]

    def _generate_frequencies(self) -> Dict[str, Tuple[int, str]]:
        """
        Generate random target frequencies within each range with messages.
        Each band gets a random frequency and message.
        """
        active = {}
        with self.error_handler("frequency generation"):
            for band, (min_freq, max_freq) in self.RADIO_RANGES.items():
                frequency = random.randint(min_freq, max_freq)
                message, _ = random.choice(self.RADIO_MESSAGES[band])
                active[band] = (frequency, message)
            return active
        
    def _validate_frequency(self, frequency: str) -> bool:
        """
        Validate user input for frequency.
        Ensures input is a number within valid ranges.
        """
        try:
            freq = int(frequency)
            min_freq = min(r[0] for r in self.RADIO_RANGES.values())
            max_freq = max(r[1] for r in self.RADIO_RANGES.values())
            return min_freq <= freq <= max_freq
        except ValueError:
            return False

    def get_signal_strength(self, frequency: int) -> Tuple[str, str, str]:
        """
        Calculate signal strength and return appropriate message.
        Returns tuple of (strength, message, band).
        """
        best_strength = "NONE"
        best_message = ""
        best_band = ""
        
        for band, (target_freq, message) in self.active_frequencies.items():
            difference = abs(target_freq - frequency)
            
            if difference == 0:
                return "STRONG", message, band
            elif difference <= 10 and best_strength != "STRONG":
                best_strength = "MODERATE"
                best_message = "Through the static, you hear fragments of a transmission..."
                best_band = band
            elif difference <= 25 and best_strength not in ["STRONG", "MODERATE"]:
                best_strength = "WEAK"
                best_message = "You hear mostly static, but something's there..."
                best_band = band
                
        return best_strength, best_message, best_band

    def _display_puzzle_introduction(self) -> None:
        """
        Display the puzzle introduction and instructions.
        Provides context and guidance to the player.
        """
        intro_text = """
        Objective: Locate the emergency frequency being used by the smugglers.
        The radio manual indicates suspicious activity on emergency channels.

        The radio manual lists several frequency ranges:
        Emergency Services: 1400-1500 kHz  (Known smuggler activity)
        Police Band: 1200-1300 kHz        (May contain useful intel)
        Civilian Band: 1000-1100 kHz      (Dock worker communications)
        """
        print_text(intro_text)
    
    def _handle_strong_signal(self, band: str, message: str, game_state: Dict) -> bool:
        """
        Process a strong signal detection and update game state.
        Returns True if puzzle should continue, False if complete.
        """
        print_text(f"\nClear transmission:")
        print_text(message)
        self.found_frequencies.add(band)
        
        # Check if found emergency frequency
        if band == "emergency" and not game_state.get("solved_radio_puzzle", False):
            print_text("\nThis is it! You've found the smugglers' frequency!")
            game_state["solved_radio_puzzle"] = True
        
        # Check if found all frequencies
        if len(self.found_frequencies) == len(self.RADIO_RANGES):
            print_text("\nBy cross-referencing all the transmissions, you've uncovered")
            print_text("a clear pattern of suspicious activity at the waterfront.")
            game_state["understood_radio"] = True
            return True
            
        return False
    
    def solve(self, inventory: List[str], game_state: Dict) -> bool:
        """
        Main puzzle solving logic.
        Implements the abstract method from BasePuzzle.
        """
        with self.error_handler("radio puzzle"):
            # Check if already solved
            if game_state.get("solved_radio_puzzle", False):
                print_text("\nYou've already decoded the critical emergency transmission.")
                print_text("The radio remains available for scanning other frequencies.")
            
            # Reset frequencies for new attempt
            self.active_frequencies = self._generate_frequencies()
            
            # Display introduction
            self._display_puzzle_introduction()
            
            # Main puzzle loop
            while self.attempts < self.max_attempts:
                try:
                    print_text(f"\nAttempts remaining: {self.max_attempts - self.attempts}")
                    if self.found_frequencies:
                        print_text("Tuned bands: " + ", ".join(self.found_frequencies))
                    
                    guess = input("\nEnter frequency to tune (or 'quit'): ").lower()
                    
                    if guess == "quit":
                        return False
                    
                    # Validate input
                    if not self._validate_frequency(guess):
                        print_text("Please enter a valid frequency number.")
                        continue
                    
                    frequency = int(guess)
                    strength, message, band = self.get_signal_strength(frequency)
                    
                    # Only increment attempts for actual tuning attempts
                    if not self.increment_attempts():
                        break
                    
                    print_text(f"\nSignal Strength: {strength}")
                    
                    if strength == "STRONG":
                        if self._handle_strong_signal(band, message, game_state):
                            return True
                    else:
                        print_text(message)
                    
                    # Give hint after several attempts
                    if self.attempts == 3:
                        print_text("\nHint: Try methodically scanning through each band's range.")
                    
                except ValueError:
                    print_text("Please enter a valid frequency number.")
                except KeyboardInterrupt:
                    print_text("\nRadio operation interrupted.")
                    return False

            print_text("\nThe radio needs time to cool down. Try again later.")
            return False

    def get_state(self) -> Dict:
        """
        Get current puzzle state for saving.
        Extends base state from BasePuzzle.
        """
        state = super().get_state()
        state.update({
            "found_frequencies": list(self.found_frequencies),
            "active_frequencies": {
                band: (freq, msg) 
                for band, (freq, msg) in self.active_frequencies.items()
            }
        })
        return state

    def restore_state(self, state: Dict) -> None:
        """
        Restore puzzle state from saved game.
        Extends base state restoration from BasePuzzle.
        """
        super().restore_state(state)
        self.found_frequencies = set(state.get("found_frequencies", []))
        if "active_frequencies" in state:
            self.active_frequencies = state["active_frequencies"]

    def get_debug_info(self) -> Dict:
        """
        Get debug information about current puzzle state.
        Useful for testing and debugging.
        """
        return {
            "found_frequencies": list(self.found_frequencies),
            "active_frequencies": {
                band: freq for band, (freq, _) in self.active_frequencies.items()
            },
            "attempts": self.attempts,
            "max_attempts": self.max_attempts
        }