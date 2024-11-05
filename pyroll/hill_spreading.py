import logging
import numpy as np

from pyroll.core import BaseRollPass, RollPass, ThreeRollPass, root_hooks, Unit
from pyroll.core.hooks import Hook

VERSION = "2.0.2"
PILLAR_MODEL_LOADED = False

BaseRollPass.hill_exponent = Hook[float]()
"""Exponent w for for Hill's spread equation."""

BaseRollPass.hill_pre_factor = Hook[float]()
"""Pre factor k for Hill's spread equation.'"""


@BaseRollPass.hill_pre_factor
def default_hill_pre_factor(self: BaseRollPass):
    return 0.5


@BaseRollPass.hill_exponent
def hill_exponent(self: BaseRollPass):
    height_change = self.in_profile.equivalent_height - self.out_profile.equivalent_height

    return self.hill_pre_factor * np.exp(
        - self.in_profile.equivalent_width / (2 * np.sqrt(self.roll.working_radius * height_change)))


@RollPass.OutProfile.width
def width(self: RollPass.OutProfile):
    rp = self.roll_pass

    if not self.has_set_or_cached("width"):
        return None

    return rp.draught ** -rp.hill_exponent * rp.in_profile.width


@ThreeRollPass.OutProfile.width
def width(self: RollPass.OutProfile):
    rp = self.roll_pass

    if not (PILLAR_MODEL_LOADED and rp.disk_elements):
        if not self.has_set_or_cached("width"):
            return None

    return rp.draught ** -rp.hill_exponent * rp.in_profile.width


try:
    @RollPass.DiskElement.pillar_spreads
    def pillar_spreads(self: RollPass.DiskElement):
        rp = self.roll_pass
        return self.pillar_draughts ** -rp.hill_exponent


    PILLAR_MODEL_LOADED = True

except AttributeError:
    logging.getLogger(__name__).debug("Pillar model not loaded. Can not register respective hook function.")
