import pyam
import matplotlib.pyplot as plt

plt.style.use("default")
plt.rcParams["xtick.labelsize"] = 12
plt.rcParams["ytick.labelsize"] = 12

df = pyam.IamDataFrame(
    "You can fill in your data here v.240109.xlsx", sheet_name="Data"
)

df = df.filter(region="World", variable="Demand|Platinum")

_subplot = df.plot.bar(stacked=True, title="Platinum demand by 2050")

plt.legend(loc=2)
plt.tight_layout()
_subplot.figure.savefig("demand.pdf", dpi=1000)
