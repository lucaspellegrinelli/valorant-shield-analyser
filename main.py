import logging

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from api import APIRequester
from scrapper import ShieldMatter, scrap_data

logging.basicConfig(level=logging.INFO)


def main():
    api = APIRequester("cache")

    players = [
        ("Dias Toffoli", "STF0", "br"),
        ("Cármen Lúcia", "STF0", "br"),
        ("DCS", "DCSTv", "br"),
        ("Lewandowski", "STF", "br"),
        ("Gilmar Mendes", "SFT", "br"),
        ("Noirum", "BR1", "br"),
    ]

    for name, tag, region in players:
        df = scrap_data(name, tag, region, api)
        df = df[df["armor"] == "Heavy Shields"]

        maybe_mattered = df[(df["mattered"] == ShieldMatter.MAYBE)]
        yes_mattered = df[df["mattered"] == ShieldMatter.YES]

        yes_prob = len(yes_mattered) / len(df) * 100
        maybe_prob = len(maybe_mattered) / len(df) * 100

        print(f"{name}#{tag}")
        print(f" - Total importou:\t\t{(yes_prob + maybe_prob):.2f}%")
        print(f"   - Talvez importou:\t\t{maybe_prob:.2f}%")
        print(f"   - Definitivamente importou:\t{yes_prob:.2f}%")
        print("")


if __name__ == "__main__":
    main()
