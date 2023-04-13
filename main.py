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

        maybe_mattered_light = df[(df["mattered_light"] == ShieldMatter.MAYBE)]
        yes_mattered_light = df[df["mattered_light"] == ShieldMatter.YES]

        maybe_mattered_no = df[(df["mattered_no"] == ShieldMatter.MAYBE)]
        yes_mattered_no = df[df["mattered_no"] == ShieldMatter.YES]

        yes_prob_light = len(yes_mattered_light) / len(df) * 100
        maybe_prob_light = len(maybe_mattered_light) / len(df) * 100

        yes_prob_no = len(yes_mattered_no) / len(df) * 100
        maybe_prob_no = len(maybe_mattered_no) / len(df) * 100

        light_prob = 100 - (yes_prob_light + maybe_prob_light)
        no_prob = 100 - (yes_prob_no + maybe_prob_no)

        print(f"{name}#{tag}")
        print(f" - Número de rounds com escudo cheio: {len(df)}")
        print(
            f" - {light_prob:.2f}% dos rounds o escudo leve teria o mesmo efeito do cheio"
        )
        print(
            f" - {no_prob:.2f}% dos rounds ficar sem escudo não teria feito diferença"
        )
        print("")


if __name__ == "__main__":
    main()
