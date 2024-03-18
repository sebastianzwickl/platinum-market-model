import utils
import numpy as np
import pyomo.environ as py
from datetime import datetime
import pandas as pd
import os


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
        if _row.Region == 'Recycling':
            _maintenance_costs_dict[_row.Region] = 0 * _maintenance_cost
        else:
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

model.set_embargo_m1 = py.Set(initialize=['Russia'])


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

model.var_stock_stored = py.Var(
    model.set_t, within=py.NonNegativeReals, doc="VAR: (q_stock_stored_M1_t)."
)

model.var_stock_out = py.Var(model.set_t, within=py.NonNegativeReals, doc="VAR: (q_stock_out_M1_t).")
model.var_stock_in = py.Var(model.set_t, within=py.NonNegativeReals, doc="VAR: (q_stock_in_M1_t).")

model.var_q_bar_exp = py.Var(
    model.set_e_stroke,
    model.set_t,
    within=py.NonNegativeReals,
    doc="VAR: (q_bar_exp)."
)

model.var_q_bar_retire = py.Var(
    model.set_e_stroke,
    model.set_t,
    within=py.NonNegativeReals,
    doc="VAR: (q_bar_retire)."
)


# DUAL (INEQUALITY)

model.var_mu1 = py.Var(model.set_e, model.set_t, domain=py.NonNegativeReals)
model.var_u1 = py.Var(model.set_e, model.set_t, domain=py.Binary)

model.var_mu2 = py.Var(model.set_e, domain=py.NonNegativeReals)
model.var_u2 = py.Var(model.set_e, domain=py.Binary)

model.var_mu3 = py.Var(model.set_e, model.set_t, domain=py.NonNegativeReals)
model.var_u3 = py.Var(model.set_e, model.set_t, domain=py.Binary)

model.var_mu4 = py.Var(model.set_e_stroke, model.set_t, domain=py.NonNegativeReals)
model.var_u4 = py.Var(model.set_e_stroke, model.set_t, domain=py.Binary)

model.var_mu5 = py.Var(model.set_e_stroke, model.set_t, domain=py.NonNegativeReals)
model.var_u5 = py.Var(model.set_e_stroke, model.set_t, domain=py.Binary)

model.var_mu6 = py.Var(model.set_e, model.set_market, model.set_t, domain=py.NonNegativeReals)
model.var_u6 = py.Var(model.set_e, model.set_market, model.set_t, domain=py.Binary)

model.var_mu7 = py.Var(model.set_t, domain=py.NonNegativeReals)
model.var_u7 = py.Var(model.set_t, domain=py.Binary)

model.var_mu8 = py.Var(model.set_t, domain=py.NonNegativeReals)
model.var_u8 = py.Var(model.set_t, domain=py.Binary)

model.var_mu9 = py.Var(model.set_t, domain=py.NonNegativeReals)
model.var_u9 = py.Var(model.set_t, domain=py.Binary)

model.var_mu10 = py.Var(model.set_e_stroke, model.set_t, domain=py.NonNegativeReals)
model.var_u10 = py.Var(model.set_e_stroke, model.set_t, domain=py.Binary)

model.var_mu11 = py.Var(model.set_e_stroke, model.set_t, domain=py.NonNegativeReals)
model.var_u11 = py.Var(model.set_e_stroke, model.set_t, domain=py.Binary)

model.var_mu12 = py.Var(model.set_e_stroke, model.set_t, domain=py.NonNegativeReals)
model.var_u12 = py.Var(model.set_e_stroke, model.set_t, domain=py.Binary)


# DUAL (EQUALITY)

model.var_lambda_1 = py.Var(model.set_t)
model.var_lambda_2 = py.Var(model.set_t)
model.var_lambda_3 = py.Var(model.set_t_stroke)
model.var_lambda_4 = py.Var()
model.var_lambda_10 = py.Var()
model.var_lambda_5 = py.Var(model.set_e_stroke, model.set_t_stroke)
model.var_lambda_6 = py.Var(model.set_e_stroke)
model.var_lambda_7 = py.Var()
model.var_lambda_8 = py.Var()
model.var_lambda_9 = py.Var(model.set_embargo_m1, model.set_t)


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
    "Russia": 24,
    "Zimbabwe": 17,
    "North America": 10.5,
    "World": 2,
    "Recycling" : 50,
    "Slack exporter" : 5
}

