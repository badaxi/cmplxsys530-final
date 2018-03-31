"""Pokemon agent who's moves are determined by maximizing personal gain."""

import operator
from copy import deepcopy

from agent.basic_pokemon_agent import PokemonAgent
from agent.basic_pokemon_agent import calc_opp_position_helper, calc_position_helper
from config import USAGE_STATS, POKEMON_DATA, MOVE_DATA


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
        for _ in self.opp_gamestate["data"]["team"]:
            opp_opts.append(("SWITCH", posn))
            posn += 1

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

                # Player Switches
                if p_opt[0] == "SWITCH":
                    temp = my_gs["active"]
                    my_gs["active"] = my_gs["team"][p_opt[1]]
                    my_gs["team"].pop(p_opt[1])
                    my_gs["team"].append(temp)

                # Opponent Switches
                if o_opt[0] == "SWITCH":
                    temp = opp_gs["data"]["active"]
                    opp_gs["data"]["active"] = opp_gs["data"]["team"][o_opt[1]]
                    opp_gs["data"]["team"].pop(o_opt[1])
                    opp_gs["data"]["team"].append(temp)

                # Attacking
                dmg_range = None
                if p_opt[0] == "ATTACK" and o_opt[0] == "ATTACK":
                    # Figure out who is faster
                    dmg_range = None
                elif p_opt[0] == "ATTACK":
                    # Only we attack
                    dmg_range = self.attacking_dmg_range(my_gs, opp_gs, p_opt)

                    # Average damage as decimal
                    opp_gs["data"]["active"]["pct_hp"] -= (dmg_range[0] + dmg_range[1]) / 200

                elif o_opt[0] == "ATTACK":
                    dmg_range = self.defending_dmg_range(my_gs, opp_gs, o_opt)
                    # Average damage as portion of total HP
                    my_gs["active"].current_hp -= my_gs["active"].max_hp * \
                                                 (dmg_range[0] + dmg_range[1]) / 200

                my_posn = calc_position_helper(my_gs)
                opp_posn = calc_opp_position_helper(opp_gs)
                total_position += my_posn / opp_posn

            total_position = total_position / len(opp_opts)
            if total_position > maximal_position:
                optimal_opt = p_opt
                maximal_position = total_position

        return optimal_opt

    def attacking_dmg_range(self, my_gs, opp_gs, p_opt):
        """Calculate the (weighted) damage range for an attack."""
        p_poke = my_gs["active"]
        p_move = p_poke.moves[p_opt[1]]
        o_poke_name = opp_gs["data"]["active"]["name"]
        o_poke = POKEMON_DATA[o_poke_name]
        params = self.opp_gamestate["investment"][o_poke_name]

        # We do not handle status moves at this point in time.
        if p_move["category"] == "Status":
            return [0, 0]

        dmg_range = None
        param_combs = atk_param_combinations(p_poke, params, p_move)
        for param_comb in param_combs:
            dmg_val = self.dmg_stat_calc.calculate_range(p_move, p_poke, o_poke, param_comb)
            if not dmg_range:
                dmg_range = [0, 0]

            dmg_range[0] += dmg_val[0]
            dmg_range[1] += dmg_val[1]

        # Each combination is weighted equally
        dmg_range[0] = dmg_range[0] / len(param_combs)
        dmg_range[1] = dmg_range[1] / len(param_combs)

        return dmg_range

    def defending_dmg_range(self, my_gs, opp_gs, o_opt):
        """Calculate the (weighted) damage range when attacked."""
        p_poke = my_gs["active"]
        o_move = MOVE_DATA[o_opt[1]]
        o_poke_name = opp_gs["data"]["active"]["name"]
        o_poke = POKEMON_DATA[o_poke_name]
        params = self.opp_gamestate["investment"][o_poke_name]

        # We do not handle status moves at this point in time.
        if o_move["category"] == "Status":
            return [0, 0]

        dmg_range = None
        param_combs = def_param_combinations(p_poke, params, o_move)

        for param_comb in param_combs:
            dmg_val = self.dmg_stat_calc.calculate_range(o_move, o_poke, p_poke, param_comb)
            if not dmg_range:
                dmg_range = [0, 0]

            dmg_range[0] += dmg_val[0]
            dmg_range[1] += dmg_val[1]

        # Each combination is weighted equally
        dmg_range[0] = dmg_range[0] / len(param_combs)
        dmg_range[1] = dmg_range[1] / len(param_combs)

        return dmg_range

def atk_param_combinations(active_poke, opp_params, move):
    """Calculate possible parameter combinations for when we're attacking."""
    results = []

    # Figure out which stat we should use
    stat = "atk"
    opp_stat = "def"
    if move["category"] == "Special":
        stat = "spa"
        opp_stat = "spd"

    result_dict = {}
    result_dict["atk"] = {}

    if stat in active_poke.evs and active_poke.evs[stat] > 128:
        result_dict["atk"]["max_evs"] = True
    if active_poke.increase_stat == stat:
        result_dict["atk"]["positive_nature"] = True

    for hp_params in opp_params["hp"]:
        for def_params in opp_params[opp_stat]:
            temp_results = deepcopy(result_dict)
            temp_results["hp"] = hp_params
            temp_results["def"] = def_params
            results.append(temp_results)

    return results

def def_param_combinations(active_poke, opp_params, move):
    """Parameter combinations for when we're on the defensive."""
    results = []

    # Figure out which stat we should use
    stat = "def"
    opp_stat = "atk"
    if move["category"] == "Special":
        stat = "spd"
        opp_stat = "spa"

    result_dict = {}
    result_dict["def"] = {}
    result_dict["hp"] = {}

    # Information for Defense Stat
    if stat in active_poke.evs and active_poke.evs[stat] > 128:
        result_dict["def"]["max_evs"] = True
    if active_poke.increase_stat == stat:
        result_dict["def"]["positive_nature"] = True

    # Information for HP Stat
    if "hp" in active_poke.evs and active_poke.evs["hp"] > 128:
        result_dict["hp"]["max_evs"] = True

    for atk_params in opp_params[opp_stat]:
        temp_results = deepcopy(result_dict)
        temp_results["atk"] = atk_params
        results.append(temp_results)

    return results
