# Copyright (C) 2022 - 2026 ANSYS, Inc. and/or its affiliates.
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

from ansys.materials.manager._models._material_models.density import Density
from ansys.materials.manager._models._material_models.elasticity_anisotropic import (
    ElasticityAnisotropic,
)
from ansys.materials.manager._models._material_models.elasticity_isotropic import (
    ElasticityIsotropic,
)
from ansys.materials.manager._models._material_models.elasticity_orthotropic import (
    ElasticityOrthotropic,
)
from ansys.materials.manager.parsers._common import ModelInfo

MATERIAL_MODEL_MAP = {
    Density: ModelInfo(labels=["ro"], attributes=["density"]),
    ElasticityIsotropic: ModelInfo(
        labels=["e", "pr"], attributes=["youngs_modulus", "poissons_ratio"]
    ),
    ElasticityOrthotropic: ModelInfo(
        labels=[
            "ea",
            "eb",
            "ec",
            "gab",
            "gbc",
            "gca",
            "prba",
            "prcb",
            "prca",
        ],
        attributes=[
            "youngs_modulus_x",
            "youngs_modulus_y",
            "youngs_modulus_z",
            "shear_modulus_xy",
            "shear_modulus_yz",
            "shear_modulus_xz",
            "poissons_ratio_xy",
            "poissons_ratio_yz",
            "poissons_ratio_xz",
        ],
    ),
    ElasticityAnisotropic: ModelInfo(
        labels=[
            "c11",
            "c12",
            "c13",
            "c14",
            "c15",
            "c16",
            "c22",
            "c23",
            "c24",
            "c25",
            "c26",
            "c33",
            "c34",
            "c35",
            "c36",
            "c44",
            "c45",
            "c46",
            "c55",
            "c56",
            "c66",
        ],
        attributes=[
            "c_11",
            "c_12",
            "c_13",
            "c_14",
            "c_15",
            "c_16",
            "c_22",
            "c_23",
            "c_24",
            "c_25",
            "c_26",
            "c_33",
            "c_34",
            "c_35",
            "c_36",
            "c_44",
            "c_45",
            "c_46",
            "c_55",
            "c_56",
            "c_66",
        ],
    ),
}