model.par_q_bar_e_stroke = py.Param(
    model.set_e_stroke,
    initialize=_dict_q_bar_e_stroke_t_stroke,
    doc="PAR: initial maximum export capacity of the fringe suppliers.",
)


model.par_q_bar_emajor = py.Param(
    initialize=140, doc="PAR: maximum export capacity of the major exporter."
)


_reserves = pd.read_excel("input data/platinum-group metal reserves.xlsx", sheet_name="Data")
_dict_Q = dict()
for _i, _r in _reserves.iterrows():
    _dict_Q[_r.Region] = _r.Value
_dict_Q['North America'] = _dict_Q['United States'] + _dict_Q['Canada']
_dict_Q.pop('United States')
_dict_Q.pop('Canada')
_dict_Q['Recycling'] = 50000
_dict_Q['Slack exporter'] = 50000

model.par_Q = py.Param(
    model.set_e,
    initialize=_dict_Q,
    doc="PAR: maximum total reserves.",
)

model.par_big_m = py.Param(initialize=10e8)
model.par_beta_add = py.Param(initialize=0.075)
model.par_beta_retire = py.Param(initialize=0.25)

"""
##############################################################################
"""   
""" (E) ADD CONSTRAINTS """
"""
##############################################################################
"""

"""
    EQUALITY CONSTRAINTS (LAMBDA)
"""


def equation2(model, t):
    return sum(model.var_q[e, "M1", t]
               for e in model.set_e) + model.var_stock_out[t] - model.var_stock_in[t] - model.par_demand['M1', t] == 0


def equation3(model, t):
    return sum(model.var_q[e, "M2", t] for e in model.set_e) - model.par_demand['M2', t] == 0


def equation_10(model=None, t=None):
    return model.var_stock_stored[t] - model.var_stock_stored[t - 1] + model.var_stock_out[t - 1] - model.var_stock_in[t - 1] == 0


def equation_9(model=None):
    return model.var_stock_stored[model.set_t.first()] == 0


def no_discharge_of_initial_stock(model):
    return model.var_stock_out[model.set_t.first()] == 0


def initial_q_bar_capacity(model, e):
    return model.var_q_bar[e, model.set_t.first()] - model.par_q_bar_e_stroke[e] == 0


def equation15(model):
    return model.var_stock_out[model.set_t.last()] - model.var_stock_stored[model.set_t.last()] == 0


def equation16(m):
    return model.var_stock_in[model.set_t.last()] == 0


def equation17(m, exp, time):
    return model.var_q[exp, 'M1', time] == 0


def equation14(model, e, t):
    return model.var_q_bar[e, t] - model.var_q_bar[e, t-1] - model.var_q_bar_exp[e, t-1] + model.var_q_bar_retire[e, t-1] == 0


model.eq_demand_balance_m1 = py.Constraint(model.set_t, rule=equation2, doc='CHECKED')
model.eq_demand_balance_m2 = py.Constraint(model.set_t, rule=equation3, doc='CHECKED')
model.eq_stock_balance = py.Constraint(model.set_t_stroke, rule=equation_10, doc='CHECKED')
model.eq_empty_initial_stock = py.Constraint(rule=equation_9, doc='CHECKED')
model.eq_empty_stock_at_beginning = py.Constraint(rule=no_discharge_of_initial_stock, doc='CHECKED')
model.eq_capacity_expansion = py.Constraint(model.set_e_stroke, model.set_t_stroke, rule=equation14, doc='CHECKED')
model.eq_initial_q_bar_capacity = py.Constraint(model.set_e_stroke, rule=initial_q_bar_capacity, doc='CHECKED')
model.eq_fully_discharge_stock = py.Constraint(rule=equation15, doc='CHECKED')
model.eq_no_charge_of_stock_final_time_step = py.Constraint(rule=equation16, doc='CHECKED')
model.eq_embargo_market_m1 = py.Constraint(model.set_embargo_m1, model.set_t, rule=equation17, doc='CHECKED')


