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

from typing import Dict, Literal

from ansys.units import Quantity
from pydantic import Field, model_validator

from ansys.materials.manager._models._common import (
    MaterialModel,
    QualifierType,
    SupportedPackage,
    validate_and_initialize_model_qualifiers,
)


class CrystalPlasticity(MaterialModel):
    """Represents a crystal plasticity material model."""

    name: Literal["CrystalPlasticity"] = Field(default="CrystalPlasticity", repr=False, frozen=True)
    supported_packages: list[SupportedPackage] = Field(
        default=[SupportedPackage.MAPDL, SupportedPackage.FLUENT],
        title="Supported Packages",
        description="The list of supported packages.",
        frozen=True,
    )
    initial_hardness_per_slip_family: list[Quantity] | None = Field(
        default=None,
        description="The initial hardness for each slip family for the material.",
    )
    hardness_modulus_per_slip_family: list[Quantity] | None = Field(
        default=None,
        description="The hardness modulus for each slip family for the material.",
    )
    saturation_hardness_per_slip_family: list[Quantity] | None = Field(
        default=None,
        description="The saturation hardness for each slip family for the material.",
    )
    power_dependence_of_hardenss_moduli: list[Quantity] | None = Field(
        default=None,
        description="The power dependence of hardenss moduli for each slip family for the material.",  # noqa: E501
    )
    power_dependence_of_saturation_hardness: list[Quantity] | None = Field(
        default=None,
        description="The power dependence of saturation hardness for each slip family for the material.",  # noqa: E501
    )
    cross_hardness_parameter: Quantity | None = Field(
        default=None,
        description="The cross hardness parameter for the material.",
    )

    # all of the following
    slip_pre_exponential: Quantity | None = Field(
        default=None,
        description="The slip pre-exponential for the FCC, HCP and BCC material.",
    )
    lattice_c_by_a_ratio: Quantity | None = Field(
        default=None,
        description="The lattice c/a ratio for the FCC, HCP and BCC material.",
    )

    # FCC Material
    slip_power_dependence_1: Quantity | None = Field(
        default=None,
        description="The slip power dependence 1 for the FCC and HCP material.",
    )  # also for BCC
    slip_power_dependence_2: Quantity | None = Field(
        default=None,
        description="The slip power dependence 2 for the FCC and HCP material.",
    )  # also for BCC
    initial_ratio_of_slip_resistance: Quantity | None = Field(
        default=None,
        description="The initial ratio of slip resistance for the FCC material.",
    )
    activation_energy: Quantity | None = Field(
        default=None,
        description="The activation energy for the FCC material.",
    )

    # HCP Material
    slip_power_dependende_on_offset: Quantity | None = Field(
        default=None,
        description="The slip power dependence on offset for the HCP material.",
    )

    # BCC Material
    constant_ratio_of_slip_resistance: Quantity | None = Field(
        default=None,
        description="The constant ratio of slip resistance for the BCC material.",
    )
    activation_energy: Quantity | None = Field(
        default=None,
        description="The activation energy for the BCC material.",
    )

    @model_validator(mode="before")
    def _initialize_qualifiers(cls, values) -> Dict:
        expected_qualifiers = {
            "NumberOfSlipFamilies": ["FCC", QualifierType.FREE, ["FCC", "HCP"]],
            "FormulationNumber": [
                "Instantaneous",
                QualifierType.FREE,
                ["Power law", "Exponential"],
            ],
            "CrystalIndex": ["FCC", QualifierType.FREE, ["FCC", "HCP", "BCC"]],
            "OrientationTransformationMatrix": [
                "Straight",
                QualifierType.FREE,
                ["Straight", "Transformed"],
            ],
            "NumberOfSlipSystems": ["FCC", QualifierType.FREE, ["FCC", "HCP", "BCC"]],
            "SlipFamilyHardening": ["Yes", QualifierType.FREE, ["Yes", "No"]],
            "ActivatedSlipFamily": ["Active", QualifierType.FREE, ["Active", "Inactive"]],
        }
        values["model_qualifiers"] = validate_and_initialize_model_qualifiers(
            values, expected_qualifiers
        )
        return values

    def validate_model(self):
        """Override the validate_model implementation from the baseclass."""
        for qualifier in self.model_qualifiers:
            if qualifier.name == "CrystalIndex":
                crystal_index = qualifier.value

        is_fcc = crystal_index == "FCC"
        is_hcp = crystal_index == "HCP"
        is_bcc = crystal_index == "BCC"

        common_parameters = [self.slip_pre_exponential, self.lattice_c_by_a_ratio]
        fcc_bcc_common = [
            self.slip_power_dependence_1,
            self.slip_power_dependence_2,
            self.activation_energy,
        ]

        if is_fcc:
            for parameter in (
                [
                    self.initial_ratio_of_slip_resistance,
                ]
                + common_parameters
                + fcc_bcc_common
            ):
                if parameter is None:
                    raise Exception(
                        f"{parameter} has not been provided for the FCC crystal plasticity model."
                    )
        if is_hcp:
            for parameter in [
                self.slip_power_dependence_1,
                self.slip_power_dependence_2,
                self.slip_power_dependende_on_offset,
            ] + common_parameters:
                if parameter is None:
                    raise Exception(
                        f"{parameter} has not been provided for the HCP crystal plasticity model."
                    )
        if is_bcc:
            for parameter in (
                [
                    self.constant_ratio_of_slip_resistance,
                ]
                + common_parameters
                + fcc_bcc_common
            ):
                if parameter is None:
                    raise Exception(
                        f"{parameter} has not been provided for the BCC crystal plasticity model."
                    )
        super().validate_model()
