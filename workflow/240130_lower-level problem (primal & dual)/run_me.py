import utils
import numpy as np
import pyomo.environ as py
from datetime import datetime
import pandas as pd
import os
import equations
from openpyxl import load_workbook


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
model.dual = py.Suffix(direction=py.Suffix.IMPORT)
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

# PRIMAL

model.var_q = py.Var(
    model.set_e,
    model.set_market,
    model.set_t,
    within=py.NonNegativeReals,
    doc="VAR: (q_e_m_t).",
)

model.var_q_bar = py.Var(
    model.set_e_stroke,
    model.set_t,
    within=py.NonNegativeReals,
    doc="VAR: (q_bar_e_stroke_t).",
)

model.var_q_del = py.Var(
    model.set_e, 
    model.set_market,
    model.set_t,
    within=py.NonNegativeReals
)

model.var_q_arb = py.Var(
    model.set_e, 
    model.set_market,
    model.set_t,
    within=py.NonNegativeReals
)

model.var_stock_stored = py.Var(
    model.set_t, within=py.NonNegativeReals, doc="VAR: (q_stock_stored_M1_t)."
)

model.var_stock_in_out = py.Var(model.set_t, doc="VAR: (q_stock_in_out_M1_t).")

model.var_q_add = py.Var(
    model.set_e_stroke,
    model.set_t,
    within=py.NonNegativeReals,
    doc="VAR: (q_bar_add_e_stroke_t).",
)

model.var_q_bar_retire = py.Var(
    model.set_e_stroke,
    model.set_t,
    within=py.NonNegativeReals,
    doc="VAR: (q_bar_retire_e_stroke_t).",
)

model.var_q_diff = py.Var(
    model.set_e,
    model.set_t,
    within=py.NonNegativeReals
        
)

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


model.par_c_main_e_stroke = py.Param(
    model.set_e_stroke,
    initialize=_maintenance_costs_dict,
    doc="PAR: maintenance cost of generation for the fringe supplier [EUR/t*yr].",
)


model.par_c_stock = py.Param(
    initialize=_stock_cost,
    doc="PAR: stockpilling cost of the European market [EUR/t*yr].",
)

_dem_dict = {**_dem_dict_EU, **_dem_dict_World}

model.par_demand = py.Param(
    model.set_market,
    model.set_t,
    initialize=_dem_dict,
    doc="PAR: demand per market and year (d_m_t).",
)

model.par_alpha = py.Param(initialize=0.65, doc="PAR: alpha (alpha).")

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


model.par_q_bar_emajor = py.Param(
    initialize=250, doc="PAR: maximum export capacity of the major exporter."
)

_dict_Q = {
    "Russia": 5500,  # (initially 20, final: 35)
    "Zimbabwe": 1200,  # (initially 7.5, final: 15)
    "North America": 1210,  # Canada 6 + United States 3.3 (initially 7.5, final: 9.3)
    "World": 200, # (final 2)
    "Recycling" : 50000, # (final 50)
    "Slack exporter" : 50000, # (final 5)
    "South Africa": 63000 
}

model.par_Q = py.Param(
    model.set_e,
    initialize=_dict_Q,
    doc="PAR: maximum total reserves.",
)


"""
##############################################################################
"""   
""" (E) ADD CONSTRAINTS """
"""
##############################################################################
"""

def equation1(model, e, m, t):
    if m == 'M1': 
        return model.var_q_del[e, m, t] + model.var_q_arb[e, 'M2', t] - model.var_q[e, m, t] == 0
    else:
        return model.var_q_del[e, m, t] + model.var_q_arb[e, 'M1', t] - model.var_q[e, m, t] == 0
model.equation1 = py.Constraint(model.set_e, model.set_market, model.set_t, rule=equation1)


def equation2(model, t):
    return sum(model.var_q_del[e, "M1", t] for e in model.set_e) + sum(model.var_q_arb[e, "M2", t] for e in model.set_e) + model.var_stock_in_out[t] - model.par_demand['M1', t] == 0