# def equation4(model, e, t):
#     return model.var_q[e, 'M1', t] - model.par_alpha * model.par_demand['M1', t] <= 0
# model.eq_share_limit_exporter_m1 = py.Constraint(model.set_e, model.set_t, rule=equation4, doc='CHECKED')


# def equation5(model, e):
#     return sum(model.var_q[e, m, t]
#                 for m in model.set_market
#                 for t in model.set_t
#             ) <= model.par_Q[e]
# model.eq_exporter_reserve_limit = py.Constraint(model.set_e, rule=equation5, doc='CHECKED')


# def equation_11(model=None, exporter=None, time=None):
#     if exporter in model.set_e_stroke:
#         return sum(model.var_q[exporter, market, time] for market in model.set_market) - model.var_q_bar[exporter, time] <= 0
#     else:
#         return sum(model.var_q[exporter, market, time] for market in model.set_market) - model.par_q_bar_emajor <= 0
# model.eq_exporter_capacity_limit = py.Constraint(model.set_e, model.set_t, rule=equation_11, doc='CHECKED')


# def upper_bound_exp_retire(model, e, t):
#     return model.var_q_bar_exp[e, t] <= 0.075 * sum(model.var_q[e, m, t] for m in model.set_market)
# model.eq_upper_bound_exp = py.Constraint(model.set_e_stroke, model.set_t, rule=upper_bound_exp_retire, doc='CHECKED')


# def lower_bound_exp_retire(model, e, t):
#     _init_year = model.set_t.first()
#     return model.var_q_bar_retire[e, t] - 0.25 * model.par_q_bar_e_stroke[e] <= 0
# model.eq_upper_bound_retire = py.Constraint(model.set_e_stroke, model.set_t, rule=lower_bound_exp_retire, doc='CHECKED')


def comp_1_a(m, e, t):
    return m.var_mu1[e, t] <= m.par_big_m * m.var_u1[e, t]


def comp_1_b(m, e, t):
    return 0 <= m.par_alpha * m.par_demand['M1', t] - m.var_q[e, 'M1', t]


def comp_1_c(m, e, t):
    return m.par_alpha * m.par_demand['M1', t] - m.var_q[e, 'M1', t] <= m.par_big_m * (1 - m.var_u1[e, t])


model.comp_1_a = py.Constraint(model.set_e, model.set_t, rule=comp_1_a)
model.comp_1_b = py.Constraint(model.set_e, model.set_t, rule=comp_1_b)
model.comp_1_c = py.Constraint(model.set_e, model.set_t, rule=comp_1_c)


def comp_2_a(m, e):
    return m.var_mu2[e] <= m.par_big_m * m.var_u2[e]


def comp_2_b(m, e):
    return 0 <= m.par_Q[e] - sum(m.var_q[e, ma, t] 
                                 for ma in m.set_market
                                 for t in m.set_t)


def comp_2_c(m, e):
    return m.par_Q[e] - sum(m.var_q[e, ma, t] 
                                 for ma in m.set_market
                                 for t in m.set_t) <= m.par_big_m * (1 - m.var_u2[e])


model.comp_2_a = py.Constraint(model.set_e, rule=comp_2_a)
model.comp_2_b = py.Constraint(model.set_e, rule=comp_2_b)
model.comp_2_c = py.Constraint(model.set_e, rule=comp_2_c)


def comp_3_a(m, e, t):
    return m.var_mu3[e, t] <= m.par_big_m * m.var_u3[e, t]


def comp_3_b(m, e, t):
    if e in m.set_e_stroke:    
        return 0 <= m.var_q_bar[e, t] - sum(m.var_q[e, ma, t] for ma in m.set_market)
    else:
        return 0 <= m.par_q_bar_emajor - sum(m.var_q[e, ma, t] for ma in m.set_market)


