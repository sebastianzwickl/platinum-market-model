import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.patches as mpatches
from matplotlib.ticker import FuncFormatter
import os
from matplotlib.ticker import MultipleLocator


# print(plt.style.available)

plt.style.use("classic")
plt.rcParams["xtick.labelsize"] = 12
plt.rcParams["ytick.labelsize"] = 12
plt.rcParams["hatch.linewidth"] = 0.5


"""
    SET SCRIPT INPUTS HERE
"""

_file_name = "20240222_1600_RQ1xxDiverse_On+Stockpiling_On_2040"

result_dir = os.path.join("figures", "{}".format(_file_name))
if not os.path.exists(result_dir):
    os.makedirs(result_dir)


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
        "South Africa": "#78A083",
        "North America": "#ED7B7B",
        "Zimbabwe": "#3085C3",
        "Russia": "purple",
        "World": "#D6D46D",
        "Recycling": "#04364A",
        "Stock_out|": "pink",
    }


def format_x_ticks(value, _):
    return f'{int(value)}'


def plot_q_bar_of_exporter(file_name=None, output_name=None):
    fig, ax = plt.subplots(figsize=(6 * 1.2, 4 * 1.2))
    _data = pd.read_excel(file_name + "/M1_overview.xlsx")
    _target_year = max(_data.Year)
    _years_x = np.arange(2025, _target_year + 1, 1)
    for _exp in ["South Africa", "Recycling", "Russia", "Zimbabwe", "North America", "World", ]:
        _val = _data['Q_Bar|'+_exp]
        ax.plot(_years_x, _val, label=_exp, color=_colors.get(_exp), linewidth=2, marker='o', markersize=0)
    

    ax.xaxis.set_major_formatter(FuncFormatter(format_x_ticks))
    major_locator = MultipleLocator(5)
    ax.xaxis.set_major_locator(major_locator)
    minor_locator = MultipleLocator(1)
    ax.xaxis.set_minor_locator(minor_locator)
    
    ax.grid(which="major", axis="x", color="#758D99", alpha=1, zorder=1)
    ax.grid(which="minor", axis="x", color="#758D99", alpha=0.5, zorder=1)
    
    plt.legend(
        facecolor="white",
        fontsize=12,
        handlelength=1.5,
        handletextpad=0.5,
        borderpad=0.5,
        columnspacing=1,
        edgecolor="black",
        frameon=False,
        shadow=False,
        ncol=1,
        loc="upper right",
        bbox_to_anchor=(1, 0.95),
    )
    
    plt.tight_layout()
    plt.savefig(os.path.join(result_dir, output_name))
    
    return


plot_q_bar_of_exporter(
    file_name="model outputs/" + _file_name,
    output_name="rq1_F_export_capacity_global_scale.pdf"
)
