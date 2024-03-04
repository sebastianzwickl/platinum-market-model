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
    return f"{int(value)}"


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
    
    _major_min_fringe = []
    _max_major_min_fringe = []
    
    for _index, _row in _data.iterrows():
        _values = _row.values[1:]
        _major_min_fringe.append(140 - sum(_values)) # (A)
        _max_major_min_fringe.append(140 - max(_values)) # (B)
        
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
    # ax.set_ylim([0, 150])
    
    ax.plot(_years_x, _max_major_min_fringe, color='#FF407D', label='Major to largest fringe exporter', linewidth=2, zorder=3)
    ax.plot(_years_x, _major_min_fringe, color='#40679E', label='Major to sum of all fringe exporters', linewidth=2, zorder=3)
    
    
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
        ncol=1,
        loc="lower left",
        bbox_to_anchor=(0.025, 0.025),
        framealpha=1,
    )

    _leg.get_frame().set_linewidth(0.5)
    

    # for tick in ax.yaxis.get_major_ticks():
    #     if tick.label1.get_position()[1] == 0:
    #         tick.gridline.set_visible(False)
    
    ax.axhline(0, color='black', linewidth=0.75, linestyle='dashed', label='X-axis', zorder=2)
    
    ax.set_xlabel("Year", fontsize=12)
    ax.set_ylabel("Difference in the supply capacity [tons/year] ", fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(file_name, output_name))
    return
