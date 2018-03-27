"""Pokemon agent who's moves are determined by maximizing personal gain."""

import operator
from copy import deepcopy

from agent.basic_pokemon_agent import PokemonAgent
from agent.basic_pokemon_agent import calc_opp_position_helper, calc_position_helper
from config import USAGE_STATS


class BasicPlanningPokemonAgent(PokemonAgent):
    """
    Class for PokemonAgent who calculates the next move by maximizing some function.

    This agent will maximize the game_position given the opponent's moves are all
    equally likely.
    """

    def __init__(self, tier, **kwargs):
        """Initialize a player with a specific tier."""
        super().__init__(*kwargs)
        self.tier = tier

    def make_move(self):
        """Choose the move to make."""
        player_opts, opp_opts = self.generate_possibilities()
        move_choice = self.optimal_move(player_opts, opp_opts)
        return move_choice

    def generate_possibilities(self):
        """Generate a two lists of possible player and opponent moves."""
        player_opts = []
        opp_opts = []

        # My possible attacks
        posn = 0
        for _ in self.gamestate["active"].moves:
            player_opts.append(("ATTACK", posn))
            posn += 1

        # My possible switches
        posn = 0
        for _ in self.gamestate["team"]:
            player_opts.append(("SWITCH", posn))
            posn += 1

        # Opponent's possible attacks
        posn = 0
        opp_active_poke = self.opp_gamestate["data"]["active"]["name"]
        opp_moves = []
        if opp_active_poke in self.opp_gamestate["moves"]:
            for move in self.opp_gamestate["moves"][opp_active_poke]:
                opp_moves.append(move)
        if len(opp_moves) < 4:
            common_moves = USAGE_STATS[self.tier][opp_active_poke]["Moves"]
            common_moves = sorted(common_moves.items(),
                                  key=operator.itemgetter(1), reverse=True)
            common_moves = [move[0] for move in common_moves if move[0] != ""]
            for move in common_moves:
                if move not in opp_moves:
                    opp_moves.append(move)
                if len(opp_moves) == 4:
                    break
        for move in opp_moves:
            opp_opts.append(("ATTACK", move))

        # Opponent's possible switches
        posn = 0
        for poke in self.opp_gamestate["data"]["team"]:
            poke_name = poke["name"]
            opp_opts.append(("SWITCH", poke_name))

        return player_opts, opp_opts

    def optimal_move(self, player_opts, opp_opts):
        """Choose the optimal move given the options availible."""
        optimal_opt = None
        maximal_position = -1
        for p_opt in player_opts:
            total_position = 0
            for o_opt in opp_opts:
                my_gs = deepcopy(self.gamestate)
                opp_gs = deepcopy(self.opp_gamestate)
                print(p_opt, o_opt)

                my_posn = calc_position_helper(my_gs)
                opp_posn = calc_opp_position_helper(opp_gs)
                total_position += my_posn / opp_posn

            total_position = total_position / len(opp_opts)
            if total_position > maximal_position:
                optimal_opt = p_opt
                maximal_position = total_position

        return optimal_opt