model.equation2 = py.Constraint(model.set_t, rule=equation2)


def equation3(model, t):
    return sum(model.var_q_del[e, "M2", t] for e in model.set_e) + sum(model.var_q_arb[e, "M1", t] for e in model.set_e) - model.par_demand['M2', t] == 0
model.equation3 = py.Constraint(model.set_t, rule=equation3)


def equation4(model, e, t):
    return model.var_q_del[e, 'M1', t] + model.var_q_arb[e, 'M2', t] - model.par_alpha * model.par_demand['M1', t] <= 0
model.equation = py.Constraint(model.set_e, model.set_t, rule=equation4)
   

def equation_9(model=None):
    t = model.set_t.first()
    return model.var_stock_stored[t] == 0
model.equation9 = py.Constraint(rule=equation_9)


def equation_10(model=None, t=None):
    return model.var_stock_stored[t] - model.var_stock_stored[t - 1] + model.var_stock_in_out[t - 1] == 0
model.equation10 = py.Constraint(model.set_t_stroke, rule=equation_10)


def equation5(model, e):
    return sum(model.var_q[e, m, t] 
               for m in model.set_market
               for t in model.set_t
           ) <= model.par_Q[e]
model.equation5 = py.Constraint(model.set_e, rule=equation5)


def equation_11(model=None, exporter=None, time=None):
    if exporter in model.set_e_stroke:
        return sum(model.var_q[exporter, market, time] for market in model.set_market) - model.var_q_bar[exporter, time] <= 0
    else:
        return sum(model.var_q[exporter, market, time] for market in model.set_market) - model.par_q_bar_emajor <= 0
model.equation11 = py.Constraint(model.set_e, model.set_t, rule=equation_11)


def equation12(model, e, t):
    if e in model.set_e_stroke:
        return model.var_q_diff[e, t] == model.var_q_bar[e, t] - sum(model.var_q[e, m, t] for m in model.set_market)
    else: 
        return model.var_q_diff[e, t] == model.par_q_bar_emajor - sum(model.var_q[e, m, t] for m in model.set_market) 
model.equation12 = py.Constraint(model.set_e, model.set_t, rule=equation12)

def equation13(model, e, t):
    return model.var_q_add[e, t] <= 0.1 * (model.var_q_bar[e, t] - model.var_q_diff[e, t])
model.equation13 = py.Constraint(model.set_e_stroke, model.set_t, rule=equation13)


def equation14(model, e, t):
    return model.var_q_bar[e, t] == model.var_q_bar[e, t-1] + model.var_q_add[e, t-1] - model.var_q_bar_retire[e, t-1]
model.equation14 = py.Constraint(model.set_e_stroke, model.set_t_stroke, rule=equation14)


def equation15(model):
    _t_end = model.set_t.last()
    return model.var_stock_stored[_t_end] - model.var_stock_in_out[_t_end] == 0
model.equation15 = py.Constraint(rule=equation15)


def equation16(model, e):
    _t_start = model.set_t.first()
    return model.var_q_bar[e, _t_start] == model.par_q_bar_e_stroke[e]
model.equation16 = py.Constraint(model.set_e_stroke, rule=equation16)

def equation17(model, e, t):
    _init_year = model.set_t.first()
    return model.var_q_bar_retire[e, t] <= 0.25 * model.var_q_bar[e, _init_year]
model.constraint17 = py.Constraint(model.set_e_stroke, model.set_t, rule=equation17)

# def equation_4(model=None, m=None, t=None):
#     _mexp = model.set_mexporter.first()
#     return model.var_q_del[m, t] + model.var_q_arb_major[m, t] - model.var_q[_mexp, m, t] == 0
# model.equation4 = py.Constraint(model.set_market, model.set_t, rule=equation_4)


# def equation_5(model=None, t=None):
#     return sum(model.var_q[e, 'M1', t] for e in model.set_e_stroke) + model.var_q_del['M1', t] + model.var_q_arb_major['M2', t] + model.var_stock_in_out[t] - model.par_demand['M1', t] == 0
# model.equation5 = py.Constraint(model.set_t, rule=equation_5)


