class DependentParameter:
    """A class representing a dependent parameter in a material model.

    Parameters
    ----------
    name: str
        The name of the dependent parameter.
    values: list[float] 
        The values of the dependent parameter.
    """

    def __init__(self, name: str, values: list[float]) -> None:
        self.name = name
        self.values = values
        #self.mapping 

    def __repr__(self) -> str:
        return f"DependentParameter(name={self.name}, value={self.values})"