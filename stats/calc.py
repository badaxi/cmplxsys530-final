""" Package to calculate interesting ladder metrics """

def calculate_avg_elo(ladder, group_strategy = True):
    """ 
    Calculate the elo rankings on a ladder at a specific point in time

    :param ladder: The ladder for which to calculate the rankings
    :param group_strategy: Whether to group results by strategy or by individuals
    """
    player_pool = ladder.get_players()
    output = {}

    for player in player_pool:
        if group_strategy and hasattr(player, 'strategy'):
            player_strat = str(player.strategy)
            if player_strat not in output:
                output[player_strat] = []
            output[player_strat].append(player.elo)
        else:
            player_id = str(player.id)
            if player_id not in output:
                output[player_id] = []
            output[player_id].append(player.elo)

    for group in output:
        output[group] = sum(output[group])/len(output[group])
    
    return output