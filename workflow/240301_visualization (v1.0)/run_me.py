from q_bar_over_time_plot import function1
from marginal_supply_costs import function2
from offered_export_capacity_of_the_major_exporter import function3
from ratio_q_bar_fringe_major import function4
from ratio_stock_stored_demand import function5
from supply_share_major_exporter import function6
from weighted_average_supply_cost import function7


_file_name = "20240229_1427_RQ1xxDiverse_On+Stockpiling_On_2040"

for _func, _out in [
    [function1, "0_export_capacity_fringe.pdf"],
    [function2, "1_marginal_supply_cost.pdf"],
    [function3, "2_export_capacity_major.pdf"],
    [function4, "3_ratio_export_capacity_fringe_major.pdf"],
    [function5, "4_ratio_stock_demand.pdf"],
    [function7, "5_weighted_average_supply_cost.pdf"],
    [function6, "6_supply_share_major.txt"],
]:
    _func(_file_name, _out)
