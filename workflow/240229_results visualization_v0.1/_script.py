import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.patches as mpatches
import os


plt.style.use("default")
plt.rcParams["xtick.labelsize"] = 12
plt.rcParams["ytick.labelsize"] = 12
plt.rcParams["hatch.linewidth"] = 0.5


"""
    SET SCRIPT INPUTS HERE
"""

_file_name = "20240222_1600_RQ1xxDiverse_On+Stockpiling_On_2040"
_file_name2 = "20240223_1046_RQ1xxDiverse_On+Stockpiling_On_2040_no_uniform_prices"
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


def plot_function(file_name=str, output_name=str, _save=None):

    fig, ax = plt.subplots(figsize=(6 * 1.2, 4 * 1.2))

    _data = pd.read_excel(file_name + "/M1_overview.xlsx")

    _target_year = max(_data.Year)
    _years_x = np.arange(2030, _target_year + 1, 5)
    _bottom_bars = np.zeros(shape=len(_years_x))

    _dict = dict()
    _years = _data.Year
    for _exp in [
        "South Africa",
        "North America",
        "Zimbabwe",
        "Russia",
        "World",
        "Recycling",
    ]:
        _all_values = _data["Q|" + _exp]
        _2030 = 0
        _2035 = 0
        _2040 = 0
        for _y, _val in zip(_years, _all_values):
            if _y <= 2030:
                _2030 += _val
            elif _y <= 2035:
                _2035 += _val
            else:
                _2040 += _val

        _dict[_exp] = [_2030, _2035, _2040]

    for _exp in [
        "South Africa",
        "North America",
        "Zimbabwe",
        "Russia",
        "World",
        "Recycling",
    ]:
        _values = _dict[_exp]
        if sum(_values) == 0:
            pass
        else:
            ax.bar(
                _years_x,
                _values,
                bottom=_bottom_bars,
                label=_exp,
                color=_colors.get(_exp),
                width=2.25,
                zorder=2,
                alpha=1,
                linewidth=0.25,
                edgecolor="black",
            )
            _bottom_bars += _values

    

    formatter = ticker.ScalarFormatter(useMathText=True)
    formatter.set_scientific(True)
    ax.xaxis.set_major_formatter(formatter)

    ax.grid(which="major", axis="y", color="#758D99", alpha=0.2, zorder=1)
    ax.grid(which="minor", axis="both", color="#758D99", alpha=0.2, zorder=1)

    ax.set_xlabel("Period", fontsize=14)
    ax.set_ylabel("Import in tons", fontsize=14)

    _patches = []
    for _reg in reversed(
        ["South Africa", "North America", "Zimbabwe", "World", "Recycling"]
    ):
        if _reg == "Recycling":
            _name = "Secondary supply"
            _patches.append(
                mpatches.Patch(color=_colors.get(_reg, "black"), label=_name)
            )
        else:
            _patches.append(
                mpatches.Patch(color=_colors.get(_reg, "black"), label=_reg)
            )

    ax.legend(
        handles=_patches,
        facecolor="#EEEEEE",
        fontsize=12,
        handlelength=1.25,
        handletextpad=0.5,
        borderpad=0.5,
        columnspacing=1,
        edgecolor="black",
        frameon=True,
        shadow=False,
    )

    ax.set_xticks([2030, 2035, 2040])
    ax.set_xticklabels(labels=["2025-30", "2030-35", "2035-40"])
    
    plt.tight_layout()

    plt.savefig(os.path.join(result_dir, output_name))


