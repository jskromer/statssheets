#!/usr/bin/env python3
"""
Sampling Methodology Exercise

Replicates the 'Statistics_Exercise.xlsm' workbook:
1. Generate a synthetic population (normal distribution)
2. Draw a random sample
3. Compute descriptive statistics and compare to population
4. Calculate required sample sizes for various precision targets

Usage:
    python sampling_exercise.py
    python sampling_exercise.py --pop-mean 100 --pop-std 25 --pop-size 1000 --sample-size 30
    python sampling_exercise.py --sample-size-calc --cv 0.25 --precision 0.10 --confidence 90 --population 1000
"""
import argparse
import math
import random


def generate_population(mean, std_dev, n, seed=None):
    """Generate a normally distributed population of fixture wattages."""
    if seed is not None:
        random.seed(seed)
    return [max(0, random.gauss(mean, std_dev)) for _ in range(n)]


def draw_sample(population, sample_size, seed=None):
    """Draw a simple random sample without replacement."""
    if seed is not None:
        random.seed(seed)
    return random.sample(population, min(sample_size, len(population)))


def calc_stats(data):
    """Compute descriptive statistics."""
    n = len(data)
    mean = sum(data) / n
    variance = sum((x - mean) ** 2 for x in data) / (n - 1)
    std_dev = math.sqrt(variance)
    cv = std_dev / mean if mean != 0 else float('inf')
    return {'n': n, 'mean': mean, 'variance': variance, 'std_dev': std_dev,
            'cv': cv, 'min': min(data), 'max': max(data)}


def sample_size_infinite(z, cv, precision):
    """Required sample size (infinite population): n0 = (Z * CV / P)^2."""
    return (z * cv / precision) ** 2


def sample_size_finite(n0, N):
    """Apply finite population correction: n = (n0 * N) / (n0 + N)."""
    return (n0 * N) / (n0 + N)


def z_score(confidence_pct):
    """Approximate Z-score for common confidence levels."""
    z_table = {80: 1.282, 85: 1.440, 90: 1.645, 95: 1.960, 99: 2.576}
    if confidence_pct in z_table:
        return z_table[confidence_pct]
    # Rough approximation for other values
    from statistics import NormalDist
    return NormalDist().inv_cdf(0.5 + confidence_pct / 200)


def histogram(data, bins=10):
    """Simple text histogram."""
    lo, hi = min(data), max(data)
    width = (hi - lo) / bins
    counts = [0] * bins
    for x in data:
        idx = min(int((x - lo) / width), bins - 1)
        counts[idx] += 1
    max_count = max(counts)
    bar_width = 40
    for i in range(bins):
        edge = lo + i * width
        bar = '#' * int(counts[i] / max_count * bar_width) if max_count > 0 else ''
        print(f"  {edge:7.1f} | {bar:<{bar_width}} {counts[i]}")


