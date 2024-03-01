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


def draw_brace(ax, xspan, text, y_value):
    if text == "IDS":
        _lw = 0
    else:
        _lw = 0.5

    """Draws an annotated brace on the axes."""
    xmin, xmax = xspan
    xspan = xmax - xmin
    ax_xmin, ax_xmax = ax.get_xlim()
    xax_span = ax_xmax - ax_xmin
    ymin, ymax = ax.get_ylim()
    yspan = ymax - ymin
    resolution = int(xspan / xax_span * 100) * 2 + 1  # guaranteed uneven
    beta = 300.0 / xax_span  # the higher this is, the smaller the radius

    x = np.linspace(xmin, xmax, resolution)
    x_half = x[: resolution // 2 + 1]
    y_half_brace = 1 / (1.0 + np.exp(-beta * (x_half - x_half[0]))) + 1 / (
        1.0 + np.exp(-beta * (x_half - x_half[-1]))
    )
    y = np.concatenate((y_half_brace, y_half_brace[-2::-1]))
    y = y_value + (0.045 * y - 0.01) * yspan  # adjust vertical position

    ax.autoscale(False)
    ax.plot(x, y, lw=1, color="black")

    ax.text(
        (xmax + xmin) / 2.0,
        y_value + 0.085 * yspan,
        text,
        ha="center",
        va="bottom",
        fontsize=12,
        color="black",
        family="Helvetica",
        bbox=dict(
            facecolor="none", edgecolor="black", linewidth=_lw, boxstyle="round,pad=0.3"
        ),
    )
    return


def function2(file_name=None, output_name=None):
    fig, ax = plt.subplots(figsize=(6 * 1.05, 4 * 1.05))
    _data = pd.read_excel(file_name + "/M1_overview.xlsx")

    _target_year = max(_data.Year)
    _years_x = np.arange(2025, _target_year + 1, 1)

    _ratio = _data["Lambda_1"]

    ax.bar(
        _years_x, _ratio, color="#92C7CF", linewidth=0.5, zorder=10, edgecolor="black"
    )

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
    ax.set_ylim([0, 80])

    _list_of_index_checked = []

    for _index, _element in enumerate(_ratio):
        if _index in _list_of_index_checked:
            pass
        else:
            _list_of_index_checked.append(_index)
            _max = np.around(max(_ratio), 0)
            if _element >= (0.9 * _max):
                for _index2, _element2 in enumerate(_ratio):
                    if _index2 <= _index:
                        pass
                    else:
                        if _element2 >= (0.9 * _max):
                            _list_of_index_checked.append(_index2)
                            continue
                        else:
                            break
                _start = _index + 2025
                _end = _index2 + 2025 - 1

                if (_end - _start) > 1:
                    if _start == 2025:
                        draw_brace(ax, (_start, _end), "IDS", _max)
                    else:
                        draw_brace(
                            ax, (_start, _end), "Inelastic demand threshold (IDS)", _max
                        )
                else:
                    pass
                    draw_brace(ax, (_start - 0.5, _end + 1.5), "IDS", _max)

    # footnote_text = ""
    # figtext_x = 0.975  # X-coordinate of the footnote
    # figtext_y = 0.025  # Y-coordinate of the footnote

    # fig.text(figtext_x, figtext_y, footnote_text, ha='right', va='bottom', fontsize=12, color='gray')

    for _x, _value in enumerate(_ratio):
        ax.text(
            _x + 2025,
            _value * 0.5,
            s=str(np.around(_value, 1)),
            rotation=90,
            zorder=10,
            va="top",
            ha="center",
        )

    ax.set_ylabel("Marginal supply cost [MEUR/tons]", fontsize=12)

    plt.tight_layout()
    plt.savefig(os.path.join(file_name, output_name))

    return
