"""
Performance test of numericalodes: Comparison of C code, Python code and -- if available -- scipy code.
Call the script via command line and pass a path as first argument to write the performance output to a file.
"""

import os
from timeit import default_timer as ts
from typing import Callable, Sequence
import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp
import uncertainties as u
from numericalodes import RK4c, RK4py  # type: ignore

VERBOSE = True
REPETITIONS = 20
EQUAL_STEPS = False


def performance_test(
    solver: Callable, ivps: Sequence[tuple], rep: int = REPETITIONS, scipy: bool = False
) -> list[float]:
    mean_times = []

    if scipy:
        for i, tup in enumerate(ivps):
            duration = []
            for n in range(rep):
                funcs, t0, tmax, y0, h = tup
                system = lambda t, y: [func(t, y) for func in funcs]
                start = ts()
                # for equal step sizes but decreased performance in scipy:
                if EQUAL_STEPS:
                    solver(system, [t0, tmax], y0, method="RK45", first_step=h, max_step=h)
                else:
                    solver(system, [t0, tmax], y0, method="RK45")
                end = ts()
                duration.append(end - start)
                if VERBOSE:
                    print(f"{solver.__name__}: IVP{1} @ rep {n:02}")
            mean_times.append(u.ufloat(np.mean(duration), np.std(duration)))

    else:
        for i, tup in enumerate(ivps):
            duration = []
            for n in range(rep):
                start = ts()
                solver(*tup)
                end = ts()
                duration.append(end - start)
                if VERBOSE:
                    print(f"{solver.__name__}: IVP{i} @ rep {n:02}")
            mean_times.append(u.ufloat(np.mean(duration), np.std(duration)))

    return mean_times


def main() -> None:

    STEP_SIZE = 1e-4

    IVPS = (
        ([lambda t, y: y[0]], 0, 3, [1], STEP_SIZE),
        ([lambda t, y: -15 * y[0]], 0, 1, [1], STEP_SIZE),
        ([lambda t, y: y[1], lambda t, y: -np.sin(y[0])], 0, 2 * np.pi, [0, np.pi / 8], STEP_SIZE),
        ([lambda t, y: y[1], lambda t, y: -np.sin(y[0])], 0, 2 * np.pi, [np.pi * 0.9, 0], STEP_SIZE),
        ([lambda t, y: y[0] / t + y[1] * 2 * t, lambda t, y: y[1] / t], 1, 5, [1, 1], STEP_SIZE),
    )

    df = pd.DataFrame()

    df["C"] = performance_test(RK4c, IVPS)
    df["Python"] = performance_test(RK4py, IVPS)
    df["Scipy"] = performance_test(solve_ivp, IVPS, scipy=True)

    total_means = {
        key: u.ufloat(np.mean([x.n for x in value]), np.std([x.n for x in value])) for key, value in df.items()
    }
    df_total = pd.DataFrame(total_means, index=["total mean"])
    df = pd.concat([df, df_total])
    print(df)

    directory = "output"
    if not os.path.isdir(directory):
        os.makedirs(directory)

    df.to_csv(f"{directory}/performance.csv")


if __name__ == "__main__":
    main()