def main():
    parser = argparse.ArgumentParser(description='Sampling Methodology Exercise')
    parser.add_argument('--pop-mean', type=float, default=100, help='Population mean wattage (default: 100)')
    parser.add_argument('--pop-std', type=float, default=25, help='Population std dev (default: 25)')
    parser.add_argument('--pop-size', type=int, default=1000, help='Population size (default: 1000)')
    parser.add_argument('--sample-size', type=int, default=30, help='Sample size to draw (default: 30)')
    parser.add_argument('--seed', type=int, default=42, help='Random seed (default: 42)')
    parser.add_argument('--sample-size-calc', action='store_true', help='Run sample size calculator only')
    parser.add_argument('--cv', type=float, default=None, help='CV for sample size calc')
    parser.add_argument('--precision', type=float, default=0.10, help='Desired precision (default: 0.10 = 10%%)')
    parser.add_argument('--confidence', type=int, default=90, help='Confidence level %% (default: 90)')
    parser.add_argument('--population', type=int, default=None, help='Population size for finite correction')
    args = parser.parse_args()

    if args.sample_size_calc:
        cv = args.cv if args.cv else 0.25
        run_sample_size_calc(cv, args.precision, args.confidence, args.population)
        return

    # Step 1: Generate population
    print("=" * 60)
    print("STEP 1: GENERATE POPULATION")
    print("=" * 60)
    pop = generate_population(args.pop_mean, args.pop_std, args.pop_size, seed=args.seed)
    pop_stats = calc_stats(pop)
    print(f"  Target:   mean={args.pop_mean}, std_dev={args.pop_std}, N={args.pop_size}")
    print(f"  Observed: mean={pop_stats['mean']:.2f}, std_dev={pop_stats['std_dev']:.2f}")
    print(f"  Range:    {pop_stats['min']:.1f} – {pop_stats['max']:.1f}")
    print(f"  CV:       {pop_stats['cv']:.4f} ({pop_stats['cv']*100:.2f}%)")
    print()
    print("  Distribution:")
    histogram(pop)

    # Step 2: Draw random sample
    print()
    print("=" * 60)
    print(f"STEP 2: DRAW RANDOM SAMPLE (n={args.sample_size})")
    print("=" * 60)
    sample = draw_sample(pop, args.sample_size, seed=args.seed + 1)
    samp_stats = calc_stats(sample)
    print(f"  Sample: {', '.join(f'{x:.1f}' for x in sample[:10])}{'...' if len(sample) > 10 else ''}")
    print()
    print(f"  {'Statistic':<20} {'Population':<15} {'Sample':<15} {'% Diff':<10}")
    print("  " + "-" * 60)
    for label, pk, sk in [
        ('Mean', pop_stats['mean'], samp_stats['mean']),
        ('Std Dev', pop_stats['std_dev'], samp_stats['std_dev']),
        ('CV', pop_stats['cv'], samp_stats['cv']),
    ]:
        pct_diff = (sk - pk) / pk * 100 if pk != 0 else 0
        print(f"  {label:<20} {pk:<15.2f} {sk:<15.2f} {pct_diff:<+10.1f}%")

    # Step 3: Descriptive statistics detail
    print()
    print("=" * 60)
    print("STEP 3: DESCRIPTIVE STATISTICS (STEP BY STEP)")
    print("=" * 60)
    deviations = [x - samp_stats['mean'] for x in sample]
    sq_devs = [d ** 2 for d in deviations]
    print(f"  {'#':<4} {'Watts':<10} {'Deviation':<12} {'Dev^2':<12}")
    print("  " + "-" * 38)
    for i, (w, d, d2) in enumerate(zip(sample, deviations, sq_devs), 1):
        print(f"  {i:<4} {w:<10.1f} {d:<12.2f} {d2:<12.2f}")
    print("  " + "-" * 38)
    print(f"  {'Sum':<4} {sum(sample):<10.1f} {'':12} {sum(sq_devs):<12.2f}")
    print()
    print(f"  Sample Variance = {sum(sq_devs):.2f} / ({samp_stats['n']} - 1) = {samp_stats['variance']:.2f}")
    print(f"  Sample Std Dev  = sqrt({samp_stats['variance']:.2f}) = {samp_stats['std_dev']:.2f}")
    print(f"  CV              = {samp_stats['std_dev']:.2f} / {samp_stats['mean']:.2f} = {samp_stats['cv']:.4f}")

    # Step 4: Sample size calculator
    print()
    print("=" * 60)
    print("STEP 4: SAMPLE SIZE CALCULATOR")
    print("=" * 60)
    run_sample_size_calc(samp_stats['cv'], args.precision, args.confidence, args.pop_size)


def run_sample_size_calc(cv, precision, confidence, pop_size):
    """Run sample size calculations for multiple scenarios."""
    z = z_score(confidence)
    n0 = sample_size_infinite(z, cv, precision)
    print(f"\n  Formula: n0 = (Z * CV / P)^2")
    print(f"  Z({confidence}%) = {z:.3f},  CV = {cv:.4f},  P = {precision:.2f}")
    print(f"  n0 = ({z:.3f} * {cv:.4f} / {precision:.2f})^2 = {n0:.1f}")

    if pop_size:
        n_final = sample_size_finite(n0, pop_size)
        print(f"\n  Finite population correction (N={pop_size}):")
        print(f"  n = (n0 * N) / (n0 + N) = ({n0:.1f} * {pop_size}) / ({n0:.1f} + {pop_size}) = {n_final:.1f}")
        print(f"  Required sample size: {math.ceil(n_final)}")

    # Scenario comparison
    print("\n  SCENARIO COMPARISON")
    print(f"  {'Confidence':<12} {'Precision':<12} {'n0':<10} {'n (N={})'.format(pop_size or 'inf'):<10}")
    print("  " + "-" * 44)
    for conf in [80, 90, 95]:
        for prec in [0.05, 0.10, 0.20]:
            z_val = z_score(conf)
            n0_val = sample_size_infinite(z_val, cv, prec)
            n_val = sample_size_finite(n0_val, pop_size) if pop_size else n0_val
            print(f"  {conf}%{'':<8} +/-{prec*100:.0f}%{'':<7} {math.ceil(n0_val):<10} {math.ceil(n_val):<10}")


if __name__ == '__main__':
    main()