def comp_3_c(m, e, t):
    if e in m.set_e_stroke:    
        return m.var_q_bar[e, t] - sum(m.var_q[e, ma, t] for ma in m.set_market) <= m.par_big_m * (1 - m.var_u3[e, t])
    else:
        return m.par_q_bar_emajor - sum(m.var_q[e, ma, t] for ma in m.set_market) <= m.par_big_m * (1 - m.var_u3[e, t])


model.comp_3_a = py.Constraint(model.set_e, model.set_t, rule=comp_3_a)
model.comp_3_b = py.Constraint(model.set_e, model.set_t, rule=comp_3_b)
model.comp_3_c = py.Constraint(model.set_e, model.set_t, rule=comp_3_c)


def comp_4_a(m, e, t):
    return m.var_mu4[e, t] <= m.par_big_m * m.var_u4[e, t]


def comp_4_b(m, e, t):
    return 0 <= m.par_beta_add * sum(m.var_q[e, ma, t] for ma in m.set_market) - m.var_q_bar_exp[e, t]


def comp_4_c(m, e, t):
    return m.par_beta_add * sum(m.var_q[e, ma, t] for ma in m.set_market) - m.var_q_bar_exp[e, t] <= m.par_big_m * (1 - m.var_u4[e, t])


model.comp_4_a = py.Constraint(model.set_e_stroke, model.set_t, rule=comp_4_a)
model.comp_4_b = py.Constraint(model.set_e_stroke, model.set_t, rule=comp_4_b)
model.comp_4_c = py.Constraint(model.set_e_stroke, model.set_t, rule=comp_4_c)


def comp_5_a(m, e, t):
    return m.var_mu5[e, t] <= m.par_big_m * m.var_u5[e, t]


def comp_5_b(m, e, t):
    return 0 <= m.par_beta_retire * m.par_q_bar_e_stroke[e] - m.var_q_bar_retire[e, t]


def comp_5_c(m, e, t):
    return m.par_beta_retire * m.par_q_bar_e_stroke[e] - m.var_q_bar_retire[e, t] <= m.par_big_m * (1 - m.var_u5[e, t])


model.comp_5_a = py.Constraint(model.set_e_stroke, model.set_t, rule=comp_5_a)
model.comp_5_b = py.Constraint(model.set_e_stroke, model.set_t, rule=comp_5_b)
model.comp_5_c = py.Constraint(model.set_e_stroke, model.set_t, rule=comp_5_c)


def comp_6_a(mo, e, m, t):
    return mo.var_mu6[e, m, t] <= mo.par_big_m * mo.var_u6[e, m, t]


def comp_6_b(mo, e, m, t):
    return mo.var_q[e, m, t] <= mo.par_big_m * (1 - mo.var_u6[e, m, t])


model.comp_6_a = py.Constraint(model.set_e, model.set_market, model.set_t, rule=comp_6_a)
model.comp_6_b = py.Constraint(model.set_e, model.set_market, model.set_t, rule=comp_6_b)


def comp_7_a(m, t):
    return m.var_mu7[t] <= m.par_big_m * m.var_u7[t]


def comp_7_b(m, t):
    return m.var_stock_stored[t] <= m.par_big_m * (1- m.var_u7[t])


model.comp_7_a = py.Constraint(model.set_t, rule=comp_7_a)
model.comp_7_b = py.Constraint(model.set_t, rule=comp_7_b)


def comp_8_a(m, t):
    return m.var_mu8[t] <= m.par_big_m * m.var_u8[t]


def comp_8_b(m, t):
    return m.var_stock_out[t] <= m.par_big_m * (1 - m.var_u8[t])


model.comp_8_a = py.Constraint(model.set_t, rule=comp_8_a)
model.comp_8_b = py.Constraint(model.set_t, rule=comp_8_b)


