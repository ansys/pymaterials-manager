
ISOTROPIC_ELASTIC = """<?xml version="1.0" ?>
<Material>
  <BulkDetails>
    <Name>Isotropic Test Material</Name>
    <PropertyData property="pr0">
      <Data format="string">-</Data>
      <Qualifier name="Behavior">Isotropic</Qualifier>
      <ParameterValue parameter="pa0" format="string">
        <Data>Interpolation Options</Data>
        <Qualifier name="AlgorithmType">Linear Multivariate</Qualifier>
        <Qualifier name="Cached">True</Qualifier>
        <Qualifier name="Normalized">True</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa1" format="float">
        <Data>1000000.0</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa2" format="float">
        <Data>0.3</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa3" format="float">
        <Data>7.88860905221012e-31</Data>
        <Qualifier name="Variable Type">Independent</Qualifier>
        <Qualifier name="Field Variable">Temperarture</Qualifier>
        <Qualifier name="Default Data">22.0</Qualifier>
        <Qualifier name="Field Units">C</Qualifier>
        <Qualifier name="Upper Limit">1.18329135783152E-30</Qualifier>
        <Qualifier name="Lower Limit">3.94430452610506E-31</Qualifier>
      </ParameterValue>
    </PropertyData>
  </BulkDetails>
</Material>"""

ISOTROPIC_ELASTICITY_VARIABLE = """<?xml version="1.0" ?>
<Material>
  <BulkDetails>
    <Name>Variable Isotropic Test Material</Name>
    <PropertyData property="pr0">
      <Data format="string">-</Data>
      <Qualifier name="Behavior">Isotropic</Qualifier>
      <ParameterValue parameter="pa0" format="string">
        <Data>Interpolation Options</Data>
        <Qualifier name="AlgorithmType">Linear Multivariate</Qualifier>
        <Qualifier name="Cached">True</Qualifier>
        <Qualifier name="Normalized">True</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa1" format="float">
        <Data>2000000.0, 1000000.0</Data>
        <Qualifier name="Variable Type">Dependent,Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa2" format="float">
        <Data>0.35, 0.3</Data>
        <Qualifier name="Variable Type">Dependent,Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa3" format="float">
        <Data>12.0, 21.0</Data>
        <Qualifier name="Variable Type">Independent,Independent</Qualifier>
        <Qualifier name="Field Variable">Temperarture</Qualifier>
        <Qualifier name="Default Data">22.0</Qualifier>
        <Qualifier name="Field Units">C</Qualifier>
        <Qualifier name="Upper Limit">1.18329135783152E-30</Qualifier>
        <Qualifier name="Lower Limit">3.94430452610506E-31</Qualifier>
      </ParameterValue>
    </PropertyData>
  </BulkDetails>
</Material>"""

ORTHOTROPIC_ELASTICITY = """<?xml version="1.0" ?>
<Material>
  <BulkDetails>
    <Name>Orthotropic Test Material</Name>
    <PropertyData property="pr0">
      <Data format="string">-</Data>
      <Qualifier name="Behavior">Orthotropic</Qualifier>
      <ParameterValue parameter="pa0" format="string">
        <Data>Interpolation Options</Data>
        <Qualifier name="AlgorithmType">Linear Multivariate</Qualifier>
        <Qualifier name="Cached">True</Qualifier>
        <Qualifier name="Normalized">True</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa1" format="float">
        <Data>1000000.0</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa2" format="float">
        <Data>1500000.0</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa3" format="float">
        <Data>2000000.0</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa4" format="float">
        <Data>0.3</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa5" format="float">
        <Data>0.4</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa6" format="float">
        <Data>0.2</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa7" format="float">
        <Data>2000000.0</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa8" format="float">
        <Data>3000000.0</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa9" format="float">
        <Data>1000000.0</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa10" format="float">
        <Data>7.88860905221012e-31</Data>
        <Qualifier name="Variable Type">Independent</Qualifier>
        <Qualifier name="Field Variable">Temperarture</Qualifier>
        <Qualifier name="Default Data">22.0</Qualifier>
        <Qualifier name="Field Units">C</Qualifier>
        <Qualifier name="Upper Limit">1.18329135783152E-30</Qualifier>
        <Qualifier name="Lower Limit">3.94430452610506E-31</Qualifier>
      </ParameterValue>
    </PropertyData>
  </BulkDetails>
</Material>"""

