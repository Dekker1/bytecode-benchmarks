#!/usr/bin/env python3

import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

sns.set(font_scale=1.6, style="whitegrid", font="IBM Plex Sans")

data = "timecmp.csv"
df = pd.read_csv(data, index_col=0)

f, ax = plt.subplots(figsize=(7, 7))
ax.set(xlim=(0.90, 100000), ylim=(0.90, 100000), xscale="log", yscale="log")

# ax.yaxis.set_major_formatter(ticker.EngFormatter())

sns.scatterplot(
    x="MiniZinc 2.5.5",
    y="Prototype Implementation",
    data=df,
    ax=ax,
    # hue="problem",
    # style="problem",
    legend=False,
)
plt.plot([0, 100000], [0, 100000], linewidth=2)

plt.savefig("timecmp.pdf")
