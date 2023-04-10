from typing import List

import numpy as np
import numpy_financial as npf
from bonds.interval import Interval


def get_bond_cash_flow(mkt_price: float, face_value: float, coupon_rate_pct: float, coupon_period: Interval,
                       maturity: Interval) -> List[float]:
    """
    Args:
        mkt_price: current market price for bond
        face_value: face value of the bond
        coupon_rate_pct: Annual coupon rate of the bond on each coupon:
        coupon_period: Interval between successive coupon payments
        maturity: Maturity of bond

    Returns:
        List of all cash flows
    """
    each_coupon_payment = (face_value * coupon_rate_pct / 100) * coupon_period.fraction_of_year()
    all_coupon_payments = [each_coupon_payment] * (maturity / coupon_period)
    return [-mkt_price] + all_coupon_payments[:-1] + [all_coupon_payments[-1] + face_value]


def ytm(mkt_price: float, face_value: float, coupon_rate_pct: float, coupon_period: Interval, maturity: Interval)\
        -> float:
    """
    Args:
        mkt_price: current market price for bond
        face_value: face value of the bond
        coupon_rate_pct: Annual coupon rate of the bond on each coupon:
        coupon_period: Interval between successive coupon payments
        maturity: maturity in years/month

    Returns:
        object: Yield to maturity for the bond
    """

    return npf.irr(get_bond_cash_flow(mkt_price, face_value, coupon_rate_pct, coupon_period, maturity)) \
        * 100 / coupon_period.fraction_of_year()


def rcy(mkt_price: float, face_value: float, coupon_rate_pct: float, coupon_period: Interval, maturity: Interval,
        reinvestment_rate: float) -> float:
    """
    To calculate RCY (Realized Compounded Yield):
    It calculates the net return on:
    1) Holding a bond and getting each coupon payment on time
    2) And investing each coupon and realizing a return of @inv_rate on investing these coupons

    Args:
        mkt_price: current market price for bond
        face_value: face value of the bond
        coupon_rate_pct: coupon rate of the bond
        coupon_period: Interval between successive coupon payments
        maturity: maturity in years/month
        reinvestment_rate: the annual rate of return on coupons

    Returns:
        object: Realized Compounded Yield for the bond
    """
    coupon = (face_value * coupon_rate_pct / 100) * coupon_period.fraction_of_year()
    growth_rate = 1 + reinvestment_rate * coupon_period.fraction_of_year() / 100

    coupon_count = maturity / coupon_period
    coupon_fv = coupon * np.power(growth_rate, np.arange(coupon_count))
    total_sum_capitalized = np.sum(coupon_fv) + face_value

    return (np.power(total_sum_capitalized / mkt_price, 1 / coupon_count) - 1)\
        * 100 / coupon_period.fraction_of_year()
