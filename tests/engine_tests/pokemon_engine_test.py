"""Unit tests for pokemon engine."""

from agent.pokemon_agent import PokemonAgent
from pokemon.pokemon import Pokemon
from battle_engine.pokemon_engine import PokemonEngine


def test_run():
    """Test running of a pokemon game."""
    exploud = Pokemon("exploud", ["tackle"])
    floatzel = Pokemon("floatzel", ["watergun"])

    player1 = PokemonAgent([exploud])
    player2 = PokemonAgent([floatzel])

    p_eng = PokemonEngine()

    outcome = p_eng.run(player1, player2)
    assert outcome == 1
    assert p_eng.game_state["player1"]["active"] is not None
    assert not p_eng.game_state["player1"]["team"]
    assert p_eng.game_state["player2"]["active"] is None
    assert not p_eng.game_state["player2"]["team"]


def test_run_multiple_pokemon():
    """Test running a game with multiple pokemon."""
    exploud = Pokemon("exploud", ["tackle"], level=90)
    spinda1 = Pokemon("spinda", ["watergun"])
    spinda2 = Pokemon("spinda", ["tackle"])
    magikarp = Pokemon("magikarp", ["thundershock"])

    player1 = PokemonAgent([exploud])
    player2 = PokemonAgent([spinda1, spinda2, magikarp])

    p_eng = PokemonEngine()

    p_eng.run(player1, player2)
    assert p_eng.game_state["player1"]["active"] is not None
    assert p_eng.game_state["player2"]["active"] is None
    assert not p_eng.game_state["player2"]["team"]

    assert len(player1.opp_gamestate["moves"]["magikarp"]) == 1
    assert player1.opp_gamestate["moves"]["magikarp"][0]["name"] == "Thunder Shock"
    assert len(player1.opp_gamestate["moves"]["spinda"]) == 2


def test_run_multiple_moves():
    """Test running a game with multiple moves."""
    exploud = Pokemon("exploud", ["shadowball"])
    spinda = Pokemon("spinda", ["watergun", "tackle", "thundershock"])

    player1 = PokemonAgent([exploud])
    player2 = PokemonAgent([spinda])

    p_eng = PokemonEngine()
    p_eng.run(player1, player2)


def test_run_infinite():
    """Test running a game where it'll go on forever."""
    exploud1 = Pokemon("exploud", ["shadowball"])
    exploud2 = Pokemon("exploud", ["shadowball"])

    player1 = PokemonAgent([exploud1])
    player2 = PokemonAgent([exploud2])

    p_eng = PokemonEngine()
    p_eng.run(player1, player2)
    # We got to the turn limit
    assert p_eng.game_state["num_turns"] > p_eng.turn_limit


test_run()
test_run_multiple_moves()
test_run_multiple_pokemon()
test_run_infinite()