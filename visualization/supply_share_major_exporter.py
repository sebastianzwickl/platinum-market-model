import pandas as pd
import numpy as np
import os


def function6(file_name=None, output_name=None):
    _data = pd.read_excel(file_name + "/M1_overview.xlsx")
    _sa = _data["Q|South Africa"]
    _d = _data["Demand"]

    _ratio = dict()

    for _period in [[2025, 2030], [2030, 2035], [2035, 2041]]:
        _supply = sum(_sa.iloc[_period[0] - 2025 : _period[1] - 2025])
        _demand = sum(_d.iloc[_period[0] - 2025 : _period[1] - 2025])
        _ratio[_period[1]] = np.around(_supply / _demand * 100, 1)

    _txt_output = output_name
    _info = [
        "2030: " + str(_ratio[2030]) + "%",
        "2035: " + str(_ratio[2035]) + "%",
        "2040: " + str(_ratio[2041]) + "%",
    ]
    with open(os.path.join(file_name, _txt_output), "w") as datei:
        datei.write("\n".join(_info))
    return
