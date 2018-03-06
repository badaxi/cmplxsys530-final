"""Test for pokemon module."""

from pokemon.pokemon import Pokemon


def test_init():
    """Test that the initialization runs well with no errors."""
    Pokemon("spinda", ["tackle"], level=50)


def test_param_validation():
    """Test that parameter validation."""
    pokemon_validation()
    move_validation()
    nature_validation()
    level_validation()
    ev_validation()


def move_validation():
    """Validate the moves provided."""
    # Invalid moves provided
    try:
        Pokemon("exploud", ["doot"], level=100)
        assert False
    except AttributeError:
        pass

    # No moves provided
    try:
        Pokemon("exploud", [], level=100)
        assert False
    except AttributeError:
        pass


def nature_validation():
    """Validate nature properly handled."""
    # Invalid nature
    try:
        Pokemon("exploud", ["tackle"], nature="doot")
        assert False
    except AttributeError:
        pass


def level_validation():
    """Validate proper handling of invalid levels."""
    # Level less than threshold
    try:
        Pokemon("exploud", ["tackle"], level=-1)
        assert False
    except AttributeError:
        pass

    # Level greater than threshold
    try:
        Pokemon("exploud", ["tackle"], level=500)
        assert False
    except AttributeError:
        pass

    # Level is decimal
    try:
        Pokemon("exploud", ["tackle"], level=50.5)
        assert False
    except AttributeError:
        pass


def pokemon_validation():
    """Validate pokemon choice."""
    # Invalid pokemon choice
    try:
        Pokemon("doot", ["tackle"], level=100)
        assert False
    except AttributeError:
        pass


def ev_validation():
    """Validate provided EVs"""
    # Negative EVs
    try:
        evs = {"hp": -1, "atk": 1}
        Pokemon("exploud", ["tackle"], evs=evs)
        assert False
    except AttributeError:
        pass

    # Too many EVs
    try:
        evs = {"hp": 500, "atk": 1}
        Pokemon("exploud", ["tackle"], evs=evs)
        assert False
    except AttributeError:
        pass

    # Decimal EVs
    try:
        evs = {"hp": 500.5, "atk": 1}
        Pokemon("exploud", ["tackle"], evs=evs)
        assert False
    except AttributeError:
        pass


def test_stats_calculation():
    """Test that stats are calculated properly with and without natures."""
    pkmn1 = Pokemon("spinda", ["tackle"], level=50)
    assert pkmn1.max_hp == 135
    assert pkmn1.attack == 80
    assert pkmn1.defense == 80
    assert pkmn1.sp_attack == 80
    assert pkmn1.sp_defense == 80
    assert pkmn1.speed == 80

    pkmn2 = Pokemon("spinda", ["tackle"], level=50, nature="adamant")
    assert pkmn2.max_hp == 135
    assert pkmn2.attack == 88
    assert pkmn2.defense == 80
    assert pkmn2.sp_attack == 72
    assert pkmn2.sp_defense == 80
    assert pkmn2.speed == 80

    evs = {}
    evs["atk"] = 252
    evs["spe"] = 56
    evs["spa"] = 56
    evs["hp"] = 128
    pkmn3 = Pokemon("spinda", ["tackle"], level=50, nature="adamant", evs=evs)
    assert pkmn3.max_hp == 151
    assert pkmn3.attack == 123
    assert pkmn3.defense == 80
    assert pkmn3.sp_attack == 78
    assert pkmn3.sp_defense == 80
    assert pkmn3.speed == 87


test_init()
test_param_validation()
test_stats_calculation()