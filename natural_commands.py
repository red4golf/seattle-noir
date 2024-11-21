class NaturalCommandHandler:
    """Handles natural language commands with context awareness"""
    
    def __init__(self):
        # Basic direction shortcuts that are always valid
        self.direction_words = {
            # Single letter shortcuts
            'n': 'north',
            's': 'south',
            'e': 'east',
            'w': 'west',
            'u': 'up',
            'd': 'down',
            # Common variations
            'nw': 'northwest',
            'ne': 'northeast',
            'sw': 'southwest',
            'se': 'southeast',
            # Natural language variations
            'upstairs': 'up',
            'downstairs': 'down',
            'upward': 'up',
            'downward': 'down',
            'forward': 'north'  # Assumes north is forward by default
        }

        # Common action words and their variations
        self.action_words = {
            'movement': [
                'go', 'walk', 'run', 'move', 'travel', 'head', 
                'proceed', 'enter', 'leave', 'exit'
            ],
            'taking': [
                'take', 'get', 'grab', 'pick', 'collect', 'acquire'
            ],
            'looking': [
                'look', 'examine', 'check', 'inspect', 'view', 'see',
                'read', 'study', 'observe'
            ],
            'talking': [
                'talk', 'speak', 'chat', 'ask', 'tell', 'say',
                'discuss', 'converse'
            ],
            'quitting': [
                'quit', 'exit', 'bye', 'goodbye', 'leave game'
            ],
            'inventory': [
                'inventory', 'inv', 'i', 'items', 'possessions', 
                'belongings', 'carrying'
            ]
        }

    def understand_command(self, user_input: str, context: str = "normal") -> tuple[str, str]:
        """
        Convert natural language input into game commands based on context.
        
        Args:
            user_input: The raw input from the user
            context: The current context (e.g., "normal", "conversation", "puzzle")
            
        Returns:
            tuple of (command_type, command_argument)
        """
        # Clean up the input
        words = user_input.lower().strip().split()
        if not words:
            return ("invalid", "")

        # First, check for single-word directions
        if len(words) == 1 and words[0] in self.direction_words:
            return ("go", self.direction_words[words[0]])

        # Handle quit variations based on context
        if context == "conversation":
            if any(word in self.action_words['quitting'] for word in words):
                return ("end_conversation", "")
        elif context == "puzzle":
            if any(word in self.action_words['quitting'] for word in words):
                return ("leave_puzzle", "")
        else:
            if any(word in self.action_words['quitting'] for word in words):
                return ("quit", "")

        # Look for direction words anywhere in the input
        for word in words:
            if word in self.direction_words:
                return ("go", self.direction_words[word])

        # Handle inventory checks
        if any(word in self.action_words['inventory'] for word in words):
            return ("inventory", "")

        # Handle looking/examining
        if any(word in self.action_words['looking'] for word in words):
            # If it's just "look" by itself, examine the room
            if len(words) == 1:
                return ("look", "")
            # Otherwise, they're examining something specific
            # Remove the look word and get what they're looking at
            look_word = next(word for word in words if word in self.action_words['looking'])
            target = " ".join(word for word in words if word != look_word)
            return ("examine", target)

        # Handle taking items
        if any(word in self.action_words['taking'] for word in words):
            # Find what they're trying to take
            take_word = next(word for word in words if word in self.action_words['taking'])
            # Special case for "pick up"
            if take_word == "pick" and "up" in words:
                words.remove("up")
            words.remove(take_word)
            item = " ".join(words)
            return ("take", item)

        # Handle talking
        if any(word in self.action_words['talking'] for word in words):
            return ("talk", "")

        # If we can't understand the command, return it as-is for the game to handle
        return ("unknown", user_input)

    def get_simple_help(self) -> str:
        """Returns a simple help message for natural commands"""
        return """
        You can use natural language commands like:
        - "go north" or just "north" or "n" to move
        - "get newspaper" or "take paper" to pick up items
        - "look around" or just "look" to examine your surroundings
        - "check inventory" or "i" to see what you're carrying
        - "examine newspaper" or "read paper" to look at items
        - "talk" to speak with someone
        - "quit" to exit (but try "goodbye" in conversations!)
        
        Just try saying what you want to do in a natural way!
        """

    def convert_item_name(self, item: str) -> str:
        """Convert natural item names to game format"""
        # Handle newspaper pieces specially
        if "newspaper" in item.lower() and "piece" in item.lower():
            words = item.lower().split()
            try:
                # Find the number in the words
                number = next(word for word in words if word.isdigit())
                return f"newspaper_piece_{number}"
            except StopIteration:
                return item.lower().replace(" ", "_")
        
        # Default conversion just replaces spaces with underscores
        return item.lower().replace(" ", "_")