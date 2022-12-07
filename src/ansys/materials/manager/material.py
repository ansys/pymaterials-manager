from typing import List, Optional

from ._models import _BaseModel
from ._models._common.constant import Constant


class Material:
    """
    Wrapper class for a material.

    Associates a material_id with one or more properties and nonlinear material models.
    """

    _models: List[_BaseModel]
    _id: str
    _name: str

    def __init__(
        self,
        material_name: str,
        material_id: str = None,
        models: List[_BaseModel] = None,
        reference_temperature: float = 0.0,
    ):
        """
        Create a new instance of a Material.

        Optionally specify a material ID, or other properties.

        Parameters
        ----------
        material_name: s:wtr
            The name of the material
        material_id: str
            The ID to be associated with this material.
        models: Dict[str, _BaseModel]
            Dictionary of nonlinear material models. Specified with their model code (from the
            TB command), and the model object.
        reference_temperature: float
            Reference temperature for this material, affects thermal expansion and some non-linear
            models. Default 0.0

        """
        self._models = []
        self._name = material_name
        self._id = material_id
        if models is not None:
            self.models.extend(models)
        if len(self.get_model_by_name("reference temperature")) == 0:
            self.models.append(Constant("Reference Temperature", reference_temperature))

    @property
    def name(self) -> str:
        """Return the name of the material."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def material_id(self) -> Optional[str]:
        """Return the material ID."""
        return self._id

    @material_id.setter
    def material_id(self, value: str):
        self._id = value

    @property
    def models(self) -> "List[_BaseModel]":
        """Return the currently assigned material models."""
        return self._models

    def get_model_by_name(self, model_name: str) -> "List[_BaseModel]":
        """Return the material model or models with the specified model name."""
        return [model for model in self.models if model.name.lower() == model_name.lower()]

    @property
    def reference_temperature(self) -> float:
        """Return the current reference temperature for the model."""
        reference_temperature = self.get_model_by_name("reference temperature")[0]
        assert isinstance(reference_temperature, Constant)
        return reference_temperature.value

    @reference_temperature.setter
    def reference_temperature(self, value: float) -> None:
        reference_temperature = self.get_model_by_name("reference temperature")[0]
        assert isinstance(reference_temperature, Constant)
        reference_temperature.value = value
