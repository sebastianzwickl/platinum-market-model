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

# result_dir = os.path.join("figures", "{}".format(_file_name))
# if not os.path.exists(result_dir):
# os.makedirs(result_dir)


#
#
#
#
#
#
#
#
#


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


def format_y_ticks(value, _):
    return f"{int(value)}\%"


def function4(file_name=None, output_name=None):
    fig, ax = plt.subplots(figsize=(6 * 1.05, 4 * 1.05))
    _data = pd.read_excel(file_name + "/M1_overview.xlsx")
    _filtered = [
        col
        for col in _data.columns
        if any(substring in col for substring in ["Q_Bar", "Year"])
    ]
    _data = _data[_filtered]
    del _data["Q_Bar|South Africa"]
    _target_year = max(_data.Year)
    _years_x = np.arange(2025, _target_year + 1, 1)

    _ratio = []

    for _index, _row in _data.iterrows():
        _values = _row.values[1:]
        _max = max(_values)
        _ratio.append(np.around(_max / 140 * 100, 1))
    ax.grid(which="major", axis="y", color="#758D99", alpha=1, zorder=-1000)
    ax.xaxis.set_major_formatter(FuncFormatter(format_x_ticks))
    major_locator = MultipleLocator(5)
    ax.xaxis.set_major_locator(major_locator)
    minor_locator = MultipleLocator(1)
    ax.xaxis.set_minor_locator(minor_locator)
    ax.grid(which="major", axis="y", color="#758D99", alpha=1, zorder=-1000)
    ax.yaxis.set_major_formatter(FuncFormatter(format_y_ticks))
    ax.grid(
        which="major",
        axis="y",
        color="#758D99",
        alpha=0.4,
        zorder=-1000,
        linestyle="dashed",
    )
    ax.set_ylim([0, 100])
    ax.plot(
        _years_x,
        _ratio,
        color="black",
        linewidth=2,
        marker="o",
        markersize=8,
        markeredgecolor="black",
        markevery=5,
        zorder=10000,
    )
    ax.plot(
        _years_x,
        _ratio,
        color="black",
        linewidth=0,
        marker="o",
        markersize=3,
        markeredgecolor="black",
    )
    ax.set_xlabel("Year", fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(file_name, output_name))
    return
