import unittest
import csv
from pathlib import Path
from evaluate import evaluate


def row(identifier, truth, decision, latency='100'):
    return {'id': identifier, 'truth': truth, 'decision': decision, 'latency_ms': latency}


class EvaluationTests(unittest.TestCase):
    def test_hand_calculated_fixture(self):
        with Path(__file__).with_name('synthetic.csv').open(newline='') as f:
            result = evaluate(list(csv.DictReader(f)))
        self.assertEqual(result['counts'], {'tp': 3, 'tn': 4, 'fp': 1, 'fn': 1, 'review_match': 2, 'review_mismatch': 1})
        self.assertEqual(result['metrics']['coverage'], .75)
        self.assertEqual(result['metrics']['accuracy_among_automated_decisions'], .777778)
        self.assertEqual(result['metrics']['automatically_recovered_matches_over_all_true_matches'], .5)
        self.assertEqual(result['latency_ms_all_observations'], {'p50':117.5,'p95':169.0})

    def test_all_review_does_not_report_perfect_accuracy(self):
        result = evaluate([row('a','match','review'), row('b','mismatch','review')])
        self.assertIsNone(result['metrics']['accuracy_among_automated_decisions'])
        self.assertIsNone(result['metrics']['match_precision'])
        self.assertEqual(result['metrics']['coverage'], 0)
        self.assertEqual(result['metrics']['review_rate'], 1)

    def test_single_negative_has_undefined_positive_recall(self):
        result = evaluate([row('a','mismatch','mismatch','12')])
        self.assertIsNone(result['metrics']['automatically_recovered_matches_over_all_true_matches'])
        self.assertEqual(result['metrics']['accuracy_among_automated_decisions'], 1)
        self.assertEqual(result['latency_ms_all_observations'], {'p50':12.0,'p95':12.0})

    def test_rejects_invalid_records_instead_of_silently_dropping_them(self):
        for rows in [[], [row('a','match','unknown')], [row('a','unknown','match')],
                     [row('a','match','match'), row('a','match','match')],
                     [row('','match','match')], [row('a','match','match','NaN')],
                     [row('a','match','match','-1')], [row('a','match','match','inf')]]:
            with self.subTest(rows=rows), self.assertRaises(ValueError):
                evaluate(rows)


if __name__ == '__main__':
    unittest.main()
