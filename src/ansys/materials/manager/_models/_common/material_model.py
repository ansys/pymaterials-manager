from ansys.materials.manager._models._common.independent_parameter import IndependentParameter
from ._base import _BaseModel

class MaterialModel(_BaseModel):
    def __init__(
            self,
            name: str, 
            independent_parameters: list[IndependentParameter] | None = None, 
            definition: str | None = None, localized_name: str | None = None, 
            source: str | None = None, 
            type: str | None = None
            ) -> None:
        """
        Initialize a MaterialModel instance.

        Parameters
        ----------
        name : str
            The name of the material model.
        independent_parameters : list[IndependentParameter]
            List of independent parameters for the model.
        dependent_parameters : list[DependentParameter]
            List of dependent parameters for the model.
        """
        self.name = name
        self.independent_parameters = independent_parameters
        self.definition = definition
        self.localized_name = localized_name
        self.source = source
        self.type = type