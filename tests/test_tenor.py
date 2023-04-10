import unittest

from bonds.interval import Interval


class TenorTestCase(unittest.TestCase):
    def test_tenor(self):
        t_weeks = Interval(weeks=26)
        self.assertEqual(26, t_weeks.weeks)
        self.assertFalse(any([t_weeks.months, t_weeks.years]))

        t_months = Interval(months=6)
        self.assertEqual(6, t_months.months)
        self.assertFalse(any([t_months.weeks, t_months.years]))

        t_years = Interval(years=10)
        self.assertEqual(10, t_years.years)
        self.assertFalse(any([t_years.weeks, t_years.months]))

    def test_valid_tenor(self):
        with self.assertRaises(ValueError) as context:
            Interval()  # expected to throw exception
        self.assertIn('Exactly one of (weeks, months, years) must be passed as an argument', str(context.exception))

        with self.assertRaises(ValueError) as context:
            Interval(weeks=10, years=5)  # expected to throw exception
        self.assertIn('Exactly one of (weeks, months, years) must be passed as an argument', str(context.exception))

        with self.assertRaises(ValueError) as context:
            Interval(months=10, years=1)  # expected to throw exception
        self.assertIn('Exactly one of (weeks, months, years) must be passed as an argument', str(context.exception))

    def test_div(self):
        self.assertEqual(2, Interval(weeks=10) / Interval(weeks=5))
        self.assertEqual(2, Interval(years=10) / Interval(years=5))

        # the result of division can't be a float
        with self.assertRaises(ValueError) as context:
            Interval(years=10) / Interval(years=4)
        self.assertIn('Result was expected to be an int but it is a float', str(context.exception))

        with self.assertRaises(ValueError) as context:
            Interval(years=10) / Interval(weeks=5)
        self.assertIn('Only one of the tenor is defined in weeks', str(context.exception))

        with self.assertRaises(ValueError) as context:
            Interval(weeks=520) / Interval(years=1)
        self.assertIn('Only one of the tenor is defined in weeks', str(context.exception))

        with self.assertRaises(ValueError) as context:
            Interval(years=10) / 2
        self.assertIn('Expected type', str(context.exception))


if __name__ == '__main__':
    unittest.main()