def plot_line_plot_prices(file_name=None, output_name=None, _save=None):
    fig, ax = plt.subplots(figsize=(6 * 1.2, 4 * 1.2))

    _data = pd.read_excel(file_name + "/M1_overview.xlsx")

    _target_year = max(_data.Year)
    _years_x = np.arange(2025, _target_year + 1, 1)

    _values = _data["Market price"]

    ax.bar(
        _years_x,
        _values,
        label="Prices",
        color="gray",
        zorder=2,
        alpha=1,
        linewidth=0.25,
    )
    ax.set_xlim([2024.5, 2040.5])
    ax.set_xticks(range(2025, 2041, 1))
    _list = []
    for _x in list(range(2025, 2041, 1)):
        _list.append(str(_x))
    ax.set_xticklabels(labels=_list, rotation=90)

    ax.set_xlabel("Year", fontsize=14)
    ax.set_ylabel("Marginal supply cost in MEUR/ton", fontsize=14)

    plt.tight_layout()
    plt.savefig(os.path.join(result_dir, output_name))
    return


def plot_marginal_supply_cost_with_and_without_arbitrage(
    file_name1=None, file_name2=None, output_name=None
):
    fig, ax = plt.subplots(figsize=(6 * 1.2, 4 * 1.2))
    _data = pd.read_excel(file_name1 + "/M1_overview.xlsx")
    prices_uniformed = _data["Market price"]
    prices_not_uniformed = pd.read_excel(file_name2 + "/M1_overview.xlsx")[
        "Market price"
    ]
    _target_year = max(_data.Year)
    _years_x = np.arange(2025, _target_year + 1, 1)
    formatter = ticker.ScalarFormatter(useMathText=True)
    formatter.set_scientific(True)
    ax.xaxis.set_major_formatter(formatter)
    ax.grid(which="major", axis="both", color="#758D99", alpha=0.2, zorder=1)
    ax.grid(which="minor", axis="both", color="#758D99", alpha=0.2, zorder=1)
    ax.plot(
        _years_x,
        prices_uniformed,
        label="Uniform",
        color="gray",
        zorder=2,
        alpha=1,
        linewidth=1.5,
    )
    ax.plot(
        _years_x,
        prices_not_uniformed,
        label="Not uniform",
        color="gray",
        zorder=2,
        alpha=1,
        linewidth=1.5,
        linestyle="dotted",
    )
    ax.fill_between(
        _years_x,
        prices_uniformed,
        prices_not_uniformed,
        color="gray",
        zorder=0,
        alpha=0.5,
    )

    _average = []

    for elem1, elem2 in zip(prices_uniformed, prices_not_uniformed):
        _average.append((elem1 + elem2) / 2)

    ax.plot(
        _years_x,
        _average,
        label="Average",
        color="#FF407D",
        zorder=4,
        alpha=1,
        linewidth=2.5,
        linestyle="dashed",
    )

    ax.set_ylim([0, 45])
    ax.set_xlim([2024.5, 2040.5])
    ax.set_xticks(range(2025, 2041, 1))
    _list = []
    for _x in list(range(2025, 2041, 1)):
        _list.append(str(_x))
    ax.set_xticklabels(labels=_list, rotation=90)

    ax.set_xlabel("Year", fontsize=14)
    ax.set_ylabel("Marginal supply cost in MEUR/ton", fontsize=14)

    ax.legend(
        facecolor="#EEEEEE",
        loc="lower right",
        fontsize=12,
        handlelength=1.25,
        handletextpad=0.5,
        borderpad=0.5,
        columnspacing=1,
        edgecolor="black",
        frameon=False,
        shadow=False,
    )

    plt.tight_layout()
    plt.savefig(os.path.join(result_dir, output_name))
    return


