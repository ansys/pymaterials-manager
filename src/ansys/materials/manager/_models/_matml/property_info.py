# Copyright (C) 2022 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class PropertyInfo:
    """MatML property information."""

    """The unit category of the material property.

    For unitless properties, this will be None
    For properties with units, this can be defined but is not strictly necessary.
    """
    unit_category: Optional[str]


property_infos: Dict[str, PropertyInfo] = {
    "young's modulus x direction": PropertyInfo("Stress"),
    "young's modulus y direction": PropertyInfo("Stress"),
    "young's modulus z direction": PropertyInfo("Stress"),
    "secant thermal expansion coefficient x direction": PropertyInfo(None),
    "secant thermal expansion coefficient y direction": PropertyInfo(None),
    "secant thermal expansion coefficient z direction": PropertyInfo(None),
    "instantaneous thermal expansion coefficient x direction": PropertyInfo(None),
    "instantaneous thermal expansion coefficient y direction": PropertyInfo(None),
    "instantaneous thermal expansion coefficient z direction": PropertyInfo(None),
    "strain reference temperature": PropertyInfo("Temperature"),
    "poisson's ratio xy": PropertyInfo(None),
    "poisson's ratio yz": PropertyInfo(None),
    "poisson's ratio xz": PropertyInfo(None),
    "shear modulus xy": PropertyInfo("Stress"),
    "shear modulus yz": PropertyInfo("Stress"),
    "shear modulus xz": PropertyInfo("Stress"),
    "coefficient of friction": PropertyInfo(None),
    "density": PropertyInfo("Density"),
    "specific heat capacity": PropertyInfo("Specific Heat Capacity"),
    "enthalpy": PropertyInfo("MAPDL Enthalpy"),
    "thermal conductivity x direction": PropertyInfo("Thermal Conductivity"),
    "thermal conductivity y direction": PropertyInfo("Thermal Conductivity"),
    "thermal conductivity z direction": PropertyInfo("Thermal Conductivity"),
    "convection coefficient": PropertyInfo(None),
    "emissivity": PropertyInfo(None),
    "heat generation rate": PropertyInfo(None),
    "viscosity": PropertyInfo("Dynamic Viscosity"),
    "speed of sound": PropertyInfo("Velocity"),
    "electrical resistivity x direction": PropertyInfo("Electrical Resistivity"),
    "electrical resistivity y direction": PropertyInfo("Electrical Resistivity"),
    "electrical resistivity z direction": PropertyInfo("Electrical Resistivity"),
    "electric relative permittivity x direction": PropertyInfo(None),
    "electric relative permittivity y direction": PropertyInfo(None),
    "electric relative permittivity z direction": PropertyInfo(None),
    "magnetic relative permeability x direction": PropertyInfo(None),
    "magnetic relative permeability y direction": PropertyInfo(None),
    "magnetic relative permeability z direction": PropertyInfo(None),
    "magnetic coercive force x direction": PropertyInfo(None),
    "magnetic coercive force y direction": PropertyInfo(None),
    "magnetic coercive force z direction": PropertyInfo(None),
    "dielectric loss tangent": PropertyInfo(None),
    "seebeck coefficient x direction": PropertyInfo(None),
    "seebeck coefficient y direction": PropertyInfo(None),
    "seebeck coefficient z direction": PropertyInfo(None),
}
