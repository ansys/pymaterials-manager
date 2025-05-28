class IndependentParameter:
    """Class representing an independent parameter in a material model.

    Parameters
    ----------
    name: str
        The name of the independent parameter.
    values: list[float]
        The value of the independent parameter.
    default_value: float
        The default value of the independent parameter.
    units: str
        The units of the independent parameter.
    resolution: str | None
    
    upper_limit: str | float | None
        upper limit of the independent parameter.
    lower_limit: str | float | None
        lower limit of the independent parameter.
    """

    def __init__(self, name: str, values: float, default_value: float, units: str, resolution: str | None = None,
                 upper_limit: str | float | None = None, lower_limit: str | float | None = None) -> None:
        self.name = name
        self.values = values
        self.default_value = default_value
        self.units = units
        self.resolution = resolution
        self.upper_limit = upper_limit
        self.lower_limit = lower_limit

    def __repr__(self) -> str:
        return (
            f"IndependentParameter(name={self.name}, value={self.values}, default_value={self.default_value}, " 
            + f"units={self.units}, resolution={self.resolution}, upper_limit={self.upper_limit}, " 
            + f"lower_limit={self.lower_limit}")