def plot_maximum_share_of_exporter(file_name=None, output_name=None, _save=None):
    fig, ax = plt.subplots(figsize=(6 * 1.2, 4 * 1.2))
    _data = pd.read_excel(file_name + "/M1_overview.xlsx")
    _target_year = max(_data.Year)
    _years_x = np.arange(2025, _target_year + 1, 1)

    _values = []
    for index, row in _data.iterrows():
        _share = max([(row["Q|" + _exp] / row["Demand"]) for _exp in ["South Africa"]])
        _values.append(np.around(_share * 100, 0))

    _color_share = "#78A083"
    ax.bar(_years_x, _values, color=_color_share, linewidth=2, zorder=1, alpha=1)
    ax.plot(
        _years_x,
        16 * [65],
        color="black",
        linestyle="dotted",
        zorder=2,
        linewidth=2,
        label="Import share limit of 65%",
        marker="d",
        markersize=3,
    )

    _diff = []
    _bottom_bars = []

    for elem1, elem2 in zip(16 * [65], _values):
        _temp = elem1 - elem2
        if _temp >= 65 * 0.5:
            _diff.append(_temp)
            _bottom_bars.append(elem2)
        else:
            _diff.append(0)
            _bottom_bars.append(0)

    for _index, _value in enumerate(_diff):
        if (_index <= 8) and (_value > 0):
            _diff[_index] = 0

    ax.bar(
        _years_x,
        _diff,
        color="#F9B572",
        bottom=_bottom_bars,
        zorder=2,
        alpha=1,
        hatch="//",
        label="Stockpiling quantities",
    )

    ax.set_ylim([0, 100])
    ax.set_xlim([2024.5, 2040.5])
    ax.set_xticks(range(2025, 2041, 1))
    _list = []
    for _x in list(range(2025, 2041, 1)):
        _list.append(str(_x))
    ax.set_xticklabels(labels=_list, rotation=90)

    ax.set_xlabel("Year", fontsize=14)
    ax.set_ylabel("Import share of major exporter in %", fontsize=14)
    plt.legend(
        facecolor="#EEEEEE",
        fontsize=12,
        handlelength=1.5,
        handletextpad=0.5,
        borderpad=0.5,
        columnspacing=1,
        edgecolor="black",
        frameon=False,
        shadow=False,
    )

    formatter = ticker.ScalarFormatter(useMathText=True)
    formatter.set_scientific(True)
    ax.xaxis.set_major_formatter(formatter)

    ax.grid(which="major", axis="y", color="#758D99", alpha=0.2, zorder=1)
    ax.grid(which="minor", axis="both", color="#758D99", alpha=0.2, zorder=1)

    plt.tight_layout()
    plt.savefig(os.path.join(result_dir, output_name))

    return


def plot_stockpiling_usage(file_name=None, output_name=None):
    fig, ax = plt.subplots(figsize=(6 * 1.2, 4 * 1.2))
    _data = pd.read_excel(file_name + "/M1_overview.xlsx")
    _target_year = max(_data.Year)
    _years_x = np.arange(2025, _target_year + 1, 1)

    _values = _data["Stock_stored|"]

    ax.bar(
        _years_x,
        _values,
        label="Stock",
        color="#F9D949",
        zorder=2,
        alpha=1,
        linewidth=0.75,
        edgecolor="black",
    )
    ax.set_xlim([2024.5, 2040.5])
    ax.set_xticks(range(2025, 2041, 1))
    _list = []
    for _x in list(range(2025, 2041, 1)):
        _list.append(str(_x))
    ax.set_xticklabels(labels=_list, rotation=90)

    ax.set_xlabel("Year", fontsize=14)
    ax.set_ylabel("Stock in tons", fontsize=14)

    plt.tight_layout()
    plt.savefig(output_name)
    return


