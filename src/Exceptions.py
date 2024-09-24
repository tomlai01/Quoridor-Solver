class IllegalPlayException(KeyError):
    def __init__(self, player_id):
        # Call the base class constructor with the custom message
        self.player_id = player_id
        super().__init__()

    def __str__(self):
        # Return the custom message when the exception is printed
        return f"The player {self.player_id} tried to play an illegal move"