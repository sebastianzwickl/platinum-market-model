import pandas as pd
import pyomo.environ as py


def get_demand_data_for_both_markets(_demand=None, factor=None):

    _dict_demand_EU = dict()
    _dict_demand_world = dict()

    _demand_EU = _demand.loc[_demand.Region == "EU/EU+"]
    _demand_World = _demand.loc[_demand.Region == "World"]

    _market = "M1"
    for _year in range(2025, 2051, 1):
        if _year < 2030:
            _v2020 = _demand_EU.loc[_demand_EU.Year == 2020]["Value"].item()
            _v2030 = _demand_EU.loc[_demand_EU.Year == 2030]["Value"].item()
            _diff = _v2020 - _v2030
            _v20xx = _v2020 - (_diff / 10) * (_year - 2020)
            _dict_demand_EU[_market, _year] = _v20xx * factor
        elif _year == 2030:
            _v2030 = _demand_EU.loc[_demand_EU.Year == 2030]["Value"].item()
            _dict_demand_EU[_market, _year] = _v2030 * factor
        else:
            _v2030 = _demand_EU.loc[_demand_EU.Year == 2030]["Value"].item()
            _v2050 = _demand_EU.loc[_demand_EU.Year == 2050]["Value"].item()
            _diff = _v2050 - _v2030
            _v20xx = _v2030 + (_diff / 20) * (_year - 2030)
            _dict_demand_EU[_market, _year] = _v20xx * factor

    _market = "M2"
    for _year in range(2025, 2051, 1):
        if _year < 2030:
            _v2020 = _demand_World.loc[_demand_World.Year == 2020]["Value"].item()
            _v2030 = _demand_World.loc[_demand_World.Year == 2030]["Value"].item()
            _diff = _v2020 - _v2030
            _v20xx = _v2020 - (_diff / 10) * (_year - 2020)
            _dict_demand_world[_market, _year] = _v20xx - _dict_demand_EU["M1", _year]
        elif _year == 2030:
            _v2030 = _demand_World.loc[_demand_World.Year == 2030]["Value"].item()
            _dict_demand_world[_market, _year] = _v2030 - _dict_demand_EU["M1", _year]
        else:
            _v2030 = _demand_World.loc[_demand_World.Year == 2030]["Value"].item()
            _v2050 = _demand_World.loc[_demand_World.Year == 2050]["Value"].item()
            _diff = _v2050 - _v2030
            _v20xx = _v2030 + (_diff / 20) * (_year - 2030)
            _dict_demand_world[_market, _year] = _v20xx - _dict_demand_EU["M1", _year]

    return _dict_demand_EU, _dict_demand_world