def comp_9_a(m, t):
    return m.var_mu9[t] <= m.par_big_m * m.var_u9[t]


def comp_9_b(m, t):
    return m.var_stock_in[t] <= m.par_big_m * (1 - m.var_u9[t])


model.comp_9_a = py.Constraint(model.set_t, rule=comp_9_a)
model.comp_9_b = py.Constraint(model.set_t, rule=comp_9_b)


def comp_10_a(m, e, t):
    return m.var_mu10[e, t] <= m.par_big_m * m.var_u10[e, t]


def comp_10_b(m, e, t):
    return m.var_q_bar[e, t] <= m.par_big_m * (1 - m.var_u10[e, t])


model.comp_10_a = py.Constraint(model.set_e_stroke, model.set_t, rule=comp_10_a)
model.comp_10_b = py.Constraint(model.set_e_stroke, model.set_t, rule=comp_10_b)


def comp_11_a(m, e, t):
    return m.var_mu11[e, t] <= m.par_big_m * m.var_u11[e, t]


def comp_11_b(m, e, t):
    return m.var_q_bar_exp[e, t] <= m.par_big_m * (1 - m.var_u11[e, t])


model.comp_11_a = py.Constraint(model.set_e_stroke, model.set_t, rule=comp_11_a)
model.comp_11_b = py.Constraint(model.set_e_stroke, model.set_t, rule=comp_11_b)


def comp_12_a(m, e, t):
    return m.var_mu12[e, t] <= m.par_big_m * m.var_u12[e, t]


def comp_12_b(m, e, t):
    return m.var_q_bar_retire[e, t] <= m.par_big_m * (1 - m.var_u12[e, t])


model.comp_12_a = py.Constraint(model.set_e_stroke, model.set_t, rule=comp_12_a)
model.comp_12_b = py.Constraint(model.set_e_stroke, model.set_t, rule=comp_12_b)













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

model.write('1_equations.lp', io_options={"symbolic_solver_labels": True})

solution = solver.solve(model, tee=False, warmstart=True)

# model.objective.display()
print("Primal problem: {:.0f}".format(model.objective()))


for market in model.set_market:
    _year = list(model.set_t)
    _data = {'Year': _year}
    _df = pd.DataFrame(_data)

    for exporter in model.set_e_stroke:
        """INSTALLED EXPORT CAPACITY OF FRINGE EXPORTERS"""
        _temp = [np.around(model.var_q_bar[exporter, _y](), 2) for _y in model.set_t]
        if sum(_temp) != 0:
            _df['Q_Bar|'+exporter] = _temp

    """INSTALLED EXPORT CAPACITY OF MAJOR EXPORTER"""
    _temp = [np.around(model.par_q_bar_emajor(), 2) for _y in model.set_t]
    _df['Q_Bar|'+model.set_mexporter.first()] = _temp

    """EXPORT QUANTITY OF ALL EXPORTERS"""
    for _ex in model.set_e:
        _temp = [np.around(model.var_q[_ex, market, _y](), 2) for _y in model.set_t]
        _df['Q|'+ _ex] = _temp

    """STORAGE"""
    if market == 'M1':
        _temp = [np.around(model.var_stock_in[_y](), 2) for _y in model.set_t]
        _df['Stock_in'] = _temp
        _temp = [np.around(model.var_stock_out[_y](), 2) for _y in model.set_t]
        _df['Stock_out|'] = _temp
        _temp = [np.around(model.var_stock_stored[_y](), 2) for _y in model.set_t]
        _df['Stock_stored|'] = _temp

    """DEMAND"""
    _df['Demand'] = [np.around(model.par_demand[market, _year], 2) for _year in model.set_t]

    # if market == 'M1':
    #     _temp = [model.dual[model.eq_demand_balance_m1[year]] for year in model.set_t]
    # else:
    #     _temp = [model.dual[model.eq_demand_balance_m2[year]] for year in model.set_t]

    # _df['Shadow price'] = _temp

    _df.to_excel('2_'+market+'_overview.xlsx', index=None)
