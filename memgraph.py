#!/usr/bin/env python3

import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

sns.set(font_scale=1.6, style="whitegrid", font="IBM Plex Sans")

data = "memcmp.csv"
df = pd.read_csv(data, index_col=0)

f, ax = plt.subplots(figsize=(7, 7))
ax.set(xlim=(7500, 300000), ylim=(7500, 300000), xscale="log", yscale="log")

sns.scatterplot(
    x="MiniZinc 2.5.5",
    y="Prototype Implementation",
    data=df,
    ax=ax,
    # hue="problem",
    # style="problem",
    legend=False,
)
plt.plot([0, 1000000], [0, 1000000], linewidth=2)

plt.savefig("memcmp.pdf")
