import enum
from itertools import permutations

import pandas as pd

from api import APIRequester


class ShieldMatter(enum.Enum):
    YES = 1
    NO = 2
    MAYBE = 3


def scrap_data(
    player_name: str, player_tag: str, player_region: str, api: APIRequester
):
    matches = api.get_matches(player_name, player_tag, player_region)
    player_display_name = player_name + "#" + player_tag

    all_data = []
    for match_i, match in enumerate(matches["data"]):
        for round_i, round in enumerate(match["rounds"]):
            armor_bought = "None"
            damage_instances = []

            for player in round["player_stats"]:
                if player["player_display_name"] == player_display_name:
                    armor_bought = player["economy"]["armor"]["name"]

                for damage_event in player["damage_events"]:
                    if damage_event["receiver_display_name"] == player_display_name:
                        damage_instances.append(damage_event["damage"])

            all_data.append(
                {
                    "player": player_display_name,
                    "match": match_i,
                    "round": round_i,
                    "armor": armor_bought,
                    "mattered": did_shield_matter(damage_instances),
                }
            )

    return pd.DataFrame(all_data)


def did_shield_matter(damage_events: list[int]):
    if sum(damage_events) >= 125 and sum(damage_events) < 150:
        return ShieldMatter.YES

    for comb in permutations(damage_events):
        curr_sum = 0
        for damage in comb:
            curr_sum += damage
            if curr_sum >= 125 and curr_sum < 150:
                return ShieldMatter.MAYBE

    return ShieldMatter.NO
