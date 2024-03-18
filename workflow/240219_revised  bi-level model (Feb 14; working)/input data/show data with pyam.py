import pyam
import matplotlib.pyplot as plt

df = pyam.IamDataFrame(
    "You can fill in your data here v.240109.xlsx", sheet_name="Data"
)

df = df.filter(region="World", variable="Demand|Platinum")

df.plot.bar(stacked=True, title="Platinum demand by 2050")

plt.legend(loc=2)
plt.tight_layout()
plt.show()
