from __future__ import annotations

from pydantic import BaseModel

import bonds.utils as utils
from bonds.interval import Interval


class Bond(BaseModel):
    market_price: float
    face_value: float
    coupon_rate_pct: float
    coupon_period: Interval
    tenor: Interval

    @staticmethod
    def instance(market_price: float = 990, face_value: float = 1000, coupon_rate_pct: float = 3,
                 coupon_period: Interval = Interval(years=1), tenor: Interval = Interval(years=5)) -> Bond:
        """
        A helper method to create an instance of Bond with default values. Providing a default in implicitly defined
         @__init__ would have sufficed too, but IDEs don't support parameter hints in that case
        Args:
            market_price: current price of the bond
            face_value: Face value of the bond
            coupon_rate_pct: Annual coupon rate
            coupon_period: Time interval between successive coupon payments
            tenor: Maturity of the bond

        Returns: An instance of the @Bond class
        """
        return Bond(market_price=market_price, face_value=face_value, coupon_rate_pct=coupon_rate_pct,
                    coupon_period=coupon_period, tenor=tenor)

    def ytm(self) -> float:
        """
        To calculate Yield To Maturity. It doesn't expect the coupon to be invested again.
        Returns: Yield To Maturity
        """
        return utils.ytm(self.market_price, self.face_value, self.coupon_rate_pct, self.coupon_period, self.tenor)

    def rcy(self, reinvestment_rate: float) -> float:
        """
        To calculate the Realized Compounded Yield. It is different from YTM in the sense that coupons are reinvested
        at @reinvestment_rate to get compounded return
        Args:
            reinvestment_rate: the annual return on coupon investments

        Returns: Realized Compounded Yield
        """
        return utils.rcy(self.market_price, self.face_value, self.coupon_rate_pct, self.coupon_period, self.tenor,
                         reinvestment_rate)

    def dv01(self):
        """
        Calculated DV01 of the bond:
        - first calculates the YTM (Yield To Maturity) and then calculates the price back again using YTM-0.01
        Returns:
            DV01 of the bond
        """
        ytm_01 = self.ytm() - 0.01
        return utils.price(self.face_value, self.coupon_rate_pct, ytm_01, self.coupon_period, self.tenor)
