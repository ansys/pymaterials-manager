from unittest.mock import MagicMock
from ansys.materials.manager._models._material_models.density import Density
from ansys.units import Quantity
from ansys.materials.manager._models._common._base import _MapdlCore
from ansys.materials.manager._models._common.independent_parameter import IndependentParameter

# def test_write_constant_density_apdl():
density = Density(
    density=Quantity(value=[1.34], units="kg m^-3"),
)
mock_mapdl = MagicMock(spec=_MapdlCore)
material_string = density.write_model(material_id=1, pyansys_session=mock_mapdl)
print(material_string)
# assert material_string == "MP, DENS, 1, 1.34"

density = Density(
    density=Quantity(value=[1.34, 2.5], units="kg m^-3"),
    independent_parameters=[IndependentParameter(name="Temperature", 
                                                values=Quantity(value=[22, 30], units="C"))]
)
mock_mapdl = MagicMock(spec=_MapdlCore)
material_string = density.write_model(material_id=1, pyansys_session=mock_mapdl)
print(material_string)