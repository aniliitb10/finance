import numpy_financial as npf
from typing import List


def get_bond_cash_flows(mkt_price: float, face_value: float, coupon_rate_pct: float, maturity: int, n_coupons: int)\
        -> List[float]:
    """
    Args:
        coupon_rate_pct: coupon rate of the bond
        mkt_price: current market price for bond
        face_value: face value of the bond
        maturity: maturity in years/month
        n_coupons: number of coupons every term (e.g. every month if maturity is in month, otherwise every year)

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
        n_coupons: number of coupons every term (e.g. every month if maturity is in month, otherwise every year)

    Returns:
        object: Yield to maturity for the bond
    """

    return npf.irr(get_bond_cash_flows(mkt_price, face_value, coupon_rate_pct, maturity, n_coupons)) * 100 * n_coupons
