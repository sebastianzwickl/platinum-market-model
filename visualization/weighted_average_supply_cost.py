import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.patches as mpatches
from matplotlib.ticker import FuncFormatter
import os
from matplotlib.ticker import MultipleLocator


plt.style.use("latex-sans")
plt.rcParams["xtick.labelsize"] = 12
plt.rcParams["ytick.labelsize"] = 12
plt.rcParams["hatch.linewidth"] = 0.5
plt.rcParams["axes.axisbelow"]


_colors = {
    "Recycling": "#78A083",
    "North America": "#ED7B7B",
    "Zimbabwe": "#3085C3",
    "Russia": "purple",
    "World": "#D6D46D",
    # "Recycling_low": "#04364A",
}

_cost_dict = {
    "North America": 21.78534589616,
    "Zimbabwe": 21.4313340253474,
    "Russia": 13.9426213735424,
    "World": 20.151444953948,
    "Recycling_low": 32.1878485615764,
    "Recycling_high": 48.2817728423646,
}


def format_x_ticks(value, _):
    return f"{int(value)}"


def function7(file_name=None, output_name=None):

    fig, ax = plt.subplots(figsize=(6 * 1.05, 4 * 1.05))
    _data = pd.read_excel(file_name + "/M1_overview.xlsx")
    _target_year = max(_data.Year)
    _years_x = np.arange(2025, _target_year + 1, 1)
    _results = []
    for _index, _row in _data.iterrows():

        _cost = 0
        _supply = 0
        for _exp in _cost_dict.keys():
            _cost += _row["Q|" + _exp] * _cost_dict[_exp]
            _supply += _row["Q|" + _exp]
        _cost += _row["Q|South Africa"] * _row["Production cost of major exporter"]
        _supply += _row["Q|South Africa"]

        if _cost == 0:
            _results.append(0)
        else:
            _results.append(_cost / _supply)

    _drop_index = []
    for _index, _element in enumerate(_results):
        if _element == 0:
            _drop_index.append(_index)
        else:
            pass

    for _value in _drop_index:
        if len(_drop_index) == 1:
            _x1 = _years_x[0:_value]
            _y1 = _results[0:_value]

            ax.plot(
                _x1,
                _y1,
                color="#FC6736",
                linewidth=2,
                zorder=8,
                linestyle="solid",
                label="No import",
                marker="o",
                markersize=4,
            )

            _x2 = _years_x[_value + 1 :]
            _y2 = _results[_value + 1 :]

            ax.plot(
                _x2,
                _y2,
                color="#FC6736",
                linewidth=2,
                zorder=8,
                linestyle="solid",
                marker="o",
                markersize=4,
            )

        else:
            print("More than a single gap")

        ax.plot(
            [2030, 2031, 2032],
            [38.8, 42.04, _results[_value + 1]],
            color="#607274",
            linewidth=2.5,
            zorder=7,
            linestyle="solid",
            marker="o",
            markersize=4,
            markevery=2,
            label="Stockpiling",
        )
        ax.plot(
            2031,
            42.04,
            marker="o",
            color="#607274",
            zorder=100,
            markersize=4,
        )

        ax.plot(
            [2038, 2039],
            [_results[-3], _results[-2]],
            color="#607274",
            linewidth=2.5,
            zorder=9,
            linestyle="solid",
            marker="o",
            markersize=4,
            markevery=1,
        )
        ax.plot(
            2031,
            42.04,
            marker="o",
            color="#607274",
            zorder=100,
            markersize=4,
        )

        box_color = "#444444"

        ax.plot(
            [2031, 2031],
            [42.04, 30],
            linestyle="solid",
            color=box_color,
            linewidth=0.5,
            zorder=-1,
        )

        ax.text(
            x=2030.25,
            y=29,
            s="42.04 MEUR/tons\n(93$\%$ stock up, 7$\%$ stocking)",
            fontsize=12,
            va="center",
            ha="left",
            color="black",
            multialignment="left",
            linespacing=1.5,
            bbox=dict(
                facecolor="white",
                edgecolor="black",
                linewidth=0.1,
                boxstyle="round,pad=0.3",
            ),
        )

        # ax.plot([2030, 2031], 2*[39.04], linestyle='solid', linewidth=2, zorder=10, marker='d', color='#607274', markersize=0)
        # ax.plot([2031, 2031], [39.04, 39.04+3], linestyle='solid', linewidth=2, zorder=10, color='#607274', markersize=0)
        # ax.plot([2031, 2032], [39.04+3, _results[_value+1]], linestyle='solid', linewidth=2, zorder=10, marker='d', color='#607274', markersize=0)

        # _value_before = _results[_value - 1]
        # _value_after = _results[_value + 1]
        # _new_value = _value_before + 0.5 * (_value_after - _value_before)

        # print(_new_value)

        # _x_new = [_y+2025 for _y in [_value-1, _value, _value+1]]
        # _y_new = [_value_before, _new_value, _value_after]

        # # ax.plot(
        # #     _x_new,
        # #     _y_new,
        # #     color="#607274",
        # #     linewidth=2,
        # #     zorder=10,
        # #     linestyle='dashed',
        # #     label='Stockpiling',
        # #     marker='o',
        # #     markersize=6,
        # #     markevery=2
        # # )

        # _y_new = [_value_before, 0, _value_after]

    # _results.remove(0)
    # _years_x_updated = np.arange(2025, _target_year + 1, 1).tolist()
    # _years_x_updated.pop(_drop_index[0])

    # print(_results)

    # ax.plot(
    #     _years_x_updated,
    #     _results,
    #     color="#FC6736",
    #     linewidth=2,
    #     zorder=9,
    #     label='Import'
    # )

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
    ax.set_ylabel("Weighted average supply cost [MEUR/tons]", fontsize=12)
    ax.set_ylim([0, 80])

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

    plt.tight_layout()
    plt.savefig(os.path.join(file_name, output_name))

    return
