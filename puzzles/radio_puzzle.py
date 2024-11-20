from typing import Dict, List, Set, Tuple
import random
from .base_puzzle import BasePuzzle

class RadioPuzzle(BasePuzzle):
    """Radio frequency puzzle implementation."""

    def __init__(self):
        super().__init__()
        
        # Frequency ranges for different bands
        self.RADIO_RANGES = {
            "emergency": (1400, 1500),
            "police": (1200, 1300),
            "civilian": (1000, 1100)
        }
        
        # Messages that can be heard on each band
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
        
        # Initialize active frequencies for this session
        self.active_frequencies = self._generate_frequencies()
        self.found_frequencies: Set[str] = set()

    @property
    def requirements(self) -> List[str]:
        return ["radio_manual"]

    def _generate_frequencies(self) -> Dict[str, Tuple[int, str]]:
        """Generate random target frequencies within each range with messages."""
        active = {}
        for band, (min_freq, max_freq) in self.RADIO_RANGES.items():
            frequency = random.randint(min_freq, max_freq)
            message, _ = random.choice(self.RADIO_MESSAGES[band])
            active[band] = (frequency, message)
        return active

    def get_signal_strength(self, frequency: int) -> Tuple[str, str, str]:
        """
        Calculate signal strength and return appropriate message.
        
        Args:
            frequency: The frequency being tuned to
            
        Returns:
            Tuple of (signal strength, message, band)
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

    def solve(self, inventory: List[str], game_state: Dict) -> bool:
        """Implement the radio frequency puzzle."""
        try:
            self.logger.info("Starting radio puzzle")
            
            # Check if already solved
            if game_state.get("solved_radio_puzzle", False):
                print("\nYou've already decoded the critical emergency transmission.")
                print("The radio remains available for scanning other frequencies.")
            
            # Reset frequencies for new attempt
            self.active_frequencies = self._generate_frequencies()
            
            # Show initial description
            print("\nObjective: Locate the emergency frequency being used by the smugglers.")
            print("The radio manual indicates suspicious activity on emergency channels.")
            
            print("\nThe radio manual lists several frequency ranges:")
            print("Emergency Services: 1400-1500 kHz  (Known smuggler activity)")
            print("Police Band: 1200-1300 kHz        (May contain useful intel)")
            print("Civilian Band: 1000-1100 kHz      (Dock worker communications)")
            
            attempts_left = 8
            
            while attempts_left > 0:
                try:
                    print(f"\nAttempts remaining: {attempts_left}")
                    if self.found_frequencies:
                        print("Tuned bands:", ", ".join(self.found_frequencies))
                    
                    guess = input("\nEnter frequency to tune (or 'quit'): ").lower()
                    
                    if guess == "quit":
                        return False
                    
                    if not guess.isdigit():
                        print("Please enter a valid number.")
                        continue
                    
                    frequency = int(guess)
                    strength, message, band = self.get_signal_strength(frequency)
                    attempts_left -= 1
                    
                    print(f"\nSignal Strength: {strength}")
                    
                    if strength == "STRONG":
                        print(f"\nClear transmission:")
                        print(message)
                        self.found_frequencies.add(band)
                        
                        # Check if found emergency frequency
                        if band == "emergency" and not game_state.get("solved_radio_puzzle", False):
                            print("\nThis is it! You've found the smugglers' frequency!")
                            game_state["solved_radio_puzzle"] = True
                        
                        # If found all frequencies, give bonus clue
                        if len(self.found_frequencies) == len(self.RADIO_RANGES):
                            print("\nBy cross-referencing all the transmissions, you've uncovered")
                            print("a clear pattern of suspicious activity at the waterfront.")
                            game_state["understood_radio"] = True
                            return True
                    else:
                        print(message)
                    
                    # Give hint after several attempts
                    if attempts_left == 3:
                        print("\nHint: Try methodically scanning through each band's range.")
                    
                except ValueError:
                    print("Please enter a valid frequency number.")
            
            print("\nThe radio needs time to cool down. Try again later.")
            return False
            
        except Exception as e:
            self.logger.error(f"Error in radio puzzle: {e}")
            print("There was a problem with the radio. Try again later.")
            return False

    def get_state(self) -> Dict:
        """Get current puzzle state."""
        return {
            "found_frequencies": list(self.found_frequencies),
            "active_frequencies": {
                band: (freq, msg) 
                for band, (freq, msg) in self.active_frequencies.items()
            }
        }

    def restore_state(self, state: Dict) -> None:
        """Restore puzzle state."""
        self.found_frequencies = set(state.get("found_frequencies", []))
        if "active_frequencies" in state:
            self.active_frequencies = state["active_frequencies"]