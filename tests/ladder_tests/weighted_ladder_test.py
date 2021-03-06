"""Script to test functioning of ladder."""

from agent.base_agent import BaseAgent
from ladder.weighted_ladder import WeightedLadder
from battle_engine.coinflip import CoinFlipEngine


def test_match_func():
    """Test the match_func to make sure it works."""
    # Set up variables
    lad = WeightedLadder()
    ba1 = BaseAgent(id_in="Ba1")
    ba2 = BaseAgent(id_in="Ba2")

    # Make the elo score higher
    ba1.elo = 1500
    ba2.elo = 1400

    # Add the higher ranked players
    lad.add_player(ba1)
    lad.add_player(ba2)

    # Add the rest of the agents (ranked lower)
    for i in range(3, 11):
        lad.add_player(BaseAgent(id_in="Ba{}".format(i)))

    # Try matching the higher ranked players together
    match1, match2 = lad.match_players()
    while (match1.id is not ba1.id) and (match1.id is not ba2.id):
        match1, match2 = lad.match_players()

    # Higher elo players got matched together
    assert (match2.id == ba1.id or match2.id == ba2.id)


def test_match_basic():
    """Test that match functions properly."""
    # Set up variables
    lad = WeightedLadder()
    ba1 = BaseAgent()
    ba2 = BaseAgent()

    # Add the players to the ladder
    lad.add_player(ba1)
    lad.add_player(ba2)

    # Generate a match (should be ba1 and ba2)
    _ = lad.match_players()

    # Assert that players get removed from ladder
    assert not lad.player_pool
    assert lad.num_turns == 1


def test_run_game():
    """Test run_game functions properly."""
    # Set up variables
    ba1 = BaseAgent()
    ba2 = BaseAgent()
    cfe = CoinFlipEngine()
    lad = WeightedLadder(game=cfe)

    # Add players to the ladder
    lad.add_player(ba1)
    lad.add_player(ba2)

    # Run the game
    lad.run_game()

    # Check that the ladder updated properly
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


def test_get_players_sorted():
    """Run get_players with sorted flag to true."""
    # Set up variables
    ba1 = BaseAgent()
    ba2 = BaseAgent()
    cfe = CoinFlipEngine()
    lad = WeightedLadder(cfe)

    # Add players to the ladder
    lad.add_player(ba1)
    lad.add_player(ba2)

    # Run the game
    lad.run_game()

    # Check that the results are sorted in ascending elo
    players = lad.get_players(sort=True)

    player1 = players[0]
    player2 = players[1]

    assert player1.elo > player2.elo
    assert (player1.num_wins == 1 and player2.num_wins == 0)
    assert (player1.num_losses == 0 and player2.num_losses == 1)


test_match_basic()
test_match_func()
test_run_game()
test_get_players_sorted()
