from scipy.integrate import solve_ivp
def propagate(dynamics, initial_state, t_span, t_eval):
    return solve_ivp(
        dynamics,
        t_span,
        initial_state,
        t_eval=t_eval,
        method='DOP853',
        rtol=1e-9,
        atol=1e-10,
        max_step=100
    )
