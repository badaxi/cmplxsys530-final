""" Script to run a ladder simulation for Rock Paper Scissors """

from math import ceil

from battle_engine.rockpaperscissors import RPSEngine
from agent.rps_agent import RPS_Agent
from ladder.ladder import Ladder
from stats.calc import calculate_avg_elo
from stats.plot import plot_group_ratings

def run(num_runs, num_players, proportions):
    game = RPSEngine()
    lad = Ladder()
    ratings = {}

    prop_rock = float(proportions[0])
    prop_paper = float(proportions[1])
    prop_scissors = float(proportions[2])

    num_rock = ceil(prop_rock*num_players)
    num_paper = ceil(prop_paper*num_players)
    num_scissors = ceil(prop_scissors*num_players)


    for rock_ind in range(num_rock):
        agent_id = 'rock_{}'.format(rock_ind)
        player = RPS_Agent(id_in = agent_id, strategy_in = 'rock')
        lad.add_player(player)

    for paper_ind in range(num_paper):
        agent_id = 'paper_{}'.format(paper_ind)
        player = RPS_Agent(id_in = agent_id, strategy_in = 'paper')
        lad.add_player(player)

    for sciss_ind in range(num_scissors):
        agent_id = 'scissors_{}'.format(sciss_ind)
        player = RPS_Agent(id_in = agent_id, strategy_in = 'scissors')
        lad.add_player(player)

    for game_ind in range(num_runs):
        lad.run_game(game)
        if game_ind % 10 == 0:
            # Calculate the statistics every 10 values
            current_stats = calculate_avg_elo(lad)
            for group in current_stats:
                if group not in ratings:
                    ratings[group] = []
                ratings[group].append(current_stats[group])
    
    players = lad.get_players(sort=True)

    for player in players:
        player.print_info()

    plot_group_ratings(ratings)