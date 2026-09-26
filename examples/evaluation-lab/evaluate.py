#!/usr/bin/env python3
"""Evaluate binary decisions with an explicit human-review outcome.

No model is called. The bundled fixture is synthetic, not a model benchmark.
Run from the repository root or from this directory. Python 3.10+.
"""
import argparse
import csv
import json
import math
from pathlib import Path


def ratio(numerator, denominator):
    """Represent undefined ratios explicitly instead of silently returning zero."""
    return round(numerator / denominator, 6) if denominator else None


def percentile(values, fraction):
    """Linear interpolation between sorted observations, rank=(n-1)*fraction."""
    values = sorted(values)
    position = (len(values) - 1) * fraction
    lo = math.floor(position)
    hi = math.ceil(position)
    return round(values[lo] + (values[hi] - values[lo]) * (position - lo), 3)


def evaluate(rows):
    if not rows:
        raise ValueError('The input must contain at least one observation.')
    counts = {k: 0 for k in ('tp','tn','fp','fn','review_match','review_mismatch')}
    identifiers = set()
    latencies = []
    for index, row in enumerate(rows, 1):
        identifier = row.get('id', '').strip()
        truth = row.get('truth', '').strip()
        decision = row.get('decision', '').strip()
        if not identifier or identifier in identifiers:
            raise ValueError(f'Observation {index}: id must be nonempty and unique.')
        identifiers.add(identifier)
        if truth not in ('match','mismatch'):
            raise ValueError(f'{identifier}: truth must be match or mismatch.')
        if decision not in ('match','mismatch','review'):
            raise ValueError(f'{identifier}: decision must be match, mismatch or review.')
        try:
            latency = float(row['latency_ms'])
        except (KeyError, ValueError, TypeError) as exc:
            raise ValueError(f'{identifier}: latency_ms must be numeric.') from exc
        if not math.isfinite(latency) or latency < 0:
            raise ValueError(f'{identifier}: latency_ms must be finite and nonnegative.')
        latencies.append(latency)
        if decision == 'review':
            counts['review_' + truth] += 1
        elif truth == 'match':
            counts['tp' if decision == 'match' else 'fn'] += 1
        else:
            counts['fp' if decision == 'match' else 'tn'] += 1
    total = len(rows)
    reviewed = counts['review_match'] + counts['review_mismatch']
    decided = total - reviewed
    positives = counts['tp'] + counts['fn'] + counts['review_match']
    negatives = counts['tn'] + counts['fp'] + counts['review_mismatch']
    return {
        'schema_version': 1,
        'observations': total,
        'automated_decisions': decided,
        'human_review': reviewed,
        'counts': counts,
        'metrics': {
            'coverage': ratio(decided, total),
            'review_rate': ratio(reviewed, total),
            'accuracy_among_automated_decisions': ratio(counts['tp'] + counts['tn'], decided),
            'match_precision': ratio(counts['tp'], counts['tp'] + counts['fp']),
            'automatically_recovered_matches_over_all_true_matches': ratio(counts['tp'], positives),
            'false_acceptances_over_all_true_mismatches': ratio(counts['fp'], negatives),
            'correct_automated_decisions_over_all_observations': ratio(counts['tp'] + counts['tn'], total),
        },
        'latency_ms_all_observations': {
            'p50': percentile(latencies, .50),
            'p95': percentile(latencies, .95),
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('csv', nargs='?', type=Path, default=Path(__file__).with_name('synthetic.csv'))
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    try:
        with args.csv.open(encoding='utf-8', newline='') as source:
            report = evaluate(list(csv.DictReader(source)))
        report['source'] = args.csv.name
        report['data_origin'] = 'synthetic illustration' if args.csv.resolve() == Path(__file__).with_name('synthetic.csv').resolve() else 'user-supplied; validate provenance separately'
    except (ValueError, OSError) as exc:
        parser.error(str(exc))
    output = json.dumps(report, indent=2, allow_nan=False) + '\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding='utf-8')
    else:
        print(output, end='')


if __name__ == '__main__':
    main()
