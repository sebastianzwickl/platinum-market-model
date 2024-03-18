import pyomo.environ as py


def eq_40_major(model, e, m, t):
    # note that there is no embargo for the major exporter considered.
    return (
        model.var_c_1[t]
        - model.var_lambda_4[m, t]
        + model.var_mhu_3[e, t]
        - model.var_mhu_11[e, m, t]
        == 0
    )


def eq_40_fringe_m1(model, e, t):
    if e in model.set_embargo_m1:
        # embargo on exporter
        return (
            model.par_c_gen_e_t[e]
            + model.var_lambda_5[t]
            + model.var_lambda_7[e, t]
            + model.var_mhu_3[e, t]
            - model.var_mhu_11[e, "M1", t]
            == 0
        )
    else:
        # no embargo on exporter
        return (
            model.par_c_gen_e_t[e]
            + model.var_lambda_5[t]
            + model.var_mhu_3[e, t]
            - model.var_mhu_11[e, "M1", t]
            == 0
        )


def eq_40_fringe_m2(model, e, t):
    # note that there is no embargo for the major exporter considered.
    return (
        model.par_c_gen_e_t[e]
        + model.var_lambda_6[t]
        + model.var_mhu_3[e, t]
        - model.var_mhu_11[e, "M2", t]
        == 0
    )


def eq_41(model, e, t):
    return (
        model.par_c_main_e_stroke[e] - model.var_mhu_3[e, t] - model.var_mhu_12[e, t]
        == 0
    )


def eq_42(model, t):
    return -model.var_lambda_5[t] + model.var_lambda_6[t] == 0


def eq_43_m1(model, t):
    return (
        model.var_lambda_4["M1", t]
        + model.var_lambda_5[t]
        + model.var_mhu_8[t]
        - model.var_mhu_13["M1", t]
        == 0
    )


def eq_43_m2(model, t):
    return (
        model.var_lambda_4["M2", t] + model.var_lambda_6[t] - model.var_mhu_13["M2", t]
        == 0
    )


def eq_44_m1(model, t):
    return (
        model.var_lambda_4["M1", t] + model.var_lambda_6[t] - model.var_mhu_14["M1", t]
        == 0
    )


def eq_44_m2(model, t):
    return (
        model.var_lambda_4["M1", t]
        + model.var_lambda_5[t]
        + model.var_mhu_8[t]
        - model.var_mhu_14["M2", t]
        == 0
    )


def eq_45(model=None, t=None):
    if t == model.set_t.last():
        return py.Constraint.Skip
    else:
        return model.var_lambda_5[t] + model.var_lambda_10[t+1] == 0


def eq_46(model=None, t=None):
    if t == model.set_t.first():
        return model.par_c_stock + model.var_lambda_9 - model.var_lambda_10[t + 1] - model.var_mhu_15[t] == 0
    elif t == model.set_t.last():
        return model.par_c_stock + model.var_lambda_10[t] - model.var_mhu_15[t] == 0
    else:
        return (
            model.par_c_stock + model.var_lambda_10[t] - model.var_lambda_10[t + 1] - model.var_mhu_15[t] == 0
        )


def add_equation_40(model):

    model.eq_40_1 = py.Constraint(
        model.set_mexporter,
        model.set_market,
        model.set_t,
        rule=eq_40_major,
        doc="Equation 40 (major supplier).",
    )

    model.eq_40_fringe_m1 = py.Constraint(
        model.set_e_stroke,
        model.set_t,
        rule=eq_40_fringe_m1,
        doc="Equation 40 (fringe supplier, european market).",
    )

    model.eq_40_fringe_m2 = py.Constraint(
        model.set_e_stroke,
        model.set_t,
        rule=eq_40_fringe_m2,
        doc="Equation 40 (fringe supplier, global market).",
    )
    return


def add_equation_41(model):
    model.eq_41 = py.Constraint(
        model.set_e_stroke, model.set_t, rule=eq_41, doc="Equation 41."
    )
    return


def add_equation_42(model):
    model.eq_42 = py.Constraint(model.set_t, rule=eq_42, doc="Equation 42.")
    return


def add_equation_43(model):
    model.eq_43_m1 = py.Constraint(
        model.set_t, rule=eq_43_m1, doc="Equation 43 (european market)."
    )

    model.eq_43_m2 = py.Constraint(
        model.set_t, rule=eq_43_m2, doc="Equation 43 (global market)."
    )
    return


