import numpy as np

def taylor_series(f, a, n_terms, x):
    series = 0
    for n in range(n_terms):
        term = (f(a) * (x - a)**n) / np.math.factorial(n)
        series += term
    return series

def integrate_taylor_series(f, a, n_terms, x_start, x_end):
    dx = 0.01
    integral = 0
    for x in np.arange(x_start, x_end, dx):
        series_approx = taylor_series(f, a, n_terms, x)
        integral += series_approx * dx
    return integral

f = lambda x: np.sin(x)
a = 0
n_terms = 5
x_start = 0
x_end = np.pi

integral_result = integrate_taylor_series(f, a, n_terms, x_start, x_end)

print(integral_result)