# def equation_6(model=None, t=None):
#     return sum(model.var_q[e, 'M2', t] for e in model.set_e_stroke) + model.var_q_del['M2', t] + model.var_q_arb_major['M1', t] - model.par_demand['M2', t] == 0
# model.equation6 = py.Constraint(model.set_t, rule=equation_6)


# def equation_8(model=None, t=None):
#     return model.var_q_del['M1', t] + model.var_q_arb_major['M2', t] - model.par_alpha * model.par_demand['M1', t] <= 0
# model.equation8 = py.Constraint(model.set_t, rule=equation_8)








"""
    SOLVE THE MODEL
"""


def objective_func(model=None):

    _sec_term = sum(
        model.par_c_main_e_stroke[e] * model.var_q_bar[e, t]
        for e in model.set_e_stroke
        for t in model.set_t
    )
    
    _thr_term = sum(
        model.par_c_stock() * model.var_stock_stored[t]
        for t in model.set_t
    )
    
    _first_term_major = sum(
        model.par_c_snake[e] * model.var_q[e, m, t]
        for e in model.set_mexporter
        for m in model.set_market
        for t in model.set_t
    )
    
    _first_term_fringe = sum(
        model.par_c_gen_e_t[e] * model.var_q[e, m, t]
        for e in model.set_e_stroke
        for m in model.set_market
        for t in model.set_t
    )
    
    return _first_term_major + _first_term_fringe + _sec_term + _thr_term


model.objective = py.Objective(expr=objective_func, sense=py.minimize)

solver = py.SolverFactory("gurobi")

model.write('lower_level.lp', io_options={"symbolic_solver_labels": True})

solution = solver.solve(model, tee=False, warmstart=True)

# model.objective.display()
print("Primal problem: {:.0f}".format(model.objective()))

# for _year in model.set_t:
#     print(_year)
#     print('Stock stored: {:.3f}'.format(model.var_stock_stored[_year]()))
#     for _market in model.set_market:
#         print(_market)
#         if _market == 'M1':
#             _other_market = 'M2'
#         else:
#             _other_market = 'M1'
#         _delivered = sum(model.var_q_del[e, _market, _year]() + model.var_q_arb[e, _other_market, _year]() for e in model.set_e)
#         print('Exporter: {:.3f}'.format(_delivered))
#         print('Demand: {:.3f}'.format(model.par_demand[_market, _year]))
#         if _market == 'M1':
#             print('Stock (in/out) : {:.3f}'.format(model.var_stock_in_out[_year]()))
#         print('')

dict_var_q = dict()
for _e in model.set_e:
    for _m in model.set_market:
        if _m == 'M1':
            _other_market = 'M2'
        else:
            _other_market = 'M1'
        for _t in model.set_t:
            dict_var_q[_e, _m, _t] = model.var_q_del[_e, _m, _t]() + model.var_q_arb[_e, _other_market, _t]()




_data_var_q = [(key[0], key[1], key[2], value) for key, value in dict_var_q.items()]

_df = pd.DataFrame(_data_var_q, columns=['Exporter', 'Market', 'Year', 'Value'])
_df.to_excel('quantities.xlsx', index=None)


dict_demand = dict()        
for _year in model.set_t:
    for _market in model.set_market:
        dict_demand[_market, _year] = model.par_demand[_market, _year]
    
_data_demand = [(key[0], key[1], value) for key, value in dict_demand.items()]
_df = pd.DataFrame(_data_demand, columns=['Market', 'Year', 'Value'])
_df.to_excel('demand.xlsx', index=None)    

dict_q_bar = dict()
for _e in model.set_e_stroke:
    for _year in model.set_t:
        dict_q_bar[_e, _year] = model.var_q_bar[_e, _year]()     
_data_bar = [(key[0], key[1], value) for key, value in dict_q_bar.items()]
_df = pd.DataFrame(_data_bar, columns=['Exporter', 'Year', 'Value'])
_df.to_excel('capacities.xlsx', index=None)