def add_equation_44(model=None):
    model.eq_44_m1 = py.Constraint(
        model.set_t, rule=eq_44_m1, doc="Equation 44 (european market)."
    )

    model.eq_44_m2 = py.Constraint(
        model.set_t, rule=eq_44_m2, doc="Equation 44 (global market)."
    )

    return


def add_equation_45(model=None):
    model.eq_45 = py.Constraint(model.set_t, rule=eq_45, doc="Equation 45.")
    return


def add_equation_46(model=None):
    model.eq_46 = py.Constraint(model.set_t, rule=eq_46, doc="Equation 46.")
    return


def eq_54_1(m, e, t):
    return m.var_mhu_3[e, t] <= m.par_big_m * m.var_u_3[e, t]


def add_equation_54_1(model=None):
    model.eq_54_1 = py.Constraint(
        model.set_e_stroke, model.set_t, rule=eq_54_1, doc="Equation 54 (1)."
    )
    return


def eq_54_2_lower(m, e, t):
    if e in m.set_e_stroke:
        return (
            0
            <= sum(m.var_q[e, market, t] for market in m.set_market) - m.var_q_bar[e, t]
        )
    else:
        return (
            0
            <= sum(m.var_q[e, market, t] for market in m.set_market) - m.var_q_bar_1[t]
        )


def add_equation_54_2_lower(model=None):
    model.eq_54_2_lower = py.Constraint(
        model.set_e_stroke, model.set_t, rule=eq_54_2_lower, doc="Equation 54 (2; lower)."
    )


def eq_54_2_upper(m, e, t):
    if e in m.set_e_stroke:
        return sum(m.var_q[e, market, t] for market in m.set_market) - m.var_q_bar[
            e, t
        ] <= m.par_big_m * (1 - m.var_u_3[e, t])
    else:
        return sum(m.var_q[e, market, t] for market in m.set_market) - m.var_q_bar_1[
            t
        ] <= m.par_big_m * (1 - m.var_u_3[e, t])


def add_equation_54_2_upper(model=None):
    model.eq_54_2_upper = py.Constraint(
        model.set_e_stroke, model.set_t, rule=eq_54_2_upper, doc="Equation 54 (2; upper)."
    )
    return


def eq_55_1(m, t):
    return m.var_mhu_8[t] <= m.par_big_m * m.var_u_8[t]


def add_equation_55_1(model=None):
    model.eq_55_1 = py.Constraint(model.set_t, rule=eq_55_1, doc="Equation 55 (1).")
    return


def eq_55_2_lower(m, t):
    return (
        0
        <= m.var_q_del["M1", t]
        + m.var_q_arb_major["M2", t]
        - m.par_alpha * m.par_demand["M1", t]
    )


def add_equation_55_2_lower(model=None):
    model.eq_55_2_lower = py.Constraint(
        model.set_t, rule=eq_55_2_lower, doc="Equation 55 (2; lower)."
    )
    return


def eq_55_2_upper(m, t):
    return m.var_q_del["M1", t] + m.var_q_arb_major[
        "M2", t
    ] - m.par_alpha * m.par_demand["M1", t] <= m.par_big_m * (1 - m.var_u_8[t])


def add_equation_55_2_upper(model=None):
    model.eq_55_2_upper = py.Constraint(
        model.set_t, rule=eq_55_2_upper, doc="Equation 55 (2; upper)."
    )
    return


def eq_56_1(model, e, m, t):
    return model.var_mhu_11[e, m, t] <= model.par_big_m * model.var_u_11[e, m, t]


def add_56_1(model=None):
    model.eq_56_1 = py.Constraint(
        model.set_e, model.set_market, model.set_t, rule=eq_56_1, doc="Eq. 56 (1)."
    )
    return


def eq_56_2(model, e, m, t):
    return model.var_q[e, m, t] <= model.par_big_m * (1 - model.var_u_11[e, m, t])


def add_56_2(model=None):
    model.eq_56_2 = py.Constraint(
        model.set_e, model.set_market, model.set_t, rule=eq_56_2, doc="Eq. 56 (2)."
    )
    return


def eq_57_1(m, e, t):
    return m.var_mhu_12[e, t] <= m.par_big_m * m.var_u_12[e, t]


def add_57_1(model=None):
    model.eq_57_1 = py.Constraint(
        model.set_e_stroke, model.set_t, rule=eq_57_1, doc="Eq. 57 (1)."
    )
    return


