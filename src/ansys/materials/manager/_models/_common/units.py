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

from enum import Enum
from typing import Any, Union

from pydantic import BaseModel, Field


class Uniteless(str, Enum):
    """Unitless class."""

    UNITLESS = "Unitless"


class LengthUnits(str, Enum):
    """Class to represent length units."""

    KILOMETERS = "km"
    METERS = "m"
    DECIMETERS = "dm"
    CENTIMETERS = "cm"
    HECTOMETERS = "hm"
    MILLIMETERS = "mm"
    MICROMETERS = "µm"
    NANOMETERS = "nm"
    INCHES = "in"
    FEET = "ft"


class MassUnits(str, Enum):
    """Class to represent mass units."""

    TONNE = ""
    KILOGRAMS = "kg"
    HECTOGRAMS = "hg"
    DECAGRAMS = "dag"
    GRAMS = "g"
    MILLIGRAMS = "mg"
    POUNDS = "lb"
    OUNCES = "oz"


class TemperatureUnits(str, Enum):
    """Class to represent temperature units."""

    CELSIUS = "C"
    FAHRENHEIT = "F"
    KELVIN = "K"


class PressureUnits(str, Enum):
    """Class to represent pressure units."""

    PASCALS = "Pa"
    KILOPASCALS = "kPa"
    MEGAPASCALS = "MPa"
    GIGAPASCALS = "GPa"
    BARS = "bar"
    PSI = "psi"
    ATMOSPHERES = "atm"


class TimeUnits(str, Enum):
    """Class to represent time units."""

    SECONDS = "s"
    MINUTES = "min"
    HOURS = "h"
    DAYS = "d"


class EnergyUnits(str, Enum):
    """Class to represent energy units."""

    JOULES = "J"
    KILOJOULES = "kJ"
    CALORIES = "cal"
    KILOCALORIES = "kcal"
    BTU = "BTU"
    WATT = "W"


class AngleUnits(str, Enum):
    """Class to represent angle units."""

    DEGREES = "degrees"
    RADIANS = "radians"
    GRADIANS = "gradians"


class ElectricCurrentUnits(str, Enum):
    """Class to represent electric current units."""

    BIOT = "Bi"
    AMPERES = "A"
    MILLIAMPERES = "mA"
    MICROAMPERES = "uA"
    NANOAMPERES = "nA"
    OHM = "Ohm"


class LuminousIntesityUnits(str, Enum):
    """Class to represent luminous intensity units."""

    CANDELAS = "cd"
    LUMENS = "lm"
    LUX = "lx"


class AmountOfSubstanceUnits(str, Enum):
    """Class to represent amount of substance units."""

    MOLES = "mol"
    MILLIMOLES = "mmol"
    MICROMOLES = "umol"


class DensityUnits(str, Enum):
    """Class to represent derived units."""

    DENSITY_G_CM3 = "g*cm^-3"
    DENSITY_KG_M3 = "kg*m^-3"
    DENSITY_G_ML = "g*mL^-1"
    DENSITY_LB_FT3 = "lb*ft^-3"
    DENSITY_SLUG = "slug*ft^-3"


class ForceUnits(str, Enum):
    """Class to represent force units."""

    NEWTONS = "N"
    KILONEWTONS = "kN"
    POUNDS_FORCE = "lbf"
    DYNE = "dyn"


class PhysicalDimension(BaseModel):
    """Class to represent physical dimensions of a unit."""

    length: int = Field(default=0, title="Length", description="Dimension of length")
    mass: int = Field(default=0, title="Mass", description="Dimension of mass")
    time: int = Field(default=0, title="Time", description="Dimension of time")
    temperature: int = Field(default=0, title="Temperature", description="Dimension of temperature")
    electric_current: int = Field(
        default=0, title="Electric Current", description="Dimension of electric current"
    )
    luminous_intensity: int = Field(
        default=0, title="Luminous Intensity", description="Dimension of luminous intensity"
    )
    amount_of_substance: int = Field(
        default=0, title="Amount of Substance", description="Dimension of amount of substance"
    )
    angle: int = Field(default=0, title="Angle", description="Dimension of angle")


Units = Union[
    LengthUnits,
    MassUnits,
    TemperatureUnits,
    PressureUnits,
    TimeUnits,
    EnergyUnits,
    AngleUnits,
    ElectricCurrentUnits,
    LuminousIntesityUnits,
    AmountOfSubstanceUnits,
    DensityUnits,
    Uniteless,
]


class MeasuredUnit(BaseModel):
    """Class to represent a measured unit with its name, dimension, and unit."""

    name: str = Field(default="", title="Name", description="Name of the unit")
    dimension: PhysicalDimension = Field(
        default_factory=PhysicalDimension,
        title="Physical Dimension",
        description="Physical dimension of the unit",
    )
    unit: Any = Field(default=None, title="Unit", description="Unit of measurement")


