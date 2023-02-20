import numpy as np

from pyroll.core import RollPass, ThreeRollPass, root_hooks, Unit
from pyroll.core.hooks import Hook

VERSION = "2.0.0"

RollPass.hill_exponent = Hook[float]()
"""Exponent w for for Hill's spread equation."""

root_hooks.add(Unit.OutProfile.width)


@RollPass.hill_exponent
def hill_exponent(self: RollPass):
    height_change = self.in_profile.equivalent_height - self.out_profile.equivalent_height
    return 0.5 * np.exp(- self.in_profile.equivalent_width / (2 * np.sqrt(self.roll.working_radius * height_change)))


@RollPass.spread
def spread(self: RollPass):
    return (
            self.draught ** self.hill_exponent
    )


@RollPass.OutProfile.width
def width(self: RollPass.OutProfile):
    rp = self.roll_pass

    if not self.has_set_or_cached("width"):
        return None

    return rp.spread * rp.in_profile.width


@ThreeRollPass.OutProfile.width
def width(self: RollPass.OutProfile):
    rp = self.roll_pass

    if not self.has_set_or_cached("width"):
        return None

    return rp.spread * rp.in_profile.width