def eq_57_2(m, e, t):
    return m.var_q_bar[e, t] <= m.par_big_m * (1 - m.var_u_12[e, t])


def add_57_2(model=None):
    model.eq_57_2 = py.Constraint(
        model.set_e_stroke, model.set_t, rule=eq_57_2, doc="Eq. 57 (2)."
    )
    return


def eq_58_1(m, market, t):
    return m.var_mhu_13[market, t] <= m.par_big_m * m.var_u_13[market, t]


def add_58_1(model=None):
    model.eq_58_1 = py.Constraint(
        model.set_market, model.set_t, rule=eq_58_1, doc="Eq. 58 (1)."
    )
    return


def eq_58_2(m, market, t):
    return m.var_q_del[market, t] <= m.par_big_m * (1 - m.var_u_13[market, t])


def add_58_2(model=None):
    model.eq_58_2 = py.Constraint(
        model.set_market, model.set_t, rule=eq_58_2, doc="Eq. 58 (2)."
    )
    return


def eq_59_1(m, market, t):
    return m.var_mhu_14[market, t] <= m.par_big_m * m.var_u_14[market, t]


def add_59_1(model=None):
    model.eq_59_1 = py.Constraint(
        model.set_market, model.set_t, rule=eq_59_1, doc="Eq. 59 (1)."
    )
    return


def eq_59_2(m, market, t):
    return m.var_q_arb_major[market, t] <= m.par_big_m * (1 - m.var_u_14[market, t])


def add_59_2(model=None):
    model.eq_59_2 = py.Constraint(
        model.set_market, model.set_t, rule=eq_59_2, doc="Eq. 59 (2)."
    )
    return


def eq_60_1(m, t):
    return m.var_mhu_15[t] <= m.par_big_m * m.var_u_15[t]


def add_60_1(model=None):
    model.eq_60_1 = py.Constraint(model.set_t, rule=eq_60_1, doc="Eq. 60 (1).")
    return


def eq_60_2(m, t):
    return m.var_stock_stored[t] <= m.par_big_m * (1 - m.var_u_15[t])


def add_60_2(model=None):
    model.eq_60_2 = py.Constraint(model.set_t, rule=eq_60_2, doc="Eq. 60 (2).")
    return


def eq_63(model, time):
    return model.var_q_bar_1[time] <= model.par_q_bar_emajor


def add_63(model=None):
    model.eq_63 = py.Constraint(model.set_t, rule=eq_63, doc="Eq. 63.")
    return


def eq_64_1(model, timestep):
    return model.var_lambda_5[timestep] == sum(
        model.par_c_gen_e_t[e] * model.var_sigma[e, "M1", timestep]
        for e in model.set_e_stroke
    )


def add_64_1(model=None):
    model.eq_64_1 = py.Constraint(model.set_t, rule=eq_64_1, doc="Eq. 64 (1).")
    return


def eq_64_2(model, timestep):
    return model.var_lambda_6[timestep] == sum(
        model.par_c_gen_e_t[e] * model.var_sigma[e, "M2", timestep]
        for e in model.set_e_stroke
    )


def add_64_2(model=None):
    model.eq_64_2 = py.Constraint(model.set_t, rule=eq_64_2, doc="Eq. 64 (2).")
    return


def eq_64_3(model, timestep):
    return model.var_lambda_6[timestep] == model.var_lambda_5[timestep]


def add_64_3(model=None):
    model.eq_64_3 = py.Constraint(model.set_t, rule=eq_64_3, doc="Eq. 64 (3).")
    return


def eq_65(model, t, m):
    return sum(model.var_sigma[e_stroke, m, t] for e_stroke in model.set_e_stroke) == 1


def add_65(model=None):
    model.eq_65 = py.Constraint(
        model.set_t, model.set_market, rule=eq_65, doc="Eq. 65."
    )
    return


"""
#
#
#
#
#
"""


def eq_66_1(model, e, t):
    # market: M1
    return (
        model.var_lambda_snake_5[e, t]
        == model.par_c_gen_e_t[e] * model.var_sigma_snake[e, "M1", t]
    )


def eq_66_2(model, e, t):
    # market: M2
    return (
        model.var_lambda_snake_6[e, t]
        == model.par_c_gen_e_t[e] * model.var_sigma_snake[e, "M2", t]
    )