UNIT_REGISTRY = {
    # length units
    "nm": MeasuredUnit(
        name="nanometers", dimension=PhysicalDimension(length=1), unit=LengthUnits.NANOMETERS
    ),
    "um": MeasuredUnit(
        name="micrometers", dimension=PhysicalDimension(length=1), unit=LengthUnits.MICROMETERS
    ),
    "mm": MeasuredUnit(
        name="millimeters", dimension=PhysicalDimension(length=1), unit=LengthUnits.MILLIMETERS
    ),
    "cm": MeasuredUnit(
        name="centimeters", dimension=PhysicalDimension(length=1), unit=LengthUnits.CENTIMETERS
    ),
    "dm": MeasuredUnit(
        name="decimeters", dimension=PhysicalDimension(length=1), unit=LengthUnits.DECIMETERS
    ),
    "m": MeasuredUnit(
        name="meters", dimension=PhysicalDimension(length=1), unit=LengthUnits.METERS
    ),
    "hm": MeasuredUnit(
        name="hectometers", dimension=PhysicalDimension(length=1), unit=LengthUnits.HECTOMETERS
    ),
    "km": MeasuredUnit(
        name="kilometers", dimension=PhysicalDimension(length=1), unit=LengthUnits.KILOMETERS
    ),
    "in": MeasuredUnit(
        name="inches", dimension=PhysicalDimension(length=1), unit=LengthUnits.INCHES
    ),
    "ft": MeasuredUnit(name="feet", dimension=PhysicalDimension(length=1), unit=LengthUnits.FEET),
    # mass units
    "kg": MeasuredUnit(
        name="kilograms", dimension=PhysicalDimension(mass=1), unit=MassUnits.KILOGRAMS
    ),
    "hg": MeasuredUnit(
        name="hectograms", dimension=PhysicalDimension(mass=1), unit=MassUnits.HECTOGRAMS
    ),
    "dag": MeasuredUnit(
        name="decagrams", dimension=PhysicalDimension(mass=1), unit=MassUnits.DECAGRAMS
    ),
    "g": MeasuredUnit(name="grams", dimension=PhysicalDimension(mass=1), unit=MassUnits.GRAMS),
    "mg": MeasuredUnit(
        name="milligrams", dimension=PhysicalDimension(mass=1), unit=MassUnits.MILLIGRAMS
    ),
    "lb": MeasuredUnit(name="pounds", dimension=PhysicalDimension(mass=1), unit=MassUnits.POUNDS),
    "oz": MeasuredUnit(name="ounces", dimension=PhysicalDimension(mass=1), unit=MassUnits.OUNCES),
    # temperature units
    "C": MeasuredUnit(
        name="celsius", dimension=PhysicalDimension(temperature=1), unit=TemperatureUnits.CELSIUS
    ),
    "F": MeasuredUnit(
        name="fahrenheit",
        dimension=PhysicalDimension(temperature=1),
        unit=TemperatureUnits.FAHRENHEIT,
    ),
    "K": MeasuredUnit(
        name="kelvin", dimension=PhysicalDimension(temperature=1), unit=TemperatureUnits.KELVIN
    ),
    # pressure units
    "Pa": MeasuredUnit(
        name="pascals",
        dimension=PhysicalDimension(length=-1, mass=1, time=-2),
        unit=PressureUnits.PASCALS,
    ),
    "kPa": MeasuredUnit(
        name="kilopascals",
        dimension=PhysicalDimension(length=-1, mass=1, time=-2),
        unit=PressureUnits.KILOPASCALS,
    ),
    "MPa": MeasuredUnit(
        name="megapascals",
        dimension=PhysicalDimension(length=-1, mass=1, time=-2),
        unit=PressureUnits.MEGAPASCALS,
    ),
    "GPa": MeasuredUnit(
        name="gigapascals",
        dimension=PhysicalDimension(length=-1, mass=1, time=-2),
        unit=PressureUnits.GIGAPASCALS,
    ),
    "bar": MeasuredUnit(
        name="bars",
        dimension=PhysicalDimension(length=-1, mass=1, time=-2),
        unit=PressureUnits.BARS,
    ),
    "psi": MeasuredUnit(
        name="pounds per square inch",
        dimension=PhysicalDimension(length=-1, mass=1, time=-2),
        unit=PressureUnits.PSI,
    ),
    "atm": MeasuredUnit(
        name="atmospheres",
        dimension=PhysicalDimension(length=-1, mass=1, time=-2),
        unit=PressureUnits.ATMOSPHERES,
    ),
    # energy units
    "J": MeasuredUnit(
        name="joules",
        dimension=PhysicalDimension(length=2, mass=1, time=-2),
        unit=EnergyUnits.JOULES,
    ),
    "kJ": MeasuredUnit(
        name="kilojoules",
        dimension=PhysicalDimension(length=2, mass=1, time=-2),
        unit=EnergyUnits.KILOJOULES,
    ),
    "cal": MeasuredUnit(
        name="calories",
        dimension=PhysicalDimension(length=2, mass=1, time=-2),
        unit=EnergyUnits.CALORIES,
    ),
    "kcal": MeasuredUnit(
        name="kilocalories",
        dimension=PhysicalDimension(length=2, mass=1, time=-2),
        unit=EnergyUnits.KILOCALORIES,
    ),
    "BTU": MeasuredUnit(
        name="British thermal units",
        dimension=PhysicalDimension(length=2, mass=1, time=-2),
        unit=EnergyUnits.BTU,
    ),
    "W": MeasuredUnit(
        name="watts", dimension=PhysicalDimension(length=2, mass=1, time=-3), unit=EnergyUnits.WATT
    ),
    # angle units
    "degrees": MeasuredUnit(
        name="degrees", dimension=PhysicalDimension(angle=1), unit=AngleUnits.DEGREES
    ),
    "radians": MeasuredUnit(name="radians", dimension=PhysicalDimension(), unit=AngleUnits.RADIANS),
    "gradians": MeasuredUnit(
        name="gradians", dimension=PhysicalDimension(), unit=AngleUnits.GRADIANS
    ),
    # density units
    "g*cm^-3": MeasuredUnit(
        name="grams per cubic centimeter",
        dimension=PhysicalDimension(length=-3, mass=1),
        unit=DensityUnits.DENSITY_G_CM3,
    ),
    "kg*m^-3": MeasuredUnit(
        name="kilograms per cubic meter",
        dimension=PhysicalDimension(length=-3, mass=1),
        unit=DensityUnits.DENSITY_KG_M3,
    ),
    "g*mL^-1": MeasuredUnit(
        name="grams per milliliter",
        dimension=PhysicalDimension(length=-1, mass=1),
        unit=DensityUnits.DENSITY_G_ML,
    ),
    "lb*ft^-3": MeasuredUnit(
        name="pounds per cubic foot",
        dimension=PhysicalDimension(length=-3, mass=1),
        unit=DensityUnits.DENSITY_LB_FT3,
    ),
    "slug*ft^-3": MeasuredUnit(
        name="slugs per cubic foot",
        dimension=PhysicalDimension(length=-3, mass=1),
        unit=DensityUnits.DENSITY_SLUG,
    ),
    # force units
    "N": MeasuredUnit(
        name="newtons",
        dimension=PhysicalDimension(length=1, mass=1, time=-2),
        unit=ForceUnits.NEWTONS,
    ),
    "kN": MeasuredUnit(
        name="kilonewtons",
        dimension=PhysicalDimension(length=1, mass=1, time=-2),
        unit=ForceUnits.KILONEWTONS,
    ),
    "lbf": MeasuredUnit(
        name="pounds-force",
        dimension=PhysicalDimension(length=1, mass=1, time=-2),
        unit=ForceUnits.POUNDS_FORCE,
    ),
    "dyn": MeasuredUnit(
        name="dynes", dimension=PhysicalDimension(length=1, mass=1, time=-2), unit=ForceUnits.DYNE
    ),
    # unitless
    "Unitless": MeasuredUnit(
        name="unitless", dimension=PhysicalDimension(), unit=Uniteless.UNITLESS
    ),
}


