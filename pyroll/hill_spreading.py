import importlib.util

import numpy as np

from pyroll.core import BaseRollPass, RollPass, ThreeRollPass, root_hooks, Unit
from pyroll.core.hooks import Hook

VERSION = "2.0.1"
PILLAR_MODEL_INSTALLED = bool(importlib.util.find_spec("pyroll.pillar_model"))

BaseRollPass.hill_exponent = Hook[float]()
"""Exponent w for for Hill's spread equation."""

root_hooks.add(Unit.OutProfile.width)


@BaseRollPass.hill_exponent
def hill_exponent(self: RollPass):
    height_change = self.in_profile.equivalent_height - self.out_profile.equivalent_height
    return 0.5 * np.exp(- self.in_profile.equivalent_width / (2 * np.sqrt(self.roll.working_radius * height_change)))


@RollPass.OutProfile.width
def width(self: RollPass.OutProfile):
    rp = self.roll_pass

    if not self.has_set_or_cached("width"):
        return None

    return rp.draught ** -rp.hill_exponent * rp.in_profile.width


@ThreeRollPass.OutProfile.width
def width(self: RollPass.OutProfile):
    rp = self.roll_pass

    if not self.has_set_or_cached("width"):
        return None

    return rp.draught ** -rp.hill_exponent * rp.in_profile.width


try:
    @RollPass.DiskElement.pillar_spreads
    def pillar_spreads(self: RollPass.DiskElement):
        rp = self.roll_pass
        return self.pillar_draughts ** -rp.hill_exponent
except AttributeError:
    pass  # pillar model not loaded