def plot_stockpiling_usage_relative(file_name=None, output_name=None, _save=None):
    fig, ax = plt.subplots(figsize=(6 * 1.2, 4 * 1.2))
    _data = pd.read_excel(file_name + "/M1_overview.xlsx")
    _target_year = max(_data.Year)
    _years_x = np.arange(2025, _target_year + 1, 1)

    _values = _data["Stock_stored|"]
    _demand = _data["Demand"]

    _output = []
    for val, dem in zip(_values, _demand):
        _output.append(val / dem)

    ax.bar(
        _years_x,
        _output,
        label="Stock",
        color="#F9B572",
        zorder=2,
        alpha=1,
        linewidth=0.75,
        edgecolor="black",
    )
    ax.set_xlim([2024.5, 2040.5])
    ax.set_xticks(range(2025, 2041, 1))
    _list = []
    for _x in list(range(2025, 2041, 1)):
        _list.append(str(_x))
    ax.set_xticklabels(labels=_list, rotation=90)

    ax.set_xlabel("Year", fontsize=14)
    ax.set_ylabel("Ratio between stock and annual demand", fontsize=14)

    # _values = _data['Stock_stored|']
    # _offset = ax.get_ylim()[1] * 0.025
    # for _i, _value in enumerate(_values):
    #     print(_i + 2025)
    #     _y = _value / _demand[_i]
    #     print(_y)
    #     ax.text(_i + 2025, _y + _offset, '(' + str(_value) + 't)', ha='center', color='black', rotation=90)

    ax.set_ylim([0, 3])
    _values = _data["Stock_stored|"]
    _offset = ax.get_ylim()[1] * 0.025
    for _i, _value in enumerate(_output):
        _value = np.around(_value, 2)
        ax.text(
            _i + 2025,
            _value + _offset,
            "(" + str(_value) + ")",
            ha="center",
            color="black",
            rotation=90,
        )

    formatter = ticker.ScalarFormatter(useMathText=True)
    formatter.set_scientific(True)
    ax.xaxis.set_major_formatter(formatter)

    ax.grid(which="major", axis="y", color="#758D99", alpha=0.2, zorder=1)
    ax.grid(which="minor", axis="both", color="#758D99", alpha=0.2, zorder=1)

    plt.tight_layout()
    plt.savefig(os.path.join(result_dir, output_name))
    return


def plot_q_bar_of_exporter(file_name=None, output_name=None):
    fig, ax = plt.subplots(figsize=(6 * 1.2, 4 * 1.2))
    _data = pd.read_excel(file_name + "/M1_overview.xlsx")
    _target_year = max(_data.Year)
    _years_x = np.arange(2025, _target_year + 1, 1)
    for _exp in ["South Africa", "Recycling", "Russia", "Zimbabwe", "North America", "World", ]:
        _val = _data['Q_Bar|'+_exp]
        ax.plot(_years_x, _val, label=_exp, color=_colors.get(_exp), linewidth=2)
    
    formatter = ticker.ScalarFormatter(useMathText=True)
    formatter.set_scientific(True)
    ax.xaxis.set_major_formatter(formatter)

    ax.grid(which="major", axis="both", color="#758D99", alpha=0.2, zorder=1)
    ax.grid(which="minor", axis="both", color="#758D99", alpha=0.2, zorder=1)
    
    plt.legend(
        facecolor="#EEEEEE",
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






plot_function(
    file_name="model outputs/" + _file_name,
    output_name="rq1_A_import_quantities_to_the_eu.pdf",
    _save=result_dir,
)
plot_line_plot_prices(
    file_name="model outputs/" + _file_name,
    output_name="rq1_B_marginal_supply_cost_in_the_eu.pdf",
    _save=result_dir,
)
plot_marginal_supply_cost_with_and_without_arbitrage(
    file_name1="model outputs/" + _file_name,
    file_name2="model outputs/" + _file_name2,
    output_name="rq1_C_marginal_supply_cost_in_the_eu.pdf",
)
plot_maximum_share_of_exporter(
    file_name="model outputs/" + _file_name,
    output_name="rq1_D_maximum_import_share_to_the_eu.pdf",
    _save=result_dir,
)
plot_stockpiling_usage_relative(
    file_name="model outputs/" + _file_name,
    output_name="rq1_E_stockpiling_relative_to_demand_in_the_eu.pdf",
    _save=result_dir,
)
plot_q_bar_of_exporter(
    file_name="model outputs/" + _file_name,
    output_name="rq1_F_export_capacity_global_scale.pdf"
)
