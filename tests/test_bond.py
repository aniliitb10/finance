import unittest

from bonds.bond import Bond
from bonds.interval import Interval


class BondTestCase(unittest.TestCase):
    def test_basic(self):
        # examples from https://www.treasurydirect.gov/marketable-securities/understanding-pricing/#id-bills-611483
        b1 = Bond(market_price=98.336995, face_value=100, coupon_rate_pct=1.75, coupon_period=Interval(years=1),
                  tenor=Interval(years=20))
        self.assertAlmostEqual(1.850, b1.ytm(), places=3)

        b2 = Bond(market_price=99.429922, face_value=100, coupon_rate_pct=1.375, coupon_period=Interval(years=1),
                  tenor=Interval(years=7))
        self.assertAlmostEqual(1.461, b2.ytm(), places=3)


if __name__ == '__main__':
    unittest.main()
