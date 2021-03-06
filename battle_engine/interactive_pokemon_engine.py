"""Pokemon Engine for the player to play against."""

from battle_engine.pokemon_engine import PokemonEngine


class InteractivePokemonEngine(PokemonEngine):
    """The class itself."""

    def run(self, player1, player2):
        """Discontinued feature, see run_turn."""
        raise NotImplementedError("Not implemented in this subclass. See run_turn()")

    def run_turn(self, player1_move, player1, player2):
        """
        Run a turn of this battle.

        Args:
            player1_move (tuple): Move chosen by player1 (the human player).
            player1 (PokemonAgent): The object that is the human player.
            player2 (PokemonAgent): The object that is the computer player.

        Returns:
            Information about the turn, as well as a dictionary with informaton on whether
                or not the game has ended.

        """
        self.game_state["num_turns"] += 1

        player2_move = player2.make_move()

        outcome, turn_info = self.run_single_turn(player1_move, player2_move, player1, player2)
        return turn_info, outcome