def add_decision_variables_vector_x(model=None):

    # SETS
    # ... set_e
    # ... set_e_stroke
    # ... set_market
    # ... set_t
    # ... set_t_stroke
    # ... set_mexporter

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
    model.var_q_bar_add = py.Var(
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
    model.var_q_arb = py.Var(
        model.set_t, doc="VAR: (q_arb_M1_M2_t)."
    )
    model.var_q_del = py.Var(
        model.set_market,
        model.set_t,
        within=py.NonNegativeReals,
        doc="VAR: (q_del_1_m_t).",
    )
    model.var_q_arb_major = py.Var(
        model.set_market,
        model.set_t,
        within=py.NonNegativeReals,
        doc="VAR: (q_arb_1_m_t).",
    )
    model.var_stock_in_out = py.Var(model.set_t, doc="VAR: (q_stock_in_out_M1_t).")
    model.var_stock_stored = py.Var(
        model.set_t, within=py.NonNegativeReals, doc="VAR: (q_stock_stored_M1_t)."
    )

    return


def add_decision_variables_vector_lambda(model=None):
    # SETS
    # ... set_e
    # ... set_e_stroke
    # ... set_market
    # ... set_t
    # ... set_t_stroke
    # ... set_mexporter

    model.var_lambda_4 = py.Var(
        model.set_market, model.set_t, doc="VAR: (lambda_4_m_t)."
    )

    model.var_lambda_5 = py.Var(model.set_t, doc="VAR: (lambda_5_t).")

    model.var_lambda_6 = py.Var(model.set_t, doc="VAR: (lambda_6).")

    model.var_lambda_7 = py.Var(
        model.set_embargo_m1, model.set_t, doc="VAR: (lambda_7_e_underline_t)."
    )

    model.var_lambda_9 = py.Var(doc="VAR: (lambda_9).")

    model.var_lambda_10 = py.Var(model.set_t_stroke, doc="VAR: (lambda_10_t_stroke).")
    return


def add_decision_variables_vector_mhu(model=None):

    model.var_mhu_3 = py.Var(
        model.set_e, model.set_t, domain=py.NonNegativeReals, doc="VAR: (mhu_3_e_t)."
    )

    model.var_mhu_8 = py.Var(
        model.set_t, domain=py.NonNegativeReals, doc="VAR: (mhu_8_t)."
    )

    model.var_mhu_11 = py.Var(
        model.set_e,
        model.set_market,
        model.set_t,
        domain=py.NonNegativeReals,
        doc="VAR: (mhu_11_e_m_t).",
    )

    model.var_mhu_12 = py.Var(
        model.set_e_stroke,
        model.set_t,
        domain=py.NonNegativeReals,
        doc="VAR: (mhu_12_e_stroke_t).",
    )

    model.var_mhu_13 = py.Var(
        model.set_market,
        model.set_t,
        domain=py.NonNegativeReals,
        doc="VAR: (mhu_13_m_t).",
    )

    model.var_mhu_14 = py.Var(
        model.set_market,
        model.set_t,
        domain=py.NonNegativeReals,
        doc="VAR: (mhu_14_m_t).",
    )

    model.var_mhu_15 = py.Var(
        model.set_t, domain=py.NonNegativeReals, doc="VAR: (mhu_15_t)."
    )

    return


def add_decision_variables_vector_y(model=None):

    model.var_c_1 = py.Var(model.set_t, within=py.NonNegativeReals, doc="VAR: (c_1_t).")

    model.var_q_bar_1 = py.Var(
        model.set_t, within=py.NonNegativeReals, doc="VAR: (q_bar_1_t)."
    )

    return


def add_decision_variables_vector_u(model=None):

    model.var_u_3 = py.Var(
        model.set_e, model.set_t, within=py.Binary, doc="VAR: (u_3_e_t)."
    )

    model.var_u_8 = py.Var(model.set_t, within=py.Binary, doc="VAR: (u_8_t).")

    model.var_u_11 = py.Var(
        model.set_e,
        model.set_market,
        model.set_t,
        within=py.Binary,
        doc="VAR: (u_11_e_m_t).",
    )

    model.var_u_12 = py.Var(
        model.set_e_stroke, model.set_t, within=py.Binary, doc="VAR: (u_12_e_stroke_t)."
    )

    model.var_u_13 = py.Var(
        model.set_market, model.set_t, within=py.Binary, doc="VAR: (u_13_m_t)."
    )

    model.var_u_14 = py.Var(
        model.set_market, model.set_t, within=py.Binary, doc="VAR: (u_14_m_t)."
    )

    model.var_u_15 = py.Var(model.set_t, within=py.Binary, doc="VAR: (u_15_t).")

    return


def add_decision_variables_vector_sigma(model=None):

    # A.2.4 Linear reformulation

    model.var_sigma = py.Var(
        model.set_e_stroke,
        model.set_market,
        model.set_t,
        within=py.Binary,
        doc="VAR: (sigma_e_m_t).",
    )

    model.var_lambda_snake_5 = py.Var(
        model.set_e_stroke, model.set_t, doc="VAR: (lambda_snake_5_e_t)."
    )

    model.var_lambda_snake_6 = py.Var(
        model.set_e_stroke, model.set_t, doc="VAR: (lambda_snake_6_e_t)."
    )

    model.var_sigma_snake = py.Var(
        model.set_e_stroke,
        model.set_market,
        model.set_t,
        within=py.Binary,
        doc="VAR: (sigma_snake_e_m_t).",
    )

    return


def add_decision_variables_vector_z(model=None):

    model.var_z = py.Var(
        model.set_e_stroke,
        model.set_market,
        model.set_t,
        within=py.NonNegativeReals,
        doc="VAR: (z_e_stroke_m_t).",
    )

    return
