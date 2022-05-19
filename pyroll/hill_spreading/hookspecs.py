from pyroll.core import RollPass


@RollPass.hookspec
def hill_exponent(roll_pass: RollPass):
    """Gets the Hill spreading model exponent w."""


