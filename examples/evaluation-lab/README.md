# Evaluation lab

**Runnable reference demo · Python 3.10+ · Standard library only**

A small evaluator for binary matching tasks with an explicit **human-review** outcome. It illustrates why automated-decision quality and coverage should be examined together.

The included inputs, decisions and latencies are **synthetic examples**. No AI model is called. The results demonstrate the evaluator's behavior; they do not measure the performance of a model or any employer system.

## Run

From the repository root:

```bash
python3 examples/evaluation-lab/evaluate.py
python3 -m unittest discover -s examples/evaluation-lab -p 'test_*.py' -v
```

To evaluate another compatible dataset:

```bash
python3 examples/evaluation-lab/evaluate.py path/to/predictions.csv --output report.json
```

## Input contract

| Field | Contract |
| --- | --- |
| `id` | Unique, nonempty observation identifier. |
| `truth` | `match` or `mismatch`; supplied by a trustworthy labeling process. |
| `decision` | `match`, `mismatch` or `review`. |
| `latency_ms` | Finite, nonnegative latency. Included for every observation. |

Invalid data fails with an error. The evaluator does not silently remove records or treat missing decisions as correct.

## What the bundled fixture shows

| Observation group | Count |
| --- | ---: |
| Correct automated matches | 3 |
| Correct automated mismatches | 4 |
| Incorrect automated matches | 1 |
| Incorrect automated mismatches | 1 |
| Sent to human review | 3 |
| Total | 12 |

Coverage is **9/12 = 75%**. Accuracy among automated decisions is **7/9 ≈ 77.78%**. Reporting only the second number hides the three cases sent to review.

## Metric definitions

- **Coverage:** automated decisions / all observations.
- **Review rate:** review decisions / all observations.
- **Accuracy among automated decisions:** correct automated decisions / all automated decisions.
- **Match precision:** correct match decisions / all automated match decisions.
- **Automatically recovered matches:** correct automated match decisions / all true matches, including those sent to review.
- **False acceptances:** incorrect match decisions / all true mismatches, including those sent to review.
- **Correct automated decisions over all observations:** records both correctness and automation coverage; it is not the conditional accuracy metric.

An undefined ratio is represented as `null`. Latency percentiles use linear interpolation at rank `(n − 1) × p`, across all observations. The synthetic p50 is 117.5 ms and p95 is 169 ms; neither represents measured inference speed.

## Engineering decisions

The human-review outcome stays explicit so an abstaining system cannot appear successful merely by hiding difficult cases. Denominators are named in the output to reduce confusion when comparing configurations. Standard-library code makes the example easy to reproduce.

For a real comparison, freeze the test set, record model/configuration versions, inspect leakage, stratify by relevant conditions and consider uncertainty intervals. The twelve invented examples here cannot support a model comparison or a business-impact claim.

[Back to profile](../../README.md)
