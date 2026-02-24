#!/usr/bin/env python3
"""
Ordinary Least Squares via Matrix Algebra

Replicates the 'Least Squares Matrix Formula' spreadsheet:
- Builds X'X and X'Y matrices step by step
- Solves beta = (X'X)^-1 X'Y
- Computes R^2, standard errors, t-statistics
- Cross-validates against numpy's lstsq

Usage:
    python least_squares_matrix.py
    python least_squares_matrix.py --x 0.5 4 6 8 10 --y 6 7 7 8 7
"""
import argparse
import math


def ols_matrix(x, y):
    """Solve y = b0 + b1*x via matrix algebra (no numpy)."""
    n = len(x)

    # Build X'X (2x2) and X'Y (2x1)
    sum_x = sum(x)
    sum_x2 = sum(xi ** 2 for xi in x)
    sum_y = sum(y)
    sum_xy = sum(xi * yi for xi, yi in zip(x, y))

    xtx = [[n, sum_x], [sum_x, sum_x2]]
    xty = [sum_y, sum_xy]

    # Invert 2x2: [[a,b],[c,d]]^-1 = (1/det) * [[d,-b],[-c,a]]
    det = xtx[0][0] * xtx[1][1] - xtx[0][1] * xtx[1][0]
    xtx_inv = [
        [xtx[1][1] / det, -xtx[0][1] / det],
        [-xtx[1][0] / det, xtx[0][0] / det],
    ]

    # Beta = (X'X)^-1 * X'Y
    b0 = xtx_inv[0][0] * xty[0] + xtx_inv[0][1] * xty[1]
    b1 = xtx_inv[1][0] * xty[0] + xtx_inv[1][1] * xty[1]

    # Predictions and residuals
    y_hat = [b0 + b1 * xi for xi in x]
    residuals = [yi - yhi for yi, yhi in zip(y, y_hat)]
    y_mean = sum_y / n

    # Sum of squares
    ss_res = sum(r ** 2 for r in residuals)
    ss_tot = sum((yi - y_mean) ** 2 for yi in y)
    ss_reg = ss_tot - ss_res

    r_squared = 1 - ss_res / ss_tot if ss_tot > 0 else 0

    # Standard errors
    p = 2  # number of parameters
    mse = ss_res / (n - p)
    se_b0 = math.sqrt(mse * xtx_inv[0][0])
    se_b1 = math.sqrt(mse * xtx_inv[1][1])

    # t-statistics
    t_b0 = b0 / se_b0 if se_b0 > 0 else float('inf')
    t_b1 = b1 / se_b1 if se_b1 > 0 else float('inf')

    return {
        'b0': b0, 'b1': b1,
        'se_b0': se_b0, 'se_b1': se_b1,
        't_b0': t_b0, 't_b1': t_b1,
        'r_squared': r_squared,
        'ss_reg': ss_reg, 'ss_res': ss_res, 'ss_tot': ss_tot,
        'mse': mse,
        'y_hat': y_hat, 'residuals': residuals,
        'xtx': xtx, 'xty': xty, 'xtx_inv': xtx_inv, 'det': det,
    }


def print_matrix(name, m, fmt='.4f'):
    """Print a 2x2 or 2x1 matrix."""
    print(f"  {name}:")
    if isinstance(m[0], list):
        for row in m:
            print(f"    [{', '.join(f'{v:{fmt}}' for v in row)}]")
    else:
        print(f"    [{', '.join(f'{v:{fmt}}' for v in m)}]")


def main():
    parser = argparse.ArgumentParser(description='OLS Regression via Matrix Algebra')
    parser.add_argument('--x', nargs='+', type=float, default=[0.5, 4, 6, 8, 10])
    parser.add_argument('--y', nargs='+', type=float, default=[6, 7, 7, 8, 7])
    args = parser.parse_args()

    x, y = args.x, args.y
    assert len(x) == len(y), "x and y must have the same length"

    result = ols_matrix(x, y)

    print("=" * 60)
    print("OLS REGRESSION VIA MATRIX ALGEBRA")
    print("=" * 60)
    print()

    # Input data
    print("INPUT DATA")
    print(f"  {'Obs':<5} {'x':<10} {'y':<10} {'x*y':<12} {'x^2':<10}")
    print("  " + "-" * 47)
    for i, (xi, yi) in enumerate(zip(x, y), 1):
        print(f"  {i:<5} {xi:<10.2f} {yi:<10.2f} {xi*yi:<12.2f} {xi**2:<10.2f}")
    print()

    # Matrix setup
    print("MATRIX CONSTRUCTION")
    print_matrix("X'X", result['xtx'])
    print_matrix("X'Y", result['xty'])
    print(f"\n  det(X'X) = {result['det']:.4f}")
    print_matrix("(X'X)^-1", result['xtx_inv'])
    print()

    # Solution
    print("SOLUTION: beta = (X'X)^-1 * X'Y")
    print(f"  b0 (intercept) = {result['b0']:.4f}")
    print(f"  b1 (slope)     = {result['b1']:.4f}")
    print(f"  Equation: y = {result['b0']:.4f} + {result['b1']:.4f} * x")
    print()

    # Predictions
    print("PREDICTIONS & RESIDUALS")
    print(f"  {'Obs':<5} {'x':<8} {'y':<8} {'y_hat':<10} {'residual':<10}")
    print("  " + "-" * 41)
    for i, (xi, yi, yh, r) in enumerate(zip(x, y, result['y_hat'], result['residuals']), 1):
        print(f"  {i:<5} {xi:<8.2f} {yi:<8.2f} {yh:<10.4f} {r:<10.4f}")
    print()

    # Goodness of fit
    print("GOODNESS OF FIT")
    print(f"  SS_regression = {result['ss_reg']:.4f}")
    print(f"  SS_residual   = {result['ss_res']:.4f}")
    print(f"  SS_total      = {result['ss_tot']:.4f}")
    print(f"  R^2           = {result['r_squared']:.4f}")
    print(f"  MSE           = {result['mse']:.4f}")
    print()

    # Standard errors
    print("STANDARD ERRORS & T-STATISTICS")
    print(f"  SE(b0) = {result['se_b0']:.4f}    t(b0) = {result['t_b0']:.4f}")
    print(f"  SE(b1) = {result['se_b1']:.4f}    t(b1) = {result['t_b1']:.4f}")

    # Cross-validate with numpy if available
    try:
        import numpy as np
        A = np.column_stack([np.ones(len(x)), x])
        betas, _, _, _ = np.linalg.lstsq(A, y, rcond=None)
        print(f"\n  numpy lstsq check: b0={betas[0]:.4f}, b1={betas[1]:.4f}  {'MATCH' if abs(betas[0] - result['b0']) < 1e-8 else 'MISMATCH'}")
    except ImportError:
        pass


if __name__ == '__main__':
    main()