for market in model.set_market:
    _year = list(model.set_t)
    _data = {'Year': _year}
    _df = pd.DataFrame(_data)

    for exporter in model.set_e_stroke:
        _temp = [np.around(model.var_q_bar[exporter, _y](), 2) for _y in model.set_t]
        if sum(_temp) != 0:
            _df['Q_Bar|'+exporter] = _temp
    _temp = [np.around(model.par_q_bar_emajor(), 2) for _y in model.set_t]
    _df['Q_Bar|'+model.set_mexporter.first()] = _temp

    for _ex in model.set_e:
        _temp = [np.around(model.var_q_del[_ex, market, _y](), 2) for _y in model.set_t]
        if sum(_temp) != 0:
            _df['Q_Del|' + _ex] = _temp
        if market == 'M1':
            _other_market = 'M2'
        else:
            _other_market = 'M1'
        _temp = [np.around(model.var_q_arb[_ex, _other_market, _y](), 2) for _y in model.set_t]
        if sum(_temp) != 0:
            _df['Q_Arb|' + _ex] = _temp

    if market == 'M1':
        _temp = [np.around(model.var_stock_in_out[_y](), 2) for _y in model.set_t]
        _df['Stock_in_out|'] = _temp

    _df['Demand'] = [np.around(model.par_demand[market, _year], 2) for _year in model.set_t]

    if market == 'M1':
        _temp = [model.dual[model.equation2[year]] for year in model.set_t]
    else:
        _temp = [model.dual[model.equation3[year]] for year in model.set_t]

    _df['Dual'] = _temp

    _df.to_excel(market+'_overview.xlsx', index=None)








# model.var_q = py.Var(
#     model.set_e,
#     model.set_market,
#     model.set_t,
#     within=py.NonNegativeReals,
#     doc="VAR: (q_e_m_t).",
# )

# model.var_q_bar = py.Var(
#     model.set_e_stroke,
#     model.set_t,
#     within=py.NonNegativeReals,
#     doc="VAR: (q_bar_e_stroke_t).",
# )

# model.var_q_del = py.Var(
#     model.set_e, 
#     model.set_market,
#     model.set_t,
#     within=py.NonNegativeReals
# )

# model.var_q_arb = py.Var(
#     model.set_e, 
#     model.set_market,
#     model.set_t,
#     within=py.NonNegativeReals
# )

# model.var_stock_stored = py.Var(
#     model.set_t, within=py.NonNegativeReals, doc="VAR: (q_stock_stored_M1_t)."
# )

# model.var_stock_in_out = py.Var(model.set_t, doc="VAR: (q_stock_in_out_M1_t).")

# model.var_q_add = py.Var(
#     model.set_e_stroke,
#     model.set_t,
#     within=py.NonNegativeReals,
#     doc="VAR: (q_bar_add_e_stroke_t).",
# )

# model.var_q_bar_retire = py.Var(
#     model.set_e_stroke,
#     model.set_t,
#     within=py.NonNegativeReals,
#     doc="VAR: (q_bar_retire_e_stroke_t).",
# )

# model.var_q_diff = py.Var(
#     model.set_e,
#     model.set_t,
#     within=py.NonNegativeReals
        
# )







    # print('Delivered major: {:.3f}'.format(model.var_q_del['M1', _year]()))
    # print('Arbitrage major: {:.3f}'.format(model.var_q_arb_major['M2', _year]()))
    
#     print('Storage: {:.3f}'.format(model.var_stock_in_out[_year]()))
#     print('Demand: {:.3f}'.format(model.par_demand['M1', _year]))
#     print('')
#     print('Fringe M2: {:.3f}'.format(sum(model.var_q[e, 'M2', _year]() for e in model.set_e_stroke)))
#     print('Delivered major: {:.3f}'.format(model.var_q_del['M2', _year]()))
#     print('Arbitrage major: {:.3f}'.format(model.var_q_arb_major['M1', _year]()))
#     print('Demand: {:.3f}'.format(model.par_demand['M2', _year]))
#     print('________')



