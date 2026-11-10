.. _ref_developer_guide:

===============
Developer guide
===============

This page describes how material **writers** serialize domain models using the
`visitor pattern <https://en.wikipedia.org/wiki/Visitor_pattern>`_, and how to
extend the library with new models or solver integrations.

End users typically interact with :class:`~ansys.materials.manager.MaterialManager`
and do not need to know about visitors. Contributors and anyone subclassing
writers should read this guide.


Writer visitor pattern
======================

Problem
-------

Material models (for example :class:`~ansys.materials.manager.models.Density`,
:class:`~ansys.materials.manager.models.ElasticityIsotropic`) are
solver-agnostic Pydantic objects in :mod:`ansys.materials.manager.models`.
Writers in :mod:`ansys.materials.manager.integrations` must turn those objects
into MatML XML, MAPDL command strings, Fluent dictionaries, or LS-DYNA keyword
cards **without** importing solver logic into the model layer.

Double dispatch
---------------

Traversal uses **double dispatch**. The model does not know which solver is
targeted; the writer does not use long ``isinstance`` chains to pick behavior.

1. A writer is constructed with a list of :class:`~ansys.materials.manager.models.Material`
   instances.
2. The writer calls :meth:`~ansys.materials.manager.models.Material.accept`.
3. Each :class:`~ansys.materials.manager.models.MaterialModel` on that material
   calls :meth:`~ansys.materials.manager.models.MaterialModel.accept`, which
   delegates to ``visitor.visit(self, material_name=...)``.
4. The writer's ``visit`` implementation (usually
   ``@functools.singledispatchmethod``) selects the handler for the concrete
   model type.
5. Output fragments accumulate in ``writer._material_repr[material_name]`` until
   ``write()`` serializes them.

.. code-block:: text

   MaterialManager.write_to_mapdl(...)
        └── MapdlWriter(materials)
                 └── material.accept(writer)
                          └── model.accept(writer, material_name=...)
                                   └── writer.visit(model, material_name=...)
                                            └── @visit.register handler

Key types
---------

.. list-table::
   :header-rows: 1

   * - Type
     - Location
     - Role
   * - :class:`~ansys.materials.manager.integrations.MaterialModelWriterVisitor`
     - ``integrations``
     - Abstract visitor (``visit``, ``visit_material``, ``is_supported``)
   * - :class:`~ansys.materials.manager.models._common.visitor_protocol.MaterialModelWriterVisitorProtocol`
     - ``models._common.visitor_protocol``
     - Structural typing protocol used by ``accept()`` (no integrations import)
   * - :class:`~ansys.materials.manager.integrations.BaseVisitor`
     - ``integrations``
     - Shared writer base: ``_model_map``, ``_populate_dependent_parameters``, traversal
   * - :class:`~ansys.materials.manager.integrations._common.ModelInfo`
     - ``integrations._common``
     - Declarative map from model fields to external labels (or ``method_write``)
   * - Concrete writers
     - ``integrations.matml``, ``mapdl``, ``fluent``, ``lsdyna``
     - Format-specific ``visit`` handlers and ``write()``

Import boundary
---------------

- ``integrations`` imports ``models``.
- ``models`` **never** imports ``integrations``. ``Material.accept`` and
  ``MaterialModel.accept`` only reference
  :class:`~ansys.materials.manager.models._common.visitor_protocol.MaterialModelWriterVisitorProtocol`.

Each writer class defines its **own** ``@singledispatchmethod visit`` so handler
registries are not shared across MatML, MAPDL, Fluent, and LS-DYNA.


``ModelInfo`` maps vs custom ``visit`` handlers
================================================

Most models only need a row in the writer's ``_*_model_map.py`` file:

.. code-block:: python

   MyModel: ModelInfo(
       labels=["EXTERNAL_LABEL"],
       attributes=["python_field_name"],
   ),

The default ``visit`` handler calls
:meth:`~ansys.materials.manager.integrations.BaseVisitor._populate_dependent_parameters`,
which reads ``_model_map``.

When labels and fields do not map 1:1, use ``method_write``:

.. code-block:: python

   MyModel: ModelInfo(method_write=map_from_my_model),

Define ``map_from_my_model(model) -> (labels, quantities)`` in the same module
(see existing MAPDL mappers in ``integrations/mapdl/_mapdl_model_map.py``).

When the entire output format is bespoke (MAPDL TB tables, multi-line APDL),
register a typed handler on that writer's ``visit``:

.. code-block:: python

   class MapdlWriter(BaseVisitor):
       @singledispatchmethod
       def visit(self, model: MaterialModel, *, material_name: str) -> None:
           ...

       @visit.register(MyModel)
       def _visit_my_model(self, model: MyModel, *, material_name: str) -> None:
           output = self._write_my_model_special(model)
           self._material_repr[material_name].append(output)

Only a small number of MAPDL models need this; the rest use the shared
"standard constants / tables" path via the default ``MaterialModel`` handler.


Readers are not visitors
========================

