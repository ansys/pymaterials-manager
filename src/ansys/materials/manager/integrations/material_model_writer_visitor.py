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

"""Writer visitor protocol for serializing material models.

Material models are solver-agnostic domain objects. Writers (MatML, MAPDL,
Fluent, LS-DYNA) are *visitors*: they traverse a ``Material`` and produce
format-specific output.

Traversal uses double dispatch::

    material.accept(writer)            # ``Material`` iterates its models
    model.accept(writer, material_name=...)     # delegates to ``writer.visit(model)``
    writer.visit(model, material_name=...)      # dispatches by concrete model type

Most model types need only a ``ModelInfo`` entry in the writer's
``_model_map``. Override ``visit`` with ``@visit.register(MyModel)`` when
serialization logic cannot be expressed as a label/attribute map.

Each concrete writer defines its own ``@singledispatchmethod visit`` so
handler registries are not shared across writer classes.

See Also
--------
MaterialModel.accept : Entry point on the model side.
BaseVisitor : Shared writer infrastructure.
ModelInfo : Declarative field-to-label mapping.
"""

from abc import ABC, abstractmethod
import logging
from typing import Any

from ..models import Material, MaterialModel

_logger = logging.getLogger(__name__)


class UnsupportedMaterialModelError(TypeError):
    """Raised when a writer has no handler for a material model type."""


class MaterialModelWriterVisitor(ABC):
    """Protocol for writers that serialize :class:`~.MaterialModel` instances.

    Subclasses implement format-specific output by defining a
    ``@functools.singledispatchmethod`` named ``visit`` and registering
    handlers (``@visit.register(MyModel)``), or by overriding ``visit``
    directly for a single code path.
    """

    @abstractmethod
    def visit(self, model: MaterialModel, *, material_name: str) -> Any:
        """Dispatch serialization for a single material model.

        Parameters
        ----------
        model : MaterialModel
            The model instance to serialize.
        material_name : str
            Name of the parent :class:`~.Material`, used to group output.

        Raises
        ------
        UnsupportedMaterialModelError
            If no handler is registered for the model's concrete type.
        """

    def visit_material(self, material: Material) -> None:
        """Visit every supported model on a material.

        Parameters
        ----------
        material : Material
            Material whose models should be serialized.
        """
        for material_model in material.models:
            if not self.is_supported(material_model):
                _logger.warning(
                    "Material model %s not supported by %s",
                    material_model.__class__.__name__,
                    self.__class__.__name__,
                )
                continue
            material_model.accept(self, material_name=material.name)

    @abstractmethod
    def is_supported(self, material_model: MaterialModel) -> bool:
        """Return whether this writer supports the given model type."""
