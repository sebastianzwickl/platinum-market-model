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

_colors = {
    "Recycling": "#78A083",
    "North America": "#ED7B7B",
    "Zimbabwe": "#3085C3",
    "Russia": "purple",
    "World": "#D6D46D",
}


def format_x_ticks(value, _):
    return f"{int(value)}"


def function1(file_name=None, output_name=None):
    fig, ax = plt.subplots(figsize=(6 * 1.05, 4 * 1.05))
    _data = pd.read_excel(file_name + "/M1_overview.xlsx")
    _filtered = [
        col
        for col in _data.columns
        if any(substring in col for substring in ["Q_Bar", "Year"])
    ]
    _data = _data[_filtered]
    _target_year = max(_data.Year)
    _years_x = np.arange(2025, _target_year + 1, 1)
    for _exp in ["Recycling", "Russia", "Zimbabwe", "North America", "World"]:
        if _exp == "Recycling":
            _val = [
                element1 + element2
                for element1, element2 in zip(
                    _data["Q_Bar|" + _exp + "_low"], _data["Q_Bar|" + _exp + "_high"]
                )
            ]
        else:
            _val = _data["Q_Bar|" + _exp]
        ax.plot(
            _years_x,
            _val,
            label=_exp,
            color=_colors.get(_exp),
            linewidth=2,
            marker="o",
            markersize=0,
            markeredgecolor=_colors.get(_exp),
        )

    ax.xaxis.set_major_formatter(FuncFormatter(format_x_ticks))
    major_locator = MultipleLocator(5)
    ax.xaxis.set_major_locator(major_locator)
    minor_locator = MultipleLocator(1)
    ax.xaxis.set_minor_locator(minor_locator)

    # ax.grid(which="major", axis="x", color="#758D99", alpha=1, zorder=1)
    # ax.grid(which="minor", axis="x", color="#758D99", alpha=0.5, zorder=1)

    ax.grid(
        which="major",
        axis="y",
        color="#758D99",
        alpha=0.4,
        zorder=-1000,
        linestyle="dashed",
    )

    handles, labels = ax.get_legend_handles_labels()

    sorted_labels, sorted_handles = zip(
        *sorted(zip(labels, handles), key=lambda t: t[0])
    )

    _leg = plt.legend(
        handles=sorted_handles,
        labels=sorted_labels,
        facecolor="white",
        fontsize=12,
        handlelength=1.5,
        handletextpad=0.5,
        borderpad=0.5,
        columnspacing=1,
        edgecolor="#444444",
        frameon=True,
        shadow=False,
        ncol=3,
        loc="upper left",
        bbox_to_anchor=(0.025, 0.975),
        framealpha=1,
    )

    _leg.get_frame().set_linewidth(0.5)

    ax.set_ylim([0, 110])

    ax.set_xlabel("Year", fontsize=12)
    ax.set_ylabel("Maximum supply capacity [tons/year]", fontsize=12)

    plt.tight_layout()
    plt.savefig(os.path.join(file_name, output_name))

    return


# plot_q_bar_of_exporter(
# file_name=_file_name,
# output_name="0_fringe_exporter_capacity.pdf"
# )
