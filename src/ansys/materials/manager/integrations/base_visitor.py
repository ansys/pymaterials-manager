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

import functools
from typing import Any
import warnings

from ..models import Material, MaterialModel
from ._common import ModelInfo
from .material_model_writer_visitor import (
    MaterialModelWriterVisitor,
    UnsupportedMaterialModelError,
)


def _visit_registry(visitor_cls: type) -> dict | None:
    """Return the singledispatch registry for a writer's ``visit`` method, if any."""
    visit = visitor_cls.__dict__.get("visit")
    if visit is None:
        return None
    if isinstance(visit, functools.singledispatchmethod):
        return visit.dispatcher.registry
    return None


class BaseVisitor(MaterialModelWriterVisitor):
    """Base class for format-specific material writers.

    Writers subclass this class and implement serialization by defining a
    ``@functools.singledispatchmethod`` named ``visit`` on the writer subclass,
    then registering handlers with ``@visit.register(MyModel)``. A default
    handler for :class:`~ansys.materials.manager.models.MaterialModel` that reads
    ``_model_map`` is enough for most models.

    Construction stores materials and initializes ``_material_repr``, a
    ``dict[str, list]`` that accumulates per-material output fragments.
    Call :meth:`visit_materials` (or rely on the subclass ``__init__``) to
    traverse via :meth:`~ansys.materials.manager.models.Material.accept`.

    Parameters
    ----------
    materials : list[Material]
        Materials to serialize.
    model_map : dict[type, ModelInfo] | None
        Maps concrete model classes to :class:`~.ModelInfo` descriptors.
        Declares which models the writer supports and how fields map to
        external labels.

    Examples
    --------
    Register a custom handler on a writer subclass::

        class MyMapdlWriter(BaseVisitor):
            @singledispatchmethod
            def visit(self, model: MaterialModel, *, material_name: str) -> None:
                raise UnsupportedMaterialModelError(...)

            @visit.register(Density)
            def _visit_density(self, model: Density, *, material_name: str) -> None:
                ...

    See Also
    --------
    MaterialModelWriterVisitor : Visitor protocol and traversal contract.
    MaterialModel.accept : Model-side dispatch entry point.
    ref_developer_guide : Contributor guide for adding models and solver maps.
    """

    def __init__(
        self,
        materials: list[Material],
        model_map: dict[type, ModelInfo] | None = None,
    ):
        """Initialize the base visitor."""
        self._materials: list[Material] = materials
        self._material_repr: dict = {material.name: [] for material in materials}
        self._model_map: dict[type, ModelInfo] = model_map if model_map is not None else {}

    def get_material_id(self, material_name) -> int:
        """
        Get the material id given the material name.

        Parameters
        ----------
        material_name : str
            Name of the material.

        Returns
        -------
        int
            Material id.
        """
        return [material.mat_id for material in self._materials if material.name == material_name][
            0
        ]

    def is_supported(self, material_model: MaterialModel) -> bool:
        """
        Check if the material model is supported.

        A model is supported when it appears in ``_model_map`` **and** the
        writer defines a ``visit`` handler for its concrete type (via
        ``@singledispatchmethod`` or a plain override).

        Parameters
        ----------
        material_model : MaterialModel
            Material model to check.

        Returns
        -------
        bool
            True if the material model is supported, False otherwise.
        """
        model_cls = material_model.__class__
        if model_cls not in self._model_map:
            return False
        return self._has_visit_handler(model_cls)

    def _has_visit_handler(self, model_cls: type) -> bool:
        """Return whether ``visit`` can dispatch for ``model_cls``."""
        registry = _visit_registry(type(self))
        if registry is not None:
            registered = {cls for cls in registry if cls is not object}
            return any(cls in registered for cls in model_cls.__mro__)
        if "visit" in type(self).__dict__:
            visit_attr = type(self).__dict__["visit"]
            if not isinstance(visit_attr, functools.singledispatchmethod):
                return visit_attr is not BaseVisitor.__dict__["visit"]
        return False

    def _populate_dependent_parameters(self, material_model: MaterialModel) -> dict:
        """Populate dependent parameters with quantity-like values."""
        if material_model.__class__ in self._model_map:
            mapping = self._model_map[material_model.__class__]
            if mapping.method_write:
                labels, quantities = mapping.method_write(material_model)
            else:
                if not mapping.labels or not mapping.attributes:
                    return {}
                labels = mapping.labels
                quantities = [getattr(material_model, label) for label in mapping.attributes]
            return {label: qty for label, qty in zip(labels, quantities) if qty is not None}
        return {}

    def visit(self, model: MaterialModel, *, material_name: str) -> Any:
        """Dispatch serialization for a material model.

        Concrete writers override this method (typically with
        ``@functools.singledispatchmethod``) to provide format-specific handlers.
        """
        raise UnsupportedMaterialModelError(
            f"{type(self).__name__} has no visit handler for {model.__class__.__name__}"
        )

    def visit_materials(self) -> None:
        """Visit all materials using double dispatch via :meth:`~.Material.accept`."""
        for material in self._materials:
            material.accept(self)

    def visit_material_model(self, material_name: str, material_model: MaterialModel) -> Any:
        """Visit a single material model.

        .. deprecated::
            Use :meth:`visit` via :meth:`~.MaterialModel.accept` instead.

        Parameters
        ----------
        material_name : str
            Name of the parent material.
        material_model : MaterialModel
            Model to visit.

        Returns
        -------
        Any
            Result from :meth:`visit`.
        """
        warnings.warn(
            "visit_material_model is deprecated; traversal uses MaterialModel.accept and visit.",
            DeprecationWarning,
            stacklevel=2,
        )
        return material_model.accept(self, material_name=material_name)
