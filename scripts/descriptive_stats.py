#!/usr/bin/env python3
"""
Descriptive Statistics for Lighting Fixture Sampling

Replicates the 'Descriptive Stats Step 1' spreadsheet:
- Compute mean, variance, std dev, CV from a sample of fixture wattages
- Scale up to building-level baseline energy estimate
- Calculate uncertainty range

Usage:
    python descriptive_stats.py
    python descriptive_stats.py --fixtures 1000 --hours 4000
    python descriptive_stats.py --data 120 100 130 122 120 78 100 100 130 80 100 120
"""
import argparse
import math


def descriptive_stats(data):
    """Compute mean, sample variance, sample std dev, and CV."""
    n = len(data)
    mean = sum(data) / n
    deviations = [x - mean for x in data]
    sq_deviations = [d ** 2 for d in deviations]
    variance = sum(sq_deviations) / (n - 1)  # sample variance
    std_dev = math.sqrt(variance)
    cv = std_dev / mean if mean != 0 else float('inf')
    return {
        'n': n,
        'mean': mean,
        'variance': variance,
        'std_dev': std_dev,
        'cv': cv,
        'deviations': deviations,
        'sq_deviations': sq_deviations,
    }


def building_energy(mean_watts, total_fixtures, hours_per_year, cv):
    """Scale sample mean to building-level energy estimate."""
    total_kw = mean_watts * total_fixtures / 1000
    total_kwh = total_kw * hours_per_year
    return {
        'total_kw': total_kw,
        'total_kwh': total_kwh,
        'uncertainty_kwh': total_kwh * cv,
    }


def main():
    parser = argparse.ArgumentParser(description='Descriptive Statistics for Lighting Fixture Sampling')
    parser.add_argument('--data', nargs='+', type=float,
                        default=[120, 100, 130, 122, 120, 78, 100, 100, 130, 80, 100, 120],
                        help='Fixture wattage measurements')
    parser.add_argument('--fixtures', type=int, default=1000,
                        help='Total number of fixtures in building (default: 1000)')
    parser.add_argument('--hours', type=float, default=4000,
                        help='Operating hours per year (default: 4000)')
    args = parser.parse_args()

    data = args.data
    stats = descriptive_stats(data)
    energy = building_energy(stats['mean'], args.fixtures, args.hours, stats['cv'])

    print("=" * 60)
    print("DESCRIPTIVE STATISTICS — FIXTURE WATTAGE SAMPLE")
    print("=" * 60)
    print()
    print(f"{'Fixture':<10} {'Watts':<10} {'Deviation':<12} {'Dev^2':<12}")
    print("-" * 44)
    for i, (w, d, d2) in enumerate(zip(data, stats['deviations'], stats['sq_deviations']), 1):
        print(f"{i:<10} {w:<10.1f} {d:<12.2f} {d2:<12.2f}")

    print("-" * 44)
    print(f"{'Sum':<10} {sum(data):<10.1f} {'':12} {sum(stats['sq_deviations']):<12.2f}")
    print()
    print(f"  Sample size (n):      {stats['n']}")
    print(f"  Mean:                 {stats['mean']:.2f} W")
    print(f"  Sample Variance:      {stats['variance']:.2f} W^2")
    print(f"  Sample Std Dev:       {stats['std_dev']:.2f} W")
    print(f"  CV:                   {stats['cv']:.4f} ({stats['cv']*100:.2f}%)")

    print()
    print("=" * 60)
    print("BUILDING-LEVEL ENERGY ESTIMATE")
    print("=" * 60)
    print()
    print(f"  Total fixtures:       {args.fixtures:,}")
    print(f"  Hours/year:           {args.hours:,.0f}")
    print(f"  Mean wattage:         {stats['mean']:.2f} W")
    print()
    print(f"  Total connected load: {energy['total_kw']:.1f} kW")
    print(f"  Annual energy:        {energy['total_kwh']:,.0f} kWh")
    print(f"  Uncertainty (1 CV):   +/- {energy['uncertainty_kwh']:,.0f} kWh ({stats['cv']*100:.1f}%)")
    print(f"  Range:                {energy['total_kwh'] - energy['uncertainty_kwh']:,.0f} – {energy['total_kwh'] + energy['uncertainty_kwh']:,.0f} kWh")


if __name__ == '__main__':
    main()
