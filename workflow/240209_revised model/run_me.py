import utils
import numpy as np
import pyomo.environ as py
from datetime import datetime
import pandas as pd
import os
import save_results_to_iamc_files as report
import plot_results_with_pyam as plot
import equations
from pyomo.environ import *


"""
##############################################################################
"""
""" (A) GET INPUT DATA """
"""
##############################################################################
"""


data = pd.read_excel(
    "input data/You can fill in your data here v.240109.xlsx", sheet_name="Data"
)

# DEMAND PLATINUM: FOR EACH MARKET, MATERIAL, AND YEAR (2025 to 2050) (d_{m,t})
_demand = data.loc[data.Variable == "Demand|Platinum"]
_dem_dict_EU, _dem_dict_World = utils.get_demand_data_for_both_markets(_demand)

# STOCKPILING COST FOR THE EUROPEAN MARKET (c^{stock})
_stock_cost = data.loc[
    data.Variable == "Stockpiling cost for the European market|Platinum"
]["Value"].item()

# MAINTENANCE COST PER FRINGE EXPORTER (c^{main}_{e'})
_maintenance_cost = data.loc[
    data.Variable == "Maintenance cost per export capacity|Platinum"
]["Value"].item()

# AVERAGE PRODUCTION COST PER EXPORTER (c^{gen}_{e,t})
_data_production = data.loc[data.Variable == "Average Production Cost|Platinum"]
_production_costs = dict()
_maintenance_costs_dict = dict()
for _index, _row in _data_production.iterrows():
    if _row.Region != "South Africa":
        _production_costs[_row.Region] = _row.Value
        _maintenance_costs_dict[_row.Region] = _maintenance_cost
    else:
        _production_costs_south_africa = _row.Value


"""
##############################################################################
"""   
""" (B) CREATE MODEL """
"""
##############################################################################
"""  

model = py.ConcreteModel()
model.name = 'bilevel'
# INIT SCENARIO NAME
model.scenario = "Scenario1"

# INIT SETS
model.set_e = py.Set(initialize=list(_data_production.Region), doc='EXPORTERS.')

model.set_e_stroke = py.Set(
    initialize=list(set(list(_production_costs.keys())) - set(["South Africa"])),
    doc='FRINGE EXPORTERS.'
)

model.set_market = py.Set(initialize=["M1", "M2"], doc='MARKETS.')

model.set_t = py.Set(initialize=list(range(2025, 2051, 1)), doc='TIMESTEPS.')

model.set_t_stroke = py.Set(initialize=range(2026, 2051, 1), doc='TIMESTEPS WITHOUT INITIAL TIMESTEP.')

model.set_mexporter = py.Set(initialize=["South Africa"], doc='MAJOR EXPORTER WITH MARKET POWER.')

model.set_embargo_m1 = py.Set(initialize=[])


"""
##############################################################################
"""   
""" (C) ADD DECISION VARIABLES """
"""
##############################################################################
"""


# ADD DECISION VARIABLES
utils.add_decision_variables_vector_x(model) # checked
utils.add_decision_variables_vector_lambda(model) # checked
utils.add_decision_variables_vector_mhu(model) # checked
utils.add_decision_variables_vector_y(model) # checked
utils.add_decision_variables_vector_u(model) # checked
utils.add_decision_variables_vector_sigma(model) # checked
utils.add_decision_variables_vector_z(model) # checked


"""
##############################################################################
"""   
""" (D) INITIALIZE PARAMETERS """
"""
##############################################################################
"""


model.par_c_gen_e_t = py.Param(
    model.set_e_stroke,
    initialize=_production_costs,
    doc="PAR: cost of generation for the fringe supplier [EUR/t] (c_e_stroke).",
)
# print('GENERATION COST OF FRINGE SUPPLIERS [MEUR/t]')
# for _e in model.set_e_stroke:
#     print('{}: {:.1f}'.format(_e, model.par_c_gen_e_t[_e]/1000000))
# print('')


model.par_c_snake = py.Param(
    model.set_mexporter,
    initialize=_production_costs_south_africa,
    doc="PAR: cost of generation for the major supplier [EUR/t].",
)
# print('GENERATION COST OF MAJOR SUPPLIER [MEUR/t]')
# print('South Africa: {:.1f} MEUR/t'.format(model.par_c_snake['South Africa']/1000000))
# print('')


model.par_c_main_e_stroke = py.Param(
    model.set_e_stroke,
    initialize=_maintenance_costs_dict,
    doc="PAR: maintenance cost of generation for the fringe supplier [EUR/t*yr].",
)
# print('MAINTENANCE COST OF FRINGE SUPPLIERS [MEUR/t*yr]')
# for _e in model.set_e_stroke:
#     print('{}: {:.1f}'.format(_e, model.par_c_main_e_stroke[_e]/1000000))
# print('')


model.par_c_stock = py.Param(
    initialize=_stock_cost,
    doc="PAR: stockpilling cost of the European market [EUR/t*yr].",
)
# print('STOCKPILLING COST OF THE EUROPEAN MARKET: {:.1f} [kEUR/t*yr]'.format(model.par_c_stock()/1000))
# print('')

_dem_dict = {**_dem_dict_EU, **_dem_dict_World}

