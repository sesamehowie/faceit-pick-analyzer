from data.config import CURRENT_MAP_POOL_LABELS, MY_PLAYER_ID
from data.models.models import TeamIdentifier, Map, User, Team


def get_teams_from_match_obj(match_obj: dict) -> list[Team]:
    factions = ["faction1", "faction2"]

    teams = []

    for faction in factions:
        team_identifier = TeamIdentifier.Unset
        players = []

        for player_obj in match_obj["teams"][faction]["roster"]:
            player_id = player_obj["player_id"]
            player_name = player_obj["nickname"]
            if player_id == MY_PLAYER_ID:
                team_identifier = TeamIdentifier.Ally
                team_name = "My team"
            players.append(User(id=player_id, faceit_name=player_name))
        if team_identifier == TeamIdentifier.Unset:
            team_identifier = TeamIdentifier.Enemy
            team_name = "Enemy team"

        teams.append(
            Team(name=team_name, team_identifier=team_identifier, players=players)
        )

    return teams


def get_map_info_for_user(user: User, user_map_info: dict) -> User:
    maps_info = dict()

    for map in user_map_info["segments"]:
        if (
            map["type"] == "Map"
            and map["mode"] == "5v5"
            and map["label"] in CURRENT_MAP_POOL_LABELS
        ):

            win_rate = int(map["stats"]["Win Rate %"])
            label = map["label"]

            map = Map(label=label, win_rate_percentage=win_rate)
            maps_info[map.label] = map.win_rate_percentage

    return {user.faceit_name: maps_info}


def calculate_average_winrate_for_team_per_map(team: Team, individual_map_stats: dict):
    team_player_amt = 5
    avg_wr_per_map = dict()

    for map in CURRENT_MAP_POOL_LABELS:
        total = 0
        for player in team.players:
            total += individual_map_stats[player.faceit_name][map]
        avg_wr = round(total / team_player_amt, 2)
        avg_wr_per_map[map] = avg_wr

    return avg_wr_per_map


def calculate_win_probability(my_wr: float | int, enemy_wr: float | int) -> float:
    # Bradley-Terry model
    prob_my_win = my_wr / (my_wr + enemy_wr)
    return round(prob_my_win * 100, 2)
