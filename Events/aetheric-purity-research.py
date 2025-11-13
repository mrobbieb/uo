#!/usr/bin/env python3
"""
Find the combination of three values whose mean is closest to 7.0.

Usage:
  python aetheric-purity-research.py 1.356 7.522 5.498 9.1 2.0
  python aetheric-purity-research.py "[1.356, 7.522, 5.498, 9.1, 2.0]"

Notes:
- Accepts either space-separated numbers or a single JSON-like array.
- Prints the best triple, its exact mean, and the mean rounded UP to the nearest thousandth.
"""

import sys
import json
import math
import itertools

TARGET_MEAN = 7.0
K = 3
TARGET_SUM = TARGET_MEAN * K

def ceil_to_thousandth(x: float) -> float:
    # Round UP to the nearest thousandth (ceiling at 3 decimals)
    return math.ceil(x * 1000.0) / 1000.0

def parse_values(argv):
    if len(argv) == 1:
        s = argv[0].strip()
        if s.startswith('[') and s.endswith(']'):
            try:
                vals = json.loads(s)
                return [float(v) for v in vals]
            except Exception as e:
                sys.exit(f"Could not parse JSON array: {e}")
    # Otherwise treat as space-separated numbers
    try:
        return [float(a) for a in argv]
    except ValueError as e:
        sys.exit(f"All inputs must be numbers (or a JSON array of numbers): {e}")

def warn_out_of_range(values):
    bad = [v for v in values if not (0.001 <= v <= 14.0)]
    if bad:
        print(f"Warning: these values are outside the 1.0–14.0 range: {bad}", file=sys.stderr)

def main():
    if len(sys.argv) < 4:
        sys.exit("Provide at least 3 values. Example: python find_best_mean7.py 1.356 7.522 5.498")

    values = parse_values(sys.argv[1:])
    warn_out_of_range(values)

    if len(values) < K:
        sys.exit(f"Need at least {K} values, got {len(values)}.")

    best_comb = None
    best_key = None  # (abs(mean-7), abs(sum-21), sorted tuple for deterministic tie-break)

    for comb in itertools.combinations(values, K):
        s = sum(comb)
        mean = s / K
        diff = abs(mean - TARGET_MEAN)
        # Deterministic tie-breakers: sum closeness, then lexicographic of sorted values
        key = (diff, abs(s - TARGET_SUM), tuple(sorted(comb)))
        if best_key is None or key < best_key:
            best_key = key
            best_comb = comb

    s = sum(best_comb)
    mean = s / K
    mean_ceiled = ceil_to_thousandth(mean)

    a, b, c = best_comb
    print(f"Best triple: ({a}, {b}, {c})")
    print(f"Exact mean: {mean:.12f}")
    print(f"Mean rounded UP to nearest thousandth: {mean_ceiled:.3f}")

if __name__ == "__main__":
    main()
