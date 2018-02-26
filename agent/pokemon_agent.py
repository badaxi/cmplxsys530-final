"""Class for a pokemon player."""

from numpy.random import uniform
from agent.base_agent import BaseAgent


class PokemonAgent(BaseAgent):
    """Class for a pokemon player."""

    def __init__(self, team):
        """Initialize the agent."""
        if not team:
            raise AttributeError("Team must have at least one pokemon")

        super().__init__(type="PokemonAgent")
        self.team = team
        self.gamestate = None
        self.reset_gamestates()

    def reset_gamestates(self):
        """Reset gamestate values for a new battle."""
        self.gamestate = None
        self.opp_gamestate = None

    def update_gamestate(self, new_gamestate):
        """Update internal gamestate for self."""
        self.gamestate = new_gamestate

    def make_move(self):
        """
        Make a move. 
        
        Either use first move or switch to first pokemon.
        """
        response = ()
        can_switch = len(self.gamestate["team"]) > 0

        if can_switch and uniform() < 0.5:
            response = "SWITCH", 0
        else:
            response = "ATTACK", 0

        return response

    def switch_faint(self):
        """
        Choose switch-in after pokemon has fainted.
        
        For now pick next pokemon in lineup.
        """
        return 0