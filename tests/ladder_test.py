""" Script to test functioning of ladder """

from agent.base_agent import Base_Agent
from ladder.ladder import Ladder
from battle_engine.coinflip import CoinFlipEngine

def test_add():
    """ Basic test for ladder add_player method """
    lad = Ladder()
    ba1 = Base_Agent()
    ba2 = Base_Agent()

    lad.add_player(ba1)
    lad.add_player(ba2)

    assert(len(lad.player_pool) == 2)


def test_no_duplicates():
    """ Test that same player cannot exist twice on ladder """
    lad = Ladder()
    ba1 = Base_Agent()
    lad.add_player(ba1)

    try:
        lad.add_player(ba1)
    except ValueError:
        # Ladder throws a ValueError if a duplicate player exists
        # We want to be here
        return

    assert(False)


def test_match():
    """ Test that match functions properly """
    lad = Ladder()
    ba1 = Base_Agent()
    ba2 = Base_Agent()

    lad.add_player(ba1)
    lad.add_player(ba2)

    player, opponent = lad.match_players()

    # Assert that players get removed from ladder
    assert(len(lad.player_pool) == 0)
    assert(lad.num_turns == 1)

def test_run_game():
    """ Test run_game functions properly """
    lad = Ladder()
    ba1 = Base_Agent()
    ba2 = Base_Agent()

    lad.add_player(ba1)
    lad.add_player(ba2)

    cfe = CoinFlipEngine()

    lad.run_game(cfe)

    players = lad.get_players()

    player1 = players[0]
    player2 = players[1]

    # Only one elo value changes
    assert((player1.elo > 1000 and player2.elo == 1000) or
         (player1.elo == 1000 and player2.elo > 1000))

    # Someone won the game
    assert((player1.num_wins == 0 and player2.num_wins == 1) or
         (player1.num_wins == 1 and player2.num_wins == 0))

    # Someone lost the game
    assert((player1.num_losses == 0 and player2.num_losses == 1) or
         (player1.num_losses == 1 and player2.num_losses == 0))

test_add()
test_no_duplicates()
test_match()
test_run_game()