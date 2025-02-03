from src.api.open_api import OpenApi
from data.models.models import Team, TeamIdentifier
from data.config import CURRENT_MAP_POOL_LABELS
from src.conversions.conversions import (
    get_map_info_for_user,
    get_teams_from_match_obj,
    calculate_average_winrate_for_team_per_map,
    calculate_win_probability,
)


class Runner:
    def __init__(self, api_key: str, match_id: str):
        self.client = OpenApi(api_key=api_key)
        self.api_key = api_key
        self.match_id = match_id

    async def get_match_obj(self):
        print(f"Getting match details - id {self.match_id}...")
        res = await self.client.get_match_details(match_id=self.match_id)
        if isinstance(res, dict):
            return res

    @staticmethod
    def get_teams(match_obj: dict) -> list[Team]:
        print("Getting teams from the match...")
        return get_teams_from_match_obj(match_obj=match_obj)

    async def get_team_map_stats(self, team: Team):
        print(f"Getting map stats for each player in {team.name}...")
        team_stats = dict()

        for player in team.players:
            player_stats = await self.client.get_player_stats(player_id=player.id)
            map_info = get_map_info_for_user(user=player, user_map_info=player_stats)
            team_stats |= map_info

        return team_stats

    @staticmethod
    def calculate_avg_wr(team: Team, team_stats: dict):
        print(f"Calculating average winrate stats for {team.name}...")
        return calculate_average_winrate_for_team_per_map(
            team=team, individual_map_stats=team_stats
        )

    async def run(self):
        print("Starting...")
        wp_dict = dict()

        match_obj = await self.get_match_obj()
        teams = self.get_teams(match_obj=match_obj)
        team1, team2 = teams

        if team1.team_identifier == TeamIdentifier.Ally:
            my_team = team1
            enemy_team = team2
        else:
            enemy_team = team1
            my_team = team2

        my_team_map_stats = await self.get_team_map_stats(team=my_team)
        enemy_team_map_stats = await self.get_team_map_stats(team=enemy_team)
        print("Comparing winrates and getting win probabilities for each map...")

        my_team_average = self.calculate_avg_wr(
            team=my_team, team_stats=my_team_map_stats
        )
        enemy_team_average = self.calculate_avg_wr(
            team=enemy_team, team_stats=enemy_team_map_stats
        )

        for map in CURRENT_MAP_POOL_LABELS:
            my_wr = my_team_average[map]
            enemy_wr = enemy_team_average[map]
            res = calculate_win_probability(my_wr=my_wr, enemy_wr=enemy_wr)
            wp_dict |= {map: str(res) + "%"}

        print("Final results:\n")

        maps_wrs = list(wp_dict.items())
        return maps_wrs
