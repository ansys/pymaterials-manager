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

PREDIFINED_TB_FIELDS = {
    "Temperature": "Temperature = 'TEMP' ! Temperature\n",
}
PREDIFINED_TB_FIELDS = {
    "Temperature": "TEMP",
}

INTERPOLATION_ALGORITHM_MAP = {"Linear Multivariate": "LMUL", "Linear Multivariate (Qhull)": "LMUL"}

EXTRAPOLATION_TYPE_MAP = {
    "Projection to the Convex Hull": "PHULL",
    "Projection to the Bounding Box": "BBOX",
}

USER_DEFINED_TB_FIELDS = """{name} = 'UF{idx:02d}' ! {unit}
"""

CONSTANT_MP_PROPERTY = """MP,{lab},{matid},{c0},{c1},{c2},{c3},{c4} ! {unit}
"""

TEMPERATURE_REFERENCE = """MP,REFT,{matid},{temp},
"""

MP_DATA = """MPDATA,{lab},{matid},{sloc},{c1},{c2},{c3},{c4},{c5},{c6} ! {unit}
"""

MP_TEMP = """MPTEMP,{sloc},{t1},{t2},{t3},{t4},{t5},{t6}
"""

TB = """TB,{lab},{matid},,,{tbopt}
"""

TB_FIELD = """TBFIELD,{type},{value}, ! {unit}
"""

TB_DATA = """TBDATA,{stloc},{c1},{c2},{c3},{c4},{c5},{c6}
"""

TB_TEMP = """TBTEMP,{temp}
"""

TBPT = """TBPT,{oper},{x},{y}
"""

TBIN_SCALE = """TBIN,SCALE,{par1},{par2},{par3},{par4}
"""

TBIN_ALGO = """TBIN,ALGO,{par1}
"""

TBIN_DEFA = """TBIN,DEFA,{par1},{par2}
"""

TBIN_BNDS = """TBIN,BNDS,{par1},{par2},{par3}
"""

TBIN_NORM = """TBIN,NORM,{par1},{par2}
"""

TBIN_CACH = """TBIN,CACH,{par1},{par2}\n"""  # codespell:ignore CACH

TBIN_EXTR = """TBIN,EXTR,{par1},{par2}
"""
