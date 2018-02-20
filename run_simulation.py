"""Script to run a ladder simulation."""
import click

from simulation.cf_simulation import CFSimulation
from simulation.rps_simulation import RPSSimulation
from simulation.multiturn_rps_simulation import MTRPSSimulation

@click.command()
@click.option("-nr",
              "--num_runs",
              default=5000,
              help="Number of games to simulate. Default is 5000")
@click.option("-np",
              "--num_players",
              default=10,
              help="Number of agents. Default is 10")
@click.option("-g",
              "--game_choice",
              help="Which game to play. Options are\n \
              [0] Coin Flip\n \
              [1] Balanced Population Rock Paper Scissors\n \
              [2] Skewed Population Rock Paper Scissors\n \
              [3] Multi-Turn Rock Paper Scissors")
@click.option("-p",
              "--proportions",
              nargs=4,
              default=(0.25, 0.25, 0.25, 0.25),
              help="Proportions for skewed RPS tournament. Default is uniform.")
@click.option("-dd",
              "--data_delay",
              default=10,
              help="Number of iterations between gathering data. Default is 10.")
@click.option("-l",
              "--ladder",
              default=0,
              help="Which ladder matching to use. Options are \n[0] Weighted (default)\n[1] Random")
def run(**kwargs):
    """Run the simulation."""
    num_runs = kwargs.get("num_runs", None)
    num_players = kwargs.get("num_players", None)
    game_choice = kwargs.get("game_choice", None)
    if game_choice is None:
        raise RuntimeError("No Game Selected")
    game_choice = int(game_choice)
    proportions = kwargs.get("proportions", None)
    data_delay = kwargs.get("data_delay", None)
    ladder_choice = int(kwargs.get("ladder", None))
    num_rounds = kwargs.get("num_rounds", None)

    if game_choice == 0:
        cf_sim = CFSimulation(num_runs=num_runs,
                              num_players=num_players,
                              ladder_choice=ladder_choice)
        cf_sim.run()
    elif game_choice == 1:
        rps_sim = RPSSimulation(num_runs=num_runs,
                                num_rounds=1,
                                num_players=num_players,
                                proportions=(0.25, 0.25, 0.25, 0.25),
                                data_delay=data_delay,
                                ladder_choice=ladder_choice)
        rps_sim.add_agents()
        rps_sim.init_type_log_writer()
        rps_sim.run()
    elif game_choice == 2:
        rps_sim = RPSSimulation(num_runs=num_runs,
                                num_rounds=1,
                                num_players=num_players,
                                proportions=proportions,
                                data_delay=data_delay,
                                ladder_choice=ladder_choice)
        rps_sim.add_agents()
        rps_sim.init_type_log_writer()
        rps_sim.run()
    elif game_choice == 3:
        mtrps_sim = MTRPSSimulation(num_runs=num_runs,
                                    num_rounds=num_rounds,
                                    num_players=num_players,
                                    ladder_choice=ladder_choice,
                                    data_delay=data_delay)
        mtrps_sim.add_agents()
        mtrps_sim.init_type_log_writer()
        mtrps_sim.run()
    else:
        raise RuntimeError("Invalid Game Choice")


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    run()