model.par_demand = py.Param(
    model.set_market,
    model.set_t,
    initialize=_dem_dict,
    doc="PAR: demand per market and year (d_m_t).",
)
# print('PLATINUM DEMAND [t/yr]')
# for _m in model.set_market:
#     for _t in model.set_t:
#         print('{}|{}: {:.1f}'.format(_m, _t, model.par_demand[_m, _t]))
# print('')


model.par_alpha = py.Param(initialize=0.65, doc="PAR: alpha (alpha).")

model.par_big_m = py.Param(initialize=10e20, doc="PAR: big m.")

model.par_beta_snake = py.Param(initialize=10e20, doc="PAR: beta_snake.")

model.par_epsilon = py.Param(initialize=5, doc="PAR: epsilon.")

_dict_q_bar_e_stroke_t_stroke = {
    "Russia": 35,  # (initially 20, final: 35)
    "Zimbabwe": 15,  # (initially 7.5, final: 15)
    "North America": 9.3,  # Canada 6 + United States 3.3 (initially 7.5, final: 9.3)
    "World": 2, # (final 2)
    "Recycling" : 50, # (final 50)
    "Slack exporter" : 5 # (final 5)
}

model.par_q_bar_e_stroke = py.Param(
    model.set_e_stroke,
    initialize=_dict_q_bar_e_stroke_t_stroke,
    doc="PAR: initial maximum export capacity of the fringe suppliers.",
)
# print('INITIAL EXPORT CAPACITY [t/yr]')
# for _e in model.set_e_stroke:
#     print('{}: {:.1f}'.format(_e, model.par_q_bar_e_stroke[_e]))


model.par_q_bar_emajor = py.Param(
    initialize=250, doc="PAR: maximum export capacity of the major exporter."
)
# print('{}: {:.1f}'.format('South Africa', model.par_q_bar_emajor()))
# print('')


"""
##############################################################################
"""   
""" (E) ADD CONSTRAINTS """
"""
##############################################################################
"""

# equations.add_feasible_constraint(model)

equations.add_equality_constraints(model) # equation 4, 5, 6, 7, 9, and 10
equations.add_21(model)
equations.add_equation_40(model)
equations.add_equation_41(model)
equations.add_equation_42(model)
equations.add_equation_43(model)
equations.add_equation_44(model)
equations.add_equation_45(model)

# equations.add_equation_46(model)

equations.add_equation_54_1(model)
equations.add_equation_54_2_lower(model)
equations.add_equation_54_2_upper(model)

equations.add_equation_55_1(model)
equations.add_equation_55_2_lower(model)
equations.add_equation_55_2_upper(model)

equations.add_56_1(model)
equations.add_56_2(model)

equations.add_57_1(model)
equations.add_57_2(model)

equations.add_58_1(model)
equations.add_58_2(model)

equations.add_59_1(model)
equations.add_59_2(model)

equations.add_60_1(model)
equations.add_60_2(model)

equations.add_63(model)

equations.add_64_1(model)
equations.add_64_2(model)
equations.add_64_3(model)  

equations.add_65(model)

equations.add_66_1_to_70_2(model)

equations.add_71_to_74(model)

equations.add_18(model)
equations.add_18_y_axis(model)

# def restrict_capacity(model=None, exporter=None, time=None):
#     return model.var_q_bar[exporter, time] <= model.par_q_bar_e_stroke[exporter]

# model.con_restrict = py.Constraint(model.set_e_stroke, model.set_t, rule=restrict_capacity)








"""
    SOLVE THE MODEL
"""


def objective_func(model):
    _first_term = sum(
        model.par_c_gen_e_t[e] * model.var_z[e, m, t] 
        for e in model.set_e_stroke
        for m in model.set_market
        for t in model.set_t
        )
    _second_term = sum(
        model.var_q[exp, m, t] * model.par_c_snake[exp]
        for exp in model.set_mexporter
        for m in model.set_market
        for t in model.set_t
    )
    
    return _first_term - _second_term



model.objective = py.Objective(expr=objective_func, sense=py.maximize)

solver = py.SolverFactory("gurobi")

model.write('materials.lp', io_options={"symbolic_solver_labels": True})

results = solver.solve(model, tee=False, warmstart=True)

model.objective.display()
# solution.write(num=1, dual=True)

# print("OBJECTIVE VALUE: {:.0f} MEUR".format(model.objective() / 1000000))

# for _year in model.set_t:
#     print('Lambda 5 | {}: {:.1f}'.format(_year, model.var_lambda_5[_year]()))
#     for _e in model.set_e_stroke:
#         print('var_q {}: {}'.format(_e, model.var_q[_e, 'M1', _year]()))
#         print('var_q_bar {}: {}'.format(_e, model.var_q_bar[_e, _year]()))
#         if model.var_sigma[_e, 'M1', _year]() != 0:
#             print('Sigma {}: {:.1f}'.format(_e, model.var_sigma[_e, 'M1', _year]()))
        
# if (results.solver.status == SolverStatus.infeasible) or \
#    (results.solver.termination_condition == TerminationCondition.infeasible):
#     # Get and print the infeasibility proof
#     infeasible_constraints = []
#     for constr in model.component_data_objects(Constraint, active=True):
#         if constr.lower == constr.upper == 0.0:
#             infeasible_constraints.append(constr.name)
    
#     print("Infeasible constraints:", infeasible_constraints)
# else:
#     # Access the optimal solution or other relevant information
#     print("Optimal solution found:", value(model.objective))    
   
    
    

