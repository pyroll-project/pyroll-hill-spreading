import numpy as np
from pyroll.core import RollPass
from pyroll.core.hooks import Hook

RollPass.hill_exponent = Hook[float]()


@RollPass.hill_exponent
def hill_exponent(self: RollPass):
    equivalent_height_change = self.in_profile.equivalent_rectangle.height - self.out_profile.equivalent_rectangle.height
    in_equivalent_width = self.in_profile.equivalent_rectangle.width

    return 0.5 * np.exp(- in_equivalent_width / (2 * np.sqrt(self.roll.working_radius * equivalent_height_change)))


@RollPass.OutProfile.width
def width(self: RollPass.OutProfile):
    roll_pass = self.roll_pass()

    equivalent_compression = (
            roll_pass.in_profile.equivalent_rectangle.height / roll_pass.out_profile.equivalent_rectangle.height)
    spread = equivalent_compression ** roll_pass.hill_exponent

    if not self.has_set_or_cached("width"):
        self.width = roll_pass.roll.groove.usable_width

    return spread * roll_pass.in_profile.width


RollPass.root_hooks.add(RollPass.OutProfile.width)
