"""Script to run a ladder simulation for Rock Paper Scissors."""

from math import ceil

from battle_engine.rockpaperscissors import RPSEngine
from agent.rps_agent import RPSAgent
from ladder.weighted_ladder import WeightedLadder
from ladder.random_ladder import RandomLadder
from stats.calc import calculate_avg_elo
# from stats.plot import plot_group_ratings
from log_manager.log_writer import LogWriter

LADDER_CHOICES = [
    WeightedLadder,
    RandomLadder
]


def run(**kwargs):
    """
    Run a Rock/Paper/Scissors simulation.

    :param num_runs: int
        Total number of games to simulate
    :param num_players: int
        Approximate number of players to have on the ladder
    :param proportions: list
        List proportions of Rock, Paper, Scissors, Uniform players
        to have on the ladder.
    :param data_delay: int
        How often to record the elo rankings of the players for graphing
    """
    num_runs = kwargs["num_runs"]
    num_players = kwargs["num_players"]
    proportions = kwargs["proportions"]
    data_delay = kwargs["data_delay"]

    game = RPSEngine()
    lad = LADDER_CHOICES[kwargs["ladder_choice"]](game)
    player_log_writer = init_player_log_writer()
    type_log_writer = init_type_log_writer(proportions)

    add_agents(lad, num_players, proportions)

    for game_ind in range(num_runs):
        outcome, player1, player2 = lad.run_game()

        datum = {
            "player1.type": player1.type,
            "player1.elo": player1.elo,
            "player2.type": player2.type,
            "player2.elo": player2.elo,
            "outcome": outcome
        }
        player_log_writer.write_line(datum)

        if game_ind % data_delay == 0:
            # Calculate the average ranking statistics
            # every <data_delay> iterations
            current_stats = calculate_avg_elo(lad)
            type_log_writer.write_line(current_stats)


def add_agents(lad, num_players, proportions):
    """Add agents in specified proportions to ladder."""
    num_rock = ceil(float(proportions[0])*num_players)
    num_paper = ceil(float(proportions[1])*num_players)
    num_scissors = ceil(float(proportions[2])*num_players)
    num_mixed = ceil(float(proportions[3])*num_players)

    for rock_ind in range(num_rock):
        agent_id = 'rock_{}'.format(rock_ind)
        player = RPSAgent(id_in=agent_id, strategy_in='rock')
        lad.add_player(player)

    for paper_ind in range(num_paper):
        agent_id = 'paper_{}'.format(paper_ind)
        player = RPSAgent(id_in=agent_id, strategy_in='paper')
        lad.add_player(player)

    for sciss_ind in range(num_scissors):
        agent_id = 'scissors_{}'.format(sciss_ind)
        player = RPSAgent(id_in=agent_id, strategy_in='scissors')
        lad.add_player(player)

    for mixed_ind in range(num_mixed):
        agent_id = 'mixed_{}'.format(mixed_ind)
        player = RPSAgent(id_in=agent_id)
        lad.add_player(player)


def init_player_log_writer():
    """Initialize player data LogWriter."""
    header = []
    header.append("player1.type")
    header.append("player1.elo")
    header.append("player2.type")
    header.append("player2.elo")
    header.append("outcome")

    log_writer = LogWriter(header, prefix="RPSPlayers")
    return log_writer


def init_type_log_writer(proportions):
    """Initialize Type Average Elo LogWriter."""
    header = []
    if proportions[0] != 0:
        header.append("rock")
    if proportions[1] != 0:
        header.append("paper")
    if proportions[2] != 0:
        header.append("scissors")
    if proportions[3] != 0:
        header.append("uniform")

    log_writer = LogWriter(header, prefix="RPSTypes")
    return log_writer
