import numpy_financial as npf
import numpy as np
from typing import List


def get_bond_cash_flow(mkt_price: float, face_value: float, coupon_rate_pct: float, maturity: int, n_coupons: int) \
        -> List[float]:
    """
    Args:
        coupon_rate_pct: coupon rate of the bond
        mkt_price: current market price for bond
        face_value: face value of the bond
        maturity: maturity in years/month
        n_coupons: number of coupons every term e.g.:
                1) if coupon is received every month and maturity is in month, then 1
                2) if coupon is received every 6 months and maturity is in years: then 2
                3) if coupon is received every year and maturity is in years: then 1

    Returns:
        List of all cash flows
    """
    each_coupon_payment = (face_value * coupon_rate_pct / 100) / n_coupons
    all_coupon_payments = [each_coupon_payment] * (maturity * n_coupons)
    return [-mkt_price] + all_coupon_payments[:-1] + [all_coupon_payments[-1] + face_value]


def ytm(mkt_price: float, face_value: float, coupon_rate_pct: float, maturity: int, n_coupons: int) -> float:
    """
    Args:
        coupon_rate_pct: coupon rate of the bond
        mkt_price: current market price for bond
        face_value: face value of the bond
        maturity: maturity in years/month
        n_coupons: number of coupons every term e.g.:
                1) if coupon is received every month and maturity is in month, then 1
                2) if coupon is received every 6 months and maturity is in years: then 2
                3) if coupon is received every year and maturity is in years: then 1

    Returns:
        object: Yield to maturity for the bond
    """

    return npf.irr(get_bond_cash_flow(mkt_price, face_value, coupon_rate_pct, maturity, n_coupons)) * 100 * n_coupons


def rcy(mkt_price: float, face_value: float, coupon_rate_pct: float, maturity: int, n_coupons: int, inv_rate: float):
    """
    To calculate RCY (Realized Compounded Yield):
    It calculates the net return on:
    1) Holding a bond and getting each coupon payment on time
    2) And investing each coupon and realizing a return of @inv_rate on investing these coupons

    Args:
        coupon_rate_pct: coupon rate of the bond
        mkt_price: current market price for bond
        face_value: face value of the bond
        maturity: maturity in years/month
        n_coupons: number of coupons every term e.g.:
                1) if coupon is received every month and maturity is in month, then 1
                2) if coupon is received every 6 months and maturity is in years: then 2
                3) if coupon is received every year and maturity is in years: then 1
        inv_rate: the rate of return on each coupon

    Returns:
        object: Realized Compounded Yield for the bond
    """
    coupon = (face_value * coupon_rate_pct / 100) / n_coupons
    growth_rate = 1 + inv_rate / 100 / n_coupons

    coupon_count = maturity * n_coupons
    coupon_fv = coupon * np.power(growth_rate, np.arange(coupon_count))
    total_sum_capitalized = np.sum(coupon_fv) + face_value

    return (np.power(total_sum_capitalized / mkt_price, 1 / coupon_count) - 1) * 100 * n_coupons
