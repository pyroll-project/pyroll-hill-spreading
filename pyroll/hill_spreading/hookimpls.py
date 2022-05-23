import numpy as np
from pyroll.core import RollPass


@RollPass.hookimpl
def hill_exponent(roll_pass: RollPass):
    equivalent_height_change = roll_pass.in_profile.equivalent_rectangle.height - roll_pass.out_profile.equivalent_rectangle.height
    in_equivalent_width = roll_pass.in_profile.equivalent_rectangle.width

    return 0.5 * np.exp(- in_equivalent_width / (2 * np.sqrt(roll_pass.roll.working_radius * equivalent_height_change)))


@RollPass.hookimpl
def spread(roll_pass: RollPass):
    compression = (roll_pass.in_profile.equivalent_rectangle.height
                   / roll_pass.out_profile.equivalent_rectangle.height)

    spread = compression ** roll_pass.hill_exponent

    return spread
