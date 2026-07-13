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

import pytest

from ansys.materials.manager.integrations.fluent._fluent_model_map import (
    MATERIAL_MODEL_MAP as FLUENT_MAP,
)
from ansys.materials.manager.integrations.fluent.fluent_writer import FluentWriter
from ansys.materials.manager.integrations.lsdyna._ls_dyna_model_map import (
    MATERIAL_MODEL_MAP as LSDYNA_MAP,
)
from ansys.materials.manager.integrations.lsdyna.lsdyna_writer import LsDynaWriter
from ansys.materials.manager.integrations.mapdl._mapdl_model_map import (
    MATERIAL_MODEL_MAP as MAPDL_MAP,
)
from ansys.materials.manager.integrations.mapdl.mapdl_writer import MapdlWriter
from ansys.materials.manager.integrations.matml._matml_model_map import (
    MATERIAL_MODEL_MAP as MATML_MAP,
)
from ansys.materials.manager.integrations.matml.matml_writer import MatmlWriter
from ansys.materials.manager.models import Material


@pytest.mark.parametrize(
    "writer_cls,model_map",
    [
        (MatmlWriter, MATML_MAP),
        (MapdlWriter, MAPDL_MAP),
        (FluentWriter, FLUENT_MAP),
        (LsDynaWriter, LSDYNA_MAP),
    ],
)
def test_mapped_models_accept_without_error(writer_cls, model_map, minimal_model_factory):
    """Each mapped model type should traverse via accept without raising."""
    for model_cls in model_map:
        model = minimal_model_factory(model_cls)
        if model is None:
            pytest.skip(f"No minimal fixture for {model_cls.__name__} yet")

        material = Material(name="test", material_id=1, models=[model])
        writer = writer_cls([material])
        assert material.name in writer._material_repr


@pytest.mark.parametrize(
    "model_map",
    [MATML_MAP, MAPDL_MAP, FLUENT_MAP, LSDYNA_MAP],
)
def test_model_info_label_attribute_alignment(model_map):
    """ModelInfo entries should have aligned labels and attributes when both are set."""
    for model_cls, info in model_map.items():
        if info.method_write or info.method_read:
            continue
        if not info.labels or not info.attributes:
            continue
        flat_labels = info.labels
        if flat_labels and isinstance(flat_labels[0], list):
            flat_labels = [label for group in flat_labels for label in group]
        assert len(flat_labels) == len(info.attributes), model_cls.__name__
        for attribute in info.attributes:
            assert hasattr(model_cls, "model_fields") or hasattr(model_cls, attribute)
