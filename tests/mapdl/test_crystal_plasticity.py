from ansys.materials.manager._models._common.model_qualifier import ModelQualifier
from ansys.materials.manager._models._material_models.crystal_plasticity import CrystalPlasticity

model_qualifiers = [
    ModelQualifier(name="NumberOfSlipFamilies", value="FCC"),
    ModelQualifier(name="FormulationNumber", value="Exponential"),
    ModelQualifier(name="CrystalIndex", value="FCC"),
    ModelQualifier(name="OrientationTransformationMatrix", value="Straight"),
    ModelQualifier(name="NumberOfSlipSystems", value="FCC"),
    ModelQualifier(name="SlipFamilyHardening", value="Yes"),
    ModelQualifier(name="ActivatedSlipFamily", value="Active"),
]

CrystalPlasticity(model_qualifiers=model_qualifiers)