MatML and REST **readers** build :class:`~ansys.materials.manager.models.MaterialModel`
instances from external data. They use the same :class:`~ansys.materials.manager.integrations._common.ModelInfo`
maps (with ``method_read`` where needed) but **do not** call ``accept()``.
Dispatch is keyed by XML property names or Granta MI model IDs, not by existing
model instances.


Adding a new material model
===========================

Use this checklist when introducing a new domain concept (a new
:class:`~ansys.materials.manager.models.MaterialModel` subclass).

1. **Define the model** in ``src/ansys/materials/manager/models/_material_models/``.

   - Subclass :class:`~ansys.materials.manager.models.MaterialModel`.
   - Set a frozen ``name: Literal["..."]``, fields, and ``supported_packages``.
   - Do **not** override ``accept()``; it is inherited from the base class.

2. **Export** the class from ``models/_material_models/__init__.py`` (and thus
   ``models.__all__``).

3. **MatML (canonical interchange)**: add an entry to
   ``integrations/matml/_matml_model_map.py``. One entry covers MatML read and write.

4. **REST / Granta MI** (if applicable): add ``MODEL_ID_MAP`` and
   ``MATERIAL_MODEL_MAP`` entries in ``integrations/rest/_rest_model_map.py``.

5. **Per-solver writer maps**: see :ref:`ref_add_solver_support` for each target
   (MAPDL, Fluent, LS-DYNA).

6. **Tests**: golden-file tests under ``tests/matml/``, ``tests/mapdl/``, etc.
   Add a ``minimal_model_factory`` entry in ``tests/integrations/conftest.py`` so
   map-coverage smoke tests pick up the new type (optional but recommended).


.. _ref_add_solver_support:

Adding solver support for an existing model
===========================================

For each solver, edit **one map file** unless the model needs custom MAPDL
serialization or LS-DYNA card composition.

.. list-table::
   :header-rows: 1

   * - Solver
     - Map file
     - Extra steps
   * - MatML
     - ``integrations/matml/_matml_model_map.py``
     - Usually already present if the model exists
   * - MAPDL
     - ``integrations/mapdl/_mapdl_model_map.py``
     - ``@visit.register`` only for non-standard output (see
       :class:`~ansys.materials.manager.integrations.mapdl.MapdlWriter`)
   * - Fluent
     - ``integrations/fluent/_fluent_model_map.py``
     - Map entry only
   * - LS-DYNA
     - ``integrations/lsdyna/_ls_dyna_model_map.py``
     - Update ``_get_material_card_map()`` in ``lsdyna_writer.py`` if the model
       participates in a keyword card

**Simple case** (example: density to MAPDL ``DENS``):

.. code-block:: python

   # integrations/mapdl/_mapdl_model_map.py
   MyModel: ModelInfo(labels=["DENS"], attributes=["density"]),

After adding the map entry, the writer's default ``visit`` handler serializes the
model. No changes to ``MapdlWriter`` are required.

**LS-DYNA card composition**: LS-DYNA merges multiple models into one keyword
card. Ensure each constituent model is in ``_ls_dyna_model_map.py``, then add or
update an entry in ``_get_material_card_map()`` keyed by the tuple of model
classes present on a :class:`~ansys.materials.manager.models.Material`.


``is_supported`` and unsupported models
=======================================

During normal traversal (:meth:`~ansys.materials.manager.integrations.MaterialModelWriterVisitor.visit_material`),
each model on a :class:`~ansys.materials.manager.models.Material` is checked with
:meth:`~ansys.materials.manager.integrations.BaseVisitor.is_supported`. A model is
supported only when **both** of the following hold:

1. Its class is listed in the writer's ``_model_map``.
2. The writer defines a ``visit`` handler that can dispatch to that class (via
   ``@singledispatchmethod`` or a plain override).

Unsupported models are **skipped** (not raised) and a **warning** is logged so
batch export can continue. Direct calls to :meth:`~ansys.materials.manager.models.MaterialModel.accept`
still dispatch through ``visit`` and may raise
:class:`~ansys.materials.manager.integrations.UnsupportedMaterialModelError` when
no handler exists.


Testing
=======

Use a **layered** approach:

1. **Visitor mechanics**: ``tests/integrations/test_visitor_dispatch.py`` (fast
   dispatch and ``accept`` wiring).
2. **Map coverage**: ``tests/integrations/test_writer_map_coverage.py``
   (parametrized smoke test per writer map).
3. **Format golden files**: existing tests under ``tests/matml/``, ``tests/mapdl/``,
   etc. (prove correct XML / APDL / Fluent / LS-DYNA output).

For a new simple map entry, layers 1-2 plus an optional golden file are usually
enough. Complex MAPDL or tabular output should always have a golden-file test.


Further reading
===============

- API reference: :class:`~ansys.materials.manager.integrations.MaterialModelWriterVisitor`,
  :class:`~ansys.materials.manager.models._common.visitor_protocol.MaterialModelWriterVisitorProtocol`,
  :class:`~ansys.materials.manager.integrations.BaseVisitor`, and concrete writers
  (generated from docstrings).
- Module overview: :mod:`ansys.materials.manager.integrations`.