def get_unit_by_symbol(symbol: str) -> MeasuredUnit:
    """Retrieve a unit from the registry by its symbol."""
    if symbol in UNIT_REGISTRY.keys():
        return UNIT_REGISTRY[symbol]
    else:
        raise ValueError(f"Unit with symbol '{symbol}' not found in registry.")


def are_units_compatible(unit1: Units, unit2: Units) -> bool:
    """Check if two units are compatible based on their physical dimensions."""
    for attributes in UNIT_REGISTRY.values():
        if attributes.unit == unit1:
            dimensions_1 = attributes.dimension
        if attributes.unit == unit2:
            dimensions_2 = attributes.dimension
        try:
            if (
                dimensions_1.length == dimensions_2.length
                and dimensions_1.mass == dimensions_2.mass
                and dimensions_1.time == dimensions_2.time
                and dimensions_1.temperature == dimensions_2.temperature
                and dimensions_1.electric_current == dimensions_2.electric_current
                and dimensions_1.luminous_intensity == dimensions_2.luminous_intensity
                and dimensions_1.amount_of_substance == dimensions_2.amount_of_substance
                and dimensions_1.angle == dimensions_2.angle
            ):
                return True
            else:
                return False
        except:
            raise ValueError(f"Units '{unit1}' or '{unit2}' are is not recognized.")
    raise ValueError(f"Units '{unit1}' and '{unit2}' are not compatible.")
