from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, root_validator


class Interval(BaseModel):
    weeks: Optional[int]
    months: Optional[int]
    years: Optional[int]

    @root_validator(pre=True)
    def at_least_one_tenor(cls, values):
        if [field in values for field in ('weeks', 'months', 'years')].count(True) != 1:
            raise ValueError(f'Exactly one of (weeks, months, years) must be passed as an argument')

        return values

    def _get_int_value(self) -> int:
        return self.weeks or self.months or self.years

    def fraction_of_year(self) -> float:
        """ Returns the fraction of year this Interval represents
        e.g. if interval is 6 months, this function returns 0.5
        """
        if self.weeks:
            return self.weeks / 52

        # instead of self / Interval(years=1) as it might be a float which is not allowed
        return 1 / (Interval(years=1) / self)

    def __str__(self) -> str:
        if self.weeks:
            return f'{self.weeks} weeks'

        if self.months:
            return f'{self.months} months'

        return f'{self.years} years'

    def __truediv__(self, other: Interval) -> int:
        """
        Returns division of tenors of the same format
        Expected use case: when you need to count the number of coupons using the tenor and interval for coupons
        """
        if type(other) != type(self):
            raise ValueError(f'Expected type {type(self)} but got {type(other)}')

        # Another sanity check
        if bool(self.weeks) != bool(other.weeks):
            raise ValueError('Only one of the tenor is defined in weeks, which is unexpected as there is '
                             'no conversion from weeks to months / years')

        if self.weeks and other.weeks:
            return self._raise_if_not_int(self.weeks / other.weeks)

        # Now, it is determined that the format doesn't involve week
        # so even if it involved months and years, these are interconvertible
        this_interval_month = self.months or self.years * 12
        other_interval_month = other.months or other.years * 12
        return self._raise_if_not_int(this_interval_month / other_interval_month)

    @staticmethod
    def _raise_if_not_int(num: float, msg: str = 'Result was expected to be an int but it is a float') -> int:
        """
        Performs sanity check: @num is expected to be an int. An exception is raised if it isn't an int
        Args:
            num: number to check it is an int
            msg: if @num is not an int, then exception is raised with this message

        Returns: returns integer type representing the @num
        """
        if num.is_integer():
            return int(num)

        raise ValueError(msg)
