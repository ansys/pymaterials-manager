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

"""External system integrations for reading and writing materials.

Domain models live in :mod:`ansys.materials.manager.models`. Writers in this
package traverse those models using the `visitor pattern
<https://en.wikipedia.org/wiki/Visitor_pattern>`_: each
:class:`~.MaterialModel` calls :meth:`~ansys.materials.manager.models.MaterialModel.accept`
on a writer, which dispatches to :meth:`~.MaterialModelWriterVisitor.visit`.

For extension or custom writers, subclass :class:`~.BaseVisitor`, define a
``@functools.singledispatchmethod visit`` on the subclass, and register handlers
with ``@visit.register(MyModel)``. Most models only need a
:class:`~._common.ModelInfo` entry in the writer's ``_model_map``. See
``doc/source/developer_guide.rst`` for a full contributor guide.

Readers (MatML, REST) deserialize external data into models via ``ModelInfo``
maps and do not use ``accept()``.
"""

from .base_visitor import BaseVisitor
from .fluent import FluentWriter
from .lsdyna import LsDynaWriter
from .mapdl import MapdlWriter, read_mapdl
from .material_model_writer_visitor import MaterialModelWriterVisitor, UnsupportedMaterialModelError
from .matml import MatmlReader, MatmlWriter

__all__ = [
    "BaseVisitor",
    "FluentWriter",
    "LsDynaWriter",
    "MapdlWriter",
    "MaterialModelWriterVisitor",
    "MatmlReader",
    "MatmlWriter",
    "UnsupportedMaterialModelError",
    "read_mapdl",
]

try:
    from .rest import RestMaterialReader, RestSessionClient
except ImportError:
    pass  # optional grantami extra
else:
    __all__ += ["RestMaterialReader", "RestSessionClient"]
