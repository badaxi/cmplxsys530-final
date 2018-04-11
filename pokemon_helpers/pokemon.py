"""Class for a pokemon used by a PokemonAgent."""

from math import floor

from config import MOVE_DATA
from config import POKEMON_DATA
from config import NATURES

from pokemon_helpers.calculate import calculate_hp_stat
from pokemon_helpers.calculate import calculate_stat


class Pokemon:
    """The pokemon class."""

    # pylint: disable=too-many-instance-attributes
    # Packaging values as a dictionary is kind of pointless
    def __init__(self, **kwargs):
        """
        Initialize a pokemon.

        Make a new instance of species <name> with moves <moves>
        at level <level> with nature <quirky>

        :param name: str
            String corresponding to value in config.POKEMON_DATA
        :param moves: list
            List of moves corresponding to moves in config.MOVE_DATA
        :param level: int
            Level of pokemon to be used in calculations
        :param nature: str
            Pokemon nature to be used to modify stat values.
        :param evs: dict
            Dictionary of key/value pairs with EVs for each stat.
            Key should be stat code, value should be number of EVs.
        """
        name = kwargs["name"]
        moves = kwargs["moves"]
        level = kwargs.get("level", 100)
        nature = kwargs.get("nature", "quirky")
        evs = kwargs.get("evs", {})

        # Validate pokemon chosen
        if name not in POKEMON_DATA:
            raise AttributeError("Invalid pokemon chosen: {}.".format(name))

        # Validate moves
        if not moves:
            raise AttributeError("Moves must be provided.")
        for move in moves:
            if move not in MOVE_DATA:
                raise AttributeError("Invalid move chosen: {}.".format(move))

        # Validate level
        if level not in range(1, 101):
            raise AttributeError("Level must be between 1 and 100")

        # Validate nature
        if nature not in NATURES:
            raise AttributeError("Invalid nature chosen: {}".format(nature))

        # Validate EVs
        for stat in evs:
            if evs[stat] < 0:
                raise AttributeError("EVs cannot be less than 0.")
            if evs[stat] > 255:
                raise AttributeError("EVs cannot exceed 255.")
            if not isinstance(evs[stat], int):
                raise AttributeError("EVs must be integer values.")

        self.name = name
        self.level = level
        self.moves = []
        for move in moves:
            self.moves.append(MOVE_DATA[move])
        self.types = POKEMON_DATA[self.name]["types"]
        self.base_stats = POKEMON_DATA[self.name]["baseStats"]
        self.evs = evs
        self.increase_stat = None
        self.set_stats(nature, evs)
        self.boosts = default_boosts()

    def set_stats(self, nature, evs):
        """
        Calculate stats for the pokemon.

        :param nature: str
            Nature of the pokemon to modify stats.
        """
        base_stats = self.base_stats

        # Calculate the statistic values
        self.max_hp = calculate_hp_stat(
            base_stats["hp"], evs.get("hp", 0), self.level)
        self.current_hp = self.max_hp
        self.attack = calculate_stat(
            base_stats["atk"], evs.get("atk", 0), self.level)
        self.defense = calculate_stat(
            base_stats["def"], evs.get("def", 0), self.level)
        self.sp_attack = calculate_stat(
            base_stats["spa"], evs.get("spa", 0), self.level)
        self.sp_defense = calculate_stat(
            base_stats["spd"], evs.get("spd", 0), self.level)
        self.speed = calculate_stat(
            base_stats["spe"], evs.get("spe", 0), self.level)

        # Update with nature modifiers
        if NATURES[nature]["increase"] is not None:
            increase_stat = NATURES[nature]["increase"]
            decrease_stat = NATURES[nature]["decrease"]
            mod_inc = floor(self.__getattribute__(increase_stat)*1.1)
            mod_dec = floor(self.__getattribute__(decrease_stat)*0.9)
            self.increase_stat = increase_stat
            self.__setattr__(increase_stat, mod_inc)
            self.__setattr__(decrease_stat, mod_dec)

    def effective_stat(self, stat):
        """Calculate this pokemon's effective stat after boosts."""
        if stat == "atk":
            stat_name = "attack"
        elif stat == "def":
            stat_name = "defense"
        elif stat == "spa":
            stat_name = "sp_attack"
        elif stat == "spd":
            stat_name = "sp_defense"
        elif stat == "spe":
            stat_name = "speed"

        val = self[stat_name]
        boost = self.boosts[stat]
        if boost > 0:
            val = val*(2+boost)/2
        elif boost < 0:
            val = val*(2/(2-boost))

        # Round down
        val = floor(val)

        return val

    def __getitem__(self, key):
        """
        Define [] operating on this object.

        :param key: str
            Attribute of this object to get.
        """
        if key == "baseStats":
            key = "base_stats"
        return self.__getattribute__(key)

    def __contains__(self, key):
        """
        Define 'in' operator on this object.

        :param key: str
            Attribute to check this object for.
        """
        try:
            self.__getattribute__(key)
        except AttributeError:
            return False

        return True

def default_boosts():
    """Generate dictionary with default boost levels."""
    boost_dict = {}
    boost_dict["atk"] = 0
    boost_dict["def"] = 0
    boost_dict["spa"] = 0
    boost_dict["spd"] = 0
    boost_dict["spe"] = 0

    return boost_dict

def default_team_spinda():
    """Generate a Spinda for these players."""
    return [Pokemon(name="spinda", moves=["return", "shadowball", "tackle", "icebeam"])]


def default_team_floatzel():
    """Generate a FLoatzel for the player."""
    return [Pokemon(name="floatzel", moves=["watergun", "tackle", "liquidation", "icebeam"])]


def default_team_ivysaur():
    """Generate an Ivysaur for these players."""
    return [Pokemon(name="ivysaur", moves=["seedbomb", "tackle", "icebeam", "swordsdance"])]
