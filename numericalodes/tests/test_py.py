import numericalodes
import numpy as np
import matplotlib.pyplot as plt
from timeit import default_timer as ts


def main() -> None:
    tup = ([lambda t, y: y], 0, 3, [1], 1e-4)

    start = ts()
    t, ypy = numericalodes.RK4py(*tup)  # type: ignore
    py = ts()
    _, yc = numericalodes.RK4c(*tup)
    c = ts()

    print(f"Python: {py-start} s\nC: {c-py} s")

    print(np.array(yc))
    print(np.array(ypy))

    plt.plot(t, ypy[0], label="Python")
    plt.plot(t, yc[0], label="C")
    plt.plot(t, np.exp(t), label="analytic")

    plt.grid()
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