def eq_67(model, e, m, t):
    return model.var_q[e, m, t] <= model.par_beta_snake * model.var_sigma_snake[e, m, t]


def eq_68(model, e, m, t):
    return model.var_q[e, m, t] >= model.par_epsilon * model.var_sigma_snake[e, m, t]


def eq_69(model, e, m, t):
    return model.var_sigma[e, m, t] <= model.var_sigma_snake[e, m, t]


def eq_70_1(model, e, t):
    # market: M1
    return model.var_lambda_5[t] >= model.var_lambda_snake_5[e, t]


def eq_70_2(model, e, t):
    # market: M2
    return model.var_lambda_6[t] >= model.var_lambda_snake_6[e, t]


def add_66_1_to_70_2(model=None):
    model.eq_66_1 = py.Constraint(model.set_e_stroke, model.set_t, rule=eq_66_1)
    model.eq_66_2 = py.Constraint(model.set_e_stroke, model.set_t, rule=eq_66_2)
    model.eq_67 = py.Constraint(
        model.set_e_stroke, model.set_market, model.set_t, rule=eq_67
    )
    model.eq_68 = py.Constraint(
        model.set_e_stroke, model.set_market, model.set_t, rule=eq_68
    )
    model.eq_69 = py.Constraint(
        model.set_e_stroke, model.set_market, model.set_t, rule=eq_69
    )
    model.eq_70_1 = py.Constraint(model.set_e_stroke, model.set_t, rule=eq_70_1)
    model.eq_70_2 = py.Constraint(model.set_e_stroke, model.set_t, rule=eq_70_2)
    return


def eq_71(model, e, m, t):
    return model.var_z[e, m, t] <= model.par_beta_snake * model.var_sigma[e, m, t]


def eq_72(model, e, m, t):
    _me = model.set_mexporter.first()
    return model.var_z[e, m, t] <= model.var_q[_me, m, t]


def eq_73(model, e, m, t):
    _me = model.set_mexporter.first()
    return (
        model.var_z[e, m, t]
        >= model.var_q[_me, m, t]
        - (1 - model.var_sigma[e, m, t]) * model.par_beta_snake
    )


def eq_74(model, e, m, t):
    return model.var_z[e, m, t] >= 0


def add_71_to_74(model=None):
    model.eq_71 = py.Constraint(
        model.set_e_stroke, model.set_market, model.set_t, rule=eq_71, doc="Eq. 71."
    )
    model.eq_72 = py.Constraint(
        model.set_e_stroke, model.set_market, model.set_t, rule=eq_72, doc="Eq. 72."
    )
    model.eq_73 = py.Constraint(
        model.set_e_stroke, model.set_market, model.set_t, rule=eq_73, doc="Eq. 73."
    )
    model.eq_74 = py.Constraint(
        model.set_e_stroke, model.set_market, model.set_t, rule=eq_74, doc="Eq. 74."
    )
    return


def eq_18_2(model, e, t, s):
    return model.var_delta_seg[e, t, s] == sum(
        model.var_delta_seg_points[e, t, s, p] for p in model.set_segments_points
    )


def eq_18_3(model, e, t, s, p):
    return model.var_delta_seg_points[e, t, s, p] <= 1


def add_18(model=None):

    model.set_segments = py.Set(
        initialize=[0, 1, 2],
        doc='three different segments: constant, linear, constant.'
    ) # checked

    model.set_segments_points = py.Set(
        initialize=[0, 1],
        doc='each segment has a starting and an ending point.'
    ) # checked

    model.var_delta_seg = py.Var(
        model.set_e_stroke,
        model.set_t,
        model.set_segments,
        within=py.Binary,
        doc='based on market clearing price, which segment is active (either segment 0, 1, or 2).'
    ) # checked

    model.var_delta_seg_points = py.Var(
        model.set_e_stroke,
        model.set_t,
        model.set_segments,
        model.set_segments_points,
        within=py.NonNegativeReals,
        doc='for linear interpolation between starting and ending point of the active segment.'
    ) # checked

    model.eq_18_seg_points_smaller_equal_one = py.Constraint(
        model.set_e_stroke,
        model.set_t_stroke,
        model.set_segments,
        model.set_segments_points,
        rule=eq_18_3,
        doc='Ensure that each of the segment points is smaller or equal to 1.'
    ) # checked

    model.eq_18_seg_points_of_active_segment = py.Constraint(
        model.set_e_stroke,
        model.set_t_stroke,
        model.set_segments,
        rule=eq_18_2,
        doc="ensure that only segment points of active segment can be greater than zero.",
    ) # checked
    return


