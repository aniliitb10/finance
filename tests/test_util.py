import unittest

import numpy as np
import numpy_financial as npf

from bonds import utils
from bonds.interval import Interval


class UtilTestCase(unittest.TestCase):
    def test_bond_cash_flows(self):
        cash_flow = utils.get_bond_cash_flow(900, 1000, 5.0, Interval(years=1), Interval(years=5))
        expected_cash_flow = np.array([-900, 50, 50, 50, 50, 1050])
        self.assertTrue(np.array_equal(expected_cash_flow, cash_flow))

    def test_ytm(self):
        cash_flow = utils.get_bond_cash_flow(900, 1000, 5.0, Interval(years=1), Interval(years=5))
        irr = npf.irr(cash_flow) * 100
        ytm = utils.ytm(900, 1000, 5.0, Interval(years=1), Interval(years=5))
        self.assertAlmostEqual(irr, ytm)

    def test_rcy(self):
        exp_ytm = utils.ytm(900, 1000, 5.0, Interval(months=6), Interval(years=5))
        rcy = utils.rcy(900, 1000, 5.0, Interval(months=6), Interval(years=5), reinvestment_rate=exp_ytm)
        self.assertAlmostEqual(exp_ytm, rcy)  # when return on coupon investment is ytm, rcy becomes ytm

    def test_rcy1(self):
        # source is https://www.financialplannerprogram.com/calculating-realized-compount-yield-on-a-bond/
        exp_rcy = utils.rcy(1000, 1000, 13.0, Interval(years=1), Interval(years=15), reinvestment_rate=9)
        self.assertAlmostEqual(11.05, exp_rcy, places=2)

    def test_rcy2(self):
        # source is https://files.eric.ed.gov/fulltext/EJ1056640.pdf
        exp_rcy = utils.rcy(1308.87, 1000, 9.0, Interval(years=1), Interval(years=10), reinvestment_rate=3)
        self.assertAlmostEqual(4.495, exp_rcy, places=3)

    def test_price(self):
        # first calculate the ytm and then use the same ytm to calculate the current price
        ytm = utils.ytm(900, 1000, 5.0, Interval(years=1), Interval(years=5))
        price = utils.price(1000, 5, ytm, Interval(years=1), Interval(years=5))
        self.assertAlmostEqual(900, price)

    def test_price2(self):
        # first calculate the ytm and then use the same ytm to calculate the current price
        ytm = utils.ytm(888, 1000, 5.0, Interval(months=6), Interval(years=20))
        price = utils.price(1000, 5, ytm, Interval(months=6), Interval(years=20))
        self.assertAlmostEqual(888, price)


if __name__ == '__main__':
    unittest.main()
