import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.patches as mpatches
from matplotlib.ticker import FuncFormatter
import os
from matplotlib.ticker import MultipleLocator


# print(plt.style.available)

plt.style.use("latex-sans")
plt.rcParams["xtick.labelsize"] = 12
plt.rcParams["ytick.labelsize"] = 12
plt.rcParams["hatch.linewidth"] = 0.5
plt.rcParams["axes.axisbelow"]


"""
    SET SCRIPT INPUTS HERE
"""

# _file_name = "20240227_2219_RQ1xxDiverse_On+Stockpiling_On_2040"

_colors = {
    "Recycling": "#78A083",
    "North America": "#ED7B7B",
    "Zimbabwe": "#3085C3",
    "Russia": "purple",
    "World": "#D6D46D",
    # "Recycling_low": "#04364A",
}


def format_x_ticks(value, _):
    return f"{int(value)}"


def function5(file_name=None, output_name=None):
    fig, ax = plt.subplots(figsize=(6 * 1.05, 4 * 1.05))
    _data = pd.read_excel(file_name + "/M1_overview.xlsx")

    _target_year = max(_data.Year)
    _years_x = np.arange(2025, _target_year + 1, 1)

    _ratio = []

    for _index, _row in _data.iterrows():
        _ratio.append(_row["Stock_stored|"] / _row.Demand)

    ax.bar(
        _years_x, _ratio, color="#607274", linewidth=0.5, zorder=10, edgecolor="black"
    )

    # ax.fill_between(_years_x, _ratio, len(_years_x) * [0], color='#FFD23F')

    ax.grid(
        which="major",
        axis="y",
        color="#758D99",
        alpha=0.4,
        zorder=-1000,
        linestyle="dashed",
    )

    ax.xaxis.set_major_formatter(FuncFormatter(format_x_ticks))
    major_locator = MultipleLocator(5)
    ax.xaxis.set_major_locator(major_locator)
    minor_locator = MultipleLocator(1)
    ax.xaxis.set_minor_locator(minor_locator)

    ax.set_xlabel("Year", fontsize=12)
    ax.set_ylim([0, 2.3])

    _offset = ax.get_ylim()[1] * 0.025
    for _i, _value in enumerate(_ratio):
        _value = np.around(_value, 2)
        if _value != 0:
            ax.text(
                _i + 2025,
                _value + _offset,
                "(" + str(_value) + ")",
                ha="center",
                color="black",
                rotation=90,
            )
        else:
            pass

    plt.tight_layout()
    plt.savefig(os.path.join(file_name, output_name))

    return