############################################################################################################
############################################################################################################
############################################################################################################


def eq_18_x_axis(model, e, t):
    if e == "Recycling":
        return model.var_q_bar_add[e, t] == 0
    elif e == "Slack exporter":
        return model.var_q_bar_add[e, t] == 0
    else:
        _lambda_snake_0 = model.par_c_gen_e_t[e]
        _lambda_snake_1 = model.par_c_gen_e_t["Recycling"]
        _lambda_snake_2 = model.par_c_gen_e_t["Slack exporter"]

        return (
                model.var_lambda_5[t - 1]
                == _lambda_snake_0 * model.var_delta_seg_points[e, t, 0, 0]
                + (_lambda_snake_1 - _lambda_snake_0) * model.var_delta_seg_points[e, t, 1, 0]
                + model.var_delta_seg[e, t, 1] * _lambda_snake_0
                + _lambda_snake_2 * model.var_delta_seg_points[e, t, 2, 0]
        )


def eq_18_1(model, e, t):
    if e in ["Recycling", "Slack exporter"]:
        return py.Constraint.Skip
    else:
        return sum(model.var_delta_seg[e, t, s] for s in model.set_segments) == 1


def eq_18_y_axis(model, e, t):
    if e in ["Recycling", "Slack exporter"]:
        return model.var_q_bar_add[e, t] == 0
    else:
        _max_increase_per_year = 0.1 * model.par_q_bar_e_stroke[e]
        return model.var_q_bar_add[e, t] <=  _max_increase_per_year * (model.var_delta_seg_points[e, t, 1, 0] + model.var_delta_seg[e, t, 2])


def add_18_y_axis(model=None):

    model.eq_18_x_axis = py.Constraint(
        model.set_e_stroke, model.set_t_stroke, rule=eq_18_x_axis, doc="Eq. 18."
    )
    
    model.eq_18_1 = py.Constraint(
        model.set_e_stroke, model.set_t_stroke, rule=eq_18_1, doc="Eq. 18 (1)"
    )
    
    model.eq_18_y_axis = py.Constraint(
        model.set_e_stroke,
        model.set_t_stroke,
        rule=eq_18_y_axis,
        doc="Eq. 18 (y-axis).",
    )

    return



############################################################################################################
############################################################################################################
############################################################################################################


def eq_21(model, time):
    _mexporter = model.set_mexporter.first()
    return model.var_q_bar_1[time] <= model.par_q_bar_emajor


def add_21(model=None):
    model.add_21 = py.Constraint(model.set_t, rule=eq_21)
    return


def feasible_constraint(model=None):
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

    return _first_term - _second_term <= 10e3



def add_feasible_constraint(model):
    model.add_feasible = py.Constraint(rule=feasible_constraint)
    return


def equation_4(model=None, m=None, t=None):
    _mexp = model.set_mexporter.first()
    return model.var_q_del[m, t] + model.var_q_arb_major[m, t] - model.var_q[_mexp, m, t] == 0

def equation_5(model=None, t=None):
    return sum(model.var_q[e, 'M1', t] for e in model.set_e_stroke) + model.var_q_del['M1', t] + model.var_q_arb_major['M2', t] + model.var_stock_in_out[t] - model.par_demand['M1', t] == 0

def equation_6(model=None, t=None):
    return sum(model.var_q[e, 'M2', t] for e in model.set_e_stroke) + model.var_q_del['M2', t] + model.var_q_arb_major['M1', t] - model.par_demand['M2', t] == 0

def equation_9(model=None):
    t = model.set_t.first()
    return model.var_stock_stored[t] == 0

def equation_10(model=None, t=None):
    return model.var_stock_stored[t] - model.var_stock_stored[t - 1] + model.var_stock_in_out[t - 1] == 0


def add_equality_constraints(model=None):
    model.equation4 = py.Constraint(model.set_market, model.set_t, rule=equation_4)
    model.equation5 = py.Constraint(model.set_t, rule=equation_5)
    model.equation6 = py.Constraint(model.set_t, rule=equation_6)
    model.equation9 = py.Constraint(rule=equation_9)
    model.equation10 = py.Constraint(model.set_t_stroke, rule=equation_10)
    return






