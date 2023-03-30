import unittest

import numpy as np
import numpy_financial as npf

from bonds import utils


class UtilTestCase(unittest.TestCase):
    def test_bond_cash_flows(self):
        cash_flow = utils.get_bond_cash_flow(mkt_price=900, face_value=1000, coupon_rate_pct=5, maturity=5, n_coupons=1)
        expected_cash_flow = np.array([-900, 50, 50, 50, 50, 1050])
        self.assertTrue(np.array_equal(expected_cash_flow, cash_flow))

    def test_ytm(self):
        cash_flow = utils.get_bond_cash_flow(mkt_price=900, face_value=1000, coupon_rate_pct=5, maturity=5, n_coupons=1)
        irr = npf.irr(cash_flow) * 100
        ytm = utils.ytm(mkt_price=900, face_value=1000, coupon_rate_pct=5, maturity=5, n_coupons=1)
        self.assertAlmostEqual(irr, ytm)

    def test_rcy(self):
        coupons_pa = 2
        exp_ytm = utils.ytm(mkt_price=900, face_value=1000, coupon_rate_pct=5, maturity=5, n_coupons=coupons_pa)
        rcy = utils.rcy(mkt_price=900, face_value=1000, coupon_rate_pct=5, maturity=5, n_coupons=coupons_pa,
                        inv_rate=exp_ytm)
        self.assertAlmostEqual(exp_ytm, rcy)  # when return on coupon investment is ytm, rcy becomes ytm

    def test_rcy1(self):
        # source is https://www.financialplannerprogram.com/calculating-realized-compount-yield-on-a-bond/
        exp_rcy = utils.rcy(mkt_price=1000, face_value=1000, coupon_rate_pct=13, maturity=15, n_coupons=1, inv_rate=9)
        self.assertAlmostEqual(11.05, exp_rcy, places=2)

    def test_rcy2(self):
        # source is https://files.eric.ed.gov/fulltext/EJ1056640.pdf
        exp_rcy = utils.rcy(mkt_price=1308.87, face_value=1000, coupon_rate_pct=9, maturity=10, n_coupons=1, inv_rate=3)
        self.assertAlmostEqual(4.495, exp_rcy, places=3)


if __name__ == '__main__':
    unittest.main()
