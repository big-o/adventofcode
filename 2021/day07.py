import numpy as np


def part_a(fh):
    """
    This question is basically asking us to minimise the mean absolute error (MAE)
    of a linear system. Our cost function is:

    $ C = \sum_{n}{|X - p|} $

    The optimal value for p is the *median* of X. If we were looking at mean square
    error, the optimal value would be the mean.
    """
    X = np.array([int(x) for line in fh for x in line.strip().split(",")])
    p = round(np.median(X))
    return np.abs(X - p).sum()


def part_b(fh):
    """
    This time the function is:

    $ C = \sum_{n}{\sum_{k=1}^{|X - p|}{k}i} = \sum_{n}{\frac{|X - p|(|X - p| + 1)}{2}}$

    Because the derivative of $|X - p|$ is another function that depends on X, sign(X),
    there is no exact solution. But by taking the extreme cases (all X < p, all X > p),
    we can get a range of possible solutions: [mean(X) - 0.5, mean(X) + 0.5].

    To obtain the optimal p:

    * Recall that $\frac{d}{dx} |x| = sign(x)$
    * Recall that $\sum_1^n{n} = \frac{n(n+1)}{2}$
    * Find the p (p') that gives the minimum C by setting dC/dx = 0
    * Because $sign(x)$ depends on x, the derivative still contains an x term that can't
      be removed. Basically, the answer depends on whether most of the submarines are to
      the left or right of the optimal point. There are only two possible solutions
      though, so we can brute force from this stage.
    """
    X = np.array([int(x) for line in fh for x in line.strip().split(",")])
    mean = X.mean()

    pmin = pbest = round(mean - 0.5)
    pmax = round(mean + 0.5)
    fn = lambda a, p: round(np.sum(np.abs(a - p) * (np.abs(a - p) + 1) / 2))
    fbest = fn(X, pmin)

    for p in range(pmin, pmax+1):
        f = fn(X, p)
        if f < fbest:
            pbest = p
            fbest = f

    return fbest


def overkill(fh, func="part_a"):
    """
    Use an optimisation library to solve for *any* fuel function, to show that I vaguely
    know what I'm talking about and didn't just look up the answers above.

    Obviously, an analytical solution is better and this method is just there to show
    it's possible.
    """
    from skopt import gp_minimize
    from skopt.space import Integer
    from skopt.utils import use_named_args
    import warnings

    X = np.array([int(x) for line in fh for x in line.strip().split(",")])

    if func == "part_a":
        fn = lambda x, p: round(np.sum(np.abs(x - p)))
    elif func == "part_b":
        fn = lambda x, p: round(np.sum(np.abs(x - p) * (np.abs(x - p) + 1) / 2))
    elif func == "silly":
        fn = lambda x, p: round(np.sum(np.abs(x - p)**2 + np.abs(x - p) + np.sin(x - p)))
    else:
        fn = func

    space = [Integer(1, int(np.max(X)), name="p")]
    @use_named_args(space)
    def objective(**params):
        return fn(X, **params)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        res_gp = gp_minimize(objective, space, n_calls=50, random_state=42)
    return fn(X, res_gp.x[0])
    

if __name__ == "__main__":
    from aocutils import run

    run(part_a)
    run(part_b)
    print("Approximations:")
    run(overkill, "part_a")
    run(overkill, "part_b")
    run(overkill, "silly")