ORTHOTROPIC_ELASTICITY_VARIABLE = """<?xml version="1.0" ?>
<Material>
  <BulkDetails>
    <Name>Variable Orthotropic Test Material</Name>
    <PropertyData property="pr0">
      <Data format="string">-</Data>
      <Qualifier name="Behavior">Orthotropic</Qualifier>
      <ParameterValue parameter="pa0" format="string">
        <Data>Interpolation Options</Data>
        <Qualifier name="AlgorithmType">Linear Multivariate</Qualifier>
        <Qualifier name="Cached">True</Qualifier>
        <Qualifier name="Normalized">True</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa1" format="float">
        <Data>1000000.0, 11000000.0</Data>
        <Qualifier name="Variable Type">Dependent,Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa2" format="float">
        <Data>1500000.0, 15100000.0</Data>
        <Qualifier name="Variable Type">Dependent,Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa3" format="float">
        <Data>2000000.0, 21000000.0</Data>
        <Qualifier name="Variable Type">Dependent,Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa4" format="float">
        <Data>0.3, 0.31</Data>
        <Qualifier name="Variable Type">Dependent,Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa5" format="float">
        <Data>0.4, 0.41</Data>
        <Qualifier name="Variable Type">Dependent,Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa6" format="float">
        <Data>0.2, 0.21</Data>
        <Qualifier name="Variable Type">Dependent,Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa7" format="float">
        <Data>2000000.0, 2100000.0</Data>
        <Qualifier name="Variable Type">Dependent,Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa8" format="float">
        <Data>3000000.0, 3100000.0</Data>
        <Qualifier name="Variable Type">Dependent,Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa9" format="float">
        <Data>1000000.0, 1100000.0</Data>
        <Qualifier name="Variable Type">Dependent,Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa10" format="float">
        <Data>21.0, 22.0</Data>
        <Qualifier name="Variable Type">Independent,Independent</Qualifier>
        <Qualifier name="Field Variable">Temperarture</Qualifier>
        <Qualifier name="Default Data">22.0</Qualifier>
        <Qualifier name="Field Units">C</Qualifier>
        <Qualifier name="Upper Limit">1.18329135783152E-30</Qualifier>
        <Qualifier name="Lower Limit">3.94430452610506E-31</Qualifier>
      </ParameterValue>
    </PropertyData>
  </BulkDetails>
</Material>"""

ANISOTROPIC_ELASTICITY = """<?xml version="1.0" ?>
<Material>
  <BulkDetails>
    <Name>Anisotropic Test Material</Name>
    <PropertyData property="pr0">
      <Data format="string">-</Data>
      <Qualifier name="Behavior">Anisotropic</Qualifier>
      <ParameterValue parameter="pa0" format="float">
        <Data>100000000.0, 1000000.0, 2000000.0, 3000000.0, 4000000.0, 5000000.0</Data>
        <Qualifier name="Variable Type">Dependent,Dependent,Dependent,Dependent,Dependent,Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa1" format="float">
        <Data>7.88860905221012e-31, 150000000.0, 6000000.0, 7000000.0, 8000000.0, 9000000.0</Data>
        <Qualifier name="Variable Type">Dependent,Dependent,Dependent,Dependent,Dependent,Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa2" format="float">
        <Data>7.88860905221012e-31, 7.88860905221012e-31, 200000000.0, 10000000.0, 11000000.0, 12000000.0</Data>
        <Qualifier name="Variable Type">Dependent,Dependent,Dependent,Dependent,Dependent,Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa3" format="float">
        <Data>7.88860905221012e-31, 7.88860905221012e-31, 7.88860905221012e-31, 50000000.0, 13000000.0, 14000000.0</Data>
        <Qualifier name="Variable Type">Dependent,Dependent,Dependent,Dependent,Dependent,Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa4" format="float">
        <Data>7.88860905221012e-31, 7.88860905221012e-31, 7.88860905221012e-31, 7.88860905221012e-31, 60000000.0, 15000000.0</Data>
        <Qualifier name="Variable Type">Dependent,Dependent,Dependent,Dependent,Dependent,Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa5" format="float">
        <Data>7.88860905221012e-31, 7.88860905221012e-31, 7.88860905221012e-31, 7.88860905221012e-31, 7.88860905221012e-31, 70000000.0</Data>
        <Qualifier name="Variable Type">Dependent,Dependent,Dependent,Dependent,Dependent,Dependent</Qualifier>
      </ParameterValue>
    </PropertyData>
  </BulkDetails>
</Material>"""  # noqa: E501

ISOTROPIC_ELASTICITY_METADATA = """<?xml version="1.0" ?>
<Metadata>
  <PropertyDetails id="pr0">
    <Unitless/>
    <Name>Elasticity</Name>
  </PropertyDetails>
  <ParameterDetails id="pa0">
    <Unitless/>
    <Name>Options Variable</Name>
  </ParameterDetails>
  <ParameterDetails id="pa1">
    <Units>
      <Unit>
        <Name>Pa</Name>
      </Unit>
    </Units>
    <Name>Young's Modulus</Name>
  </ParameterDetails>
  <ParameterDetails id="pa2">
    <Unitless/>
    <Name>Poisson's Ratio</Name>
  </ParameterDetails>
  <ParameterDetails id="pa3">
    <Units>
      <Unit>
        <Name>C</Name>
      </Unit>
    </Units>
    <Name>Temperature</Name>
  </ParameterDetails>
</Metadata>"""

ORTHOTROPIC_ELASTICITY_METADATA = """<?xml version="1.0" ?>
<Metadata>
  <PropertyDetails id="pr0">
    <Unitless/>
    <Name>Elasticity</Name>
  </PropertyDetails>
  <ParameterDetails id="pa0">
    <Unitless/>
    <Name>Options Variable</Name>
  </ParameterDetails>
  <ParameterDetails id="pa1">
    <Unitless/>
    <Name>Young's Modulus X direction</Name>
  </ParameterDetails>
  <ParameterDetails id="pa2">
    <Unitless/>
    <Name>Young's Modulus Y direction</Name>
  </ParameterDetails>
  <ParameterDetails id="pa3">
    <Unitless/>
    <Name>Young's Modulus Z direction</Name>
  </ParameterDetails>
  <ParameterDetails id="pa4">
    <Unitless/>
    <Name>Poisson's Ratio YZ</Name>
  </ParameterDetails>
  <ParameterDetails id="pa5">
    <Unitless/>
    <Name>Poisson's Ratio XZ</Name>
  </ParameterDetails>
  <ParameterDetails id="pa6">
    <Unitless/>
    <Name>Poisson's Ratio XY</Name>
  </ParameterDetails>
  <ParameterDetails id="pa7">
    <Unitless/>
    <Name>Shear Modulus YZ</Name>
  </ParameterDetails>
  <ParameterDetails id="pa8">
    <Unitless/>
    <Name>Shear Modulus XZ</Name>
  </ParameterDetails>
  <ParameterDetails id="pa9">
    <Unitless/>
    <Name>Shear Modulus XY</Name>
  </ParameterDetails>
  <ParameterDetails id="pa10">
    <Unitless/>
    <Name>Temperature</Name>
  </ParameterDetails>
</Metadata>"""

ANISOTROPIC_ELASTICITY_METADATA = """<?xml version="1.0" ?>
<Metadata>
  <PropertyDetails id="pr0">
    <Unitless/>
    <Name>Elasticity</Name>
  </PropertyDetails>
  <ParameterDetails id="pa0">
    <Unitless/>
    <Name>D[*,1]</Name>
  </ParameterDetails>
  <ParameterDetails id="pa1">
    <Unitless/>
    <Name>D[*,2]</Name>
  </ParameterDetails>
  <ParameterDetails id="pa2">
    <Unitless/>
    <Name>D[*,3]</Name>
  </ParameterDetails>
  <ParameterDetails id="pa3">
    <Unitless/>
    <Name>D[*,4]</Name>
  </ParameterDetails>
  <ParameterDetails id="pa4">
    <Unitless/>
    <Name>D[*,5]</Name>
  </ParameterDetails>
  <ParameterDetails id="pa5">
    <Unitless/>
    <Name>D[*,6]</Name>
  </ParameterDetails>
</Metadata>"""
