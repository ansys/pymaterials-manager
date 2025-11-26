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

from pathlib import Path

from ansys.units import Quantity

from ansys.materials.manager._models._common.independent_parameter import IndependentParameter
from ansys.materials.manager._models._common.model_qualifier import ModelQualifier
from ansys.materials.manager._models._material_models import IsotropicHardening
from ansys.materials.manager._models.material import Material
from ansys.materials.manager.parsers.mapdl.mapdl_writer import MapdlWriter

DIR_PATH = Path(__file__).resolve().parent
ISOTROPIC_HARDENING_MULTILINEAR_CONSTANT = DIR_PATH.joinpath(
    "..", "data", "mapdl_isotropic_hardening_multilinear_constant.cdb"
)
ISOTROPIC_HARDENING_MULTILINEAR_VARIABLE = DIR_PATH.joinpath(
    "..", "data", "mapdl_isotropic_hardening_multilinear_variable.cdb"
)
ISOTROPIC_HARDENING_BILINEAR_CONSTANT = DIR_PATH.joinpath(
    "..", "data", "mapdl_isotropic_hardening_bilinear_constant.cdb"
)
ISOTROPIC_HARDENING_BILINEAR_VARIABLE = DIR_PATH.joinpath(
    "..", "data", "mapdl_isotropic_hardening_bilinear_variable_temp.cdb"
)


def test_isotropic_hardening_multilinear_constant():
    isotropic_hardening = IsotropicHardening(
        stress=Quantity(
            value=[
                29.52801806,
                30.93946596,
                31.56895322,
                32.83324607,
                34.28804632,
                35.45779394,
                36.7206105,
                37.86550163,
                38.9800331,
                40.37409873,
                41.70507301,
                42.87224516,
                43.84021506,
                44.94150614,
                45.83281545,
                46.81708774,
                47.66814815,
                48.32197593,
                49.03683773,
                49.69403185,
                50.38934957,
                50.9180887,
                51.42733217,
                52.07041013,
                52.53035234,
                52.99417352,
                53.42471716,
                54.00033621,
                54.36001955,
                54.71963936,
                55.13624926,
            ],
            units="Pa",
        ),
        independent_parameters=[
            IndependentParameter(
                name="Plastic Strain",
                values=Quantity(
                    value=[
                        0.0,
                        0.000175189,
                        0.000257223,
                        0.00043005,
                        0.000643825,
                        0.000828966,
                        0.00104416,
                        0.001255108,
                        0.001477263,
                        0.00178269,
                        0.002108789,
                        0.002428809,
                        0.002723618,
                        0.003098638,
                        0.003439709,
                        0.003864545,
                        0.004281943,
                        0.004640923,
                        0.00507901,
                        0.005531357,
                        0.006070993,
                        0.006529747,
                        0.007015966,
                        0.007698042,
                        0.008235242,
                        0.008819543,
                        0.009399517,
                        0.010228087,
                        0.010773853,
                        0.011338467,
                        0.01201311,
                    ],
                    units="m m^-1",
                ),
            ),
        ],
    )

    material = Material(
        name="Material 2",
        material_id=2,
        models=[isotropic_hardening],
    )

    mapdl_writer = MapdlWriter(materials=[material])
    material_strings = mapdl_writer.write()
    material = Material(
        name="Material 2",
        material_id=2,
        models=[isotropic_hardening],
    )

    mapdl_writer = MapdlWriter(materials=[material])
    material_strings = mapdl_writer.write()
    with open(ISOTROPIC_HARDENING_MULTILINEAR_CONSTANT, "r") as file:
        data = file.read()
    assert data == material_strings[0]
    assert data == material_strings[0]


def test_isotropic_hardening_multilinear_variable():
    isotropic_hardening = IsotropicHardening(
        stress=Quantity(
            value=[
                16704754.8966912,
                21518003.4164155,
                25601270.737195,
                29108916.0548528,
                32154643.8146231,
                34824061.3012457,
                37182852.4430888,
                39282255.0771635,
                41162825.437843,
                42857083.7783819,
                44391410.7835827,
                45787431.1456248,
                47063039.1229118,
                48233169.6948518,
                49310386.0159359,
                50305332.2732179,
                51227086.6021781,
                52083438.8803321,
                52881111.4151668,
                53625935.7683767,
                54322995.5616163,
                54976742.6620037,
                55591092.3622225,
                56169501.8561676,
                56715035.3332417,
                57230418.279761,
                57718083.0190841,
                58180207.0964667,
                58618745.7867817,
                59035459.7488112,
                59431938.6509741,
                59809621.4369362,
                60169813.7757258,
                60513703.1423761,
                60842371.8961503,
                61156808.6598297,
                61457918.2520941,
                61746530.3831801,
                62023407.2898208,
                62289250.4574115,
                62544706.5542272,
                62790372.6833805,
                63026801.0423114,
                63254503.0663465,
                63473953.1217677,
                63685591.8045138,
                63889828.8927885,
                64087045.9952085,
                64277598.9305012,
                64461819.869974,
                64640019.2698924,
                66146656.1763758,
                67282142.2993307,
                68168583.6867895,
                68879817.0796186,
                69463116.2114581,
                69950151.2914524,
                70362936.044052,
                70717247.4511567,
                71024688.3399282,
                71293982.1976332,
                16000000,
                21518003.4164155,
                25601270.737195,
                29108916.0548528,
                32154643.8146231,
                34824061.3012457,
                37182852.4430888,
                39282255.0771635,
                41162825.437843,
                42857083.7783819,
                44391410.7835827,
                45787431.1456248,
                47063039.1229118,
                48233169.6948518,
                49310386.0159359,
                50305332.2732179,
                51227086.6021781,
                52083438.8803321,
                52881111.4151668,
                53625935.7683767,
                54322995.5616163,
                54976742.6620037,
                55591092.3622225,
                56169501.8561676,
                56715035.3332417,
                57230418.279761,
                57718083.0190841,
                58180207.0964667,
                58618745.7867817,
                59035459.7488112,
                59431938.6509741,
                59809621.4369362,
                60169813.7757258,
                60513703.1423761,
                60842371.8961503,
                61156808.6598297,
                61457918.2520941,
                61746530.3831801,
                62023407.2898208,
                62289250.4574115,
                62544706.5542272,
                62790372.6833805,
                63026801.0423114,
                63254503.0663465,
                63473953.1217677,
                63685591.8045138,
                63889828.8927885,
                64087045.9952085,
                64277598.9305012,
                64461819.869974,
                64640019.2698924,
                66146656.1763758,
                67282142.2993307,
                68168583.6867895,
                68879817.0796186,
                69463116.2114581,
                69950151.2914524,
                70362936.044052,
                70717247.4511567,
                71024688.3399282,
                71293982.1976332,
            ],
            units="Pa",
        ),
        independent_parameters=[
            IndependentParameter(
                name="Plastic Strain",
                values=Quantity(
                    value=[
                        0,
                        0.000189791542302976,
                        0.000379583084605952,
                        0.000569374626908928,
                        0.000759166169211904,
                        0.00094895771151488,
                        0.00113874925381786,
                        0.00132854079612083,
                        0.00151833233842381,
                        0.00170812388072678,
                        0.00189791542302976,
                        0.00208770696533274,
                        0.00227749850763571,
                        0.00246729004993869,
                        0.00265708159224166,
                        0.00284687313454464,
                        0.00303666467684761,
                        0.00322645621915059,
                        0.00341624776145357,
                        0.00360603930375654,
                        0.00379583084605952,
                        0.00398562238836249,
                        0.00417541393066547,
                        0.00436520547296845,
                        0.00455499701527142,
                        0.0047447885575744,
                        0.00493458009987737,
                        0.00512437164218035,
                        0.00531416318448333,
                        0.0055039547267863,
                        0.00569374626908928,
                        0.00588353781139225,
                        0.00607332935369523,
                        0.00626312089599821,
                        0.00645291243830118,
                        0.00664270398060416,
                        0.00683249552290713,
                        0.00702228706521011,
                        0.00721207860751309,
                        0.00740187014981606,
                        0.00759166169211904,
                        0.00778145323442201,
                        0.00797124477672499,
                        0.00816103631902796,
                        0.00835082786133094,
                        0.00854061940363392,
                        0.00873041094593689,
                        0.00892020248823987,
                        0.00910999403054284,
                        0.00929978557284582,
                        0.0094895771151488,
                        0.0113874925381786,
                        0.0132854079612083,
                        0.0151833233842381,
                        0.0170812388072678,
                        0.0189791542302976,
                        0.0208770696533273,
                        0.0227749850763571,
                        0.0246729004993869,
                        0.0265708159224166,
                        0.0284687313454464,
                        0,
                        0.000189791542302976,
                        0.000379583084605952,
                        0.000569374626908928,
                        0.000759166169211904,
                        0.00094895771151488,
                        0.00113874925381786,
                        0.00132854079612083,
                        0.00151833233842381,
                        0.00170812388072678,
                        0.00189791542302976,
                        0.00208770696533274,
                        0.00227749850763571,
                        0.00246729004993869,
                        0.00265708159224166,
                        0.00284687313454464,
                        0.00303666467684761,
                        0.00322645621915059,
                        0.00341624776145357,
                        0.00360603930375654,
                        0.00379583084605952,
                        0.00398562238836249,
                        0.00417541393066547,
                        0.00436520547296845,
                        0.00455499701527142,
                        0.0047447885575744,
                        0.00493458009987737,
                        0.00512437164218035,
                        0.00531416318448333,
                        0.0055039547267863,
                        0.00569374626908928,
                        0.00588353781139225,
                        0.00607332935369523,
                        0.00626312089599821,
                        0.00645291243830118,
                        0.00664270398060416,
                        0.00683249552290713,
                        0.00702228706521011,
                        0.00721207860751309,
                        0.00740187014981606,
                        0.00759166169211904,
                        0.00778145323442201,
                        0.00797124477672499,
                        0.00816103631902796,
                        0.00835082786133094,
                        0.00854061940363392,
                        0.00873041094593689,
                        0.00892020248823987,
                        0.00910999403054284,
                        0.00929978557284582,
                        0.0094895771151488,
                        0.0113874925381786,
                        0.0132854079612083,
                        0.0151833233842381,
                        0.0170812388072678,
                        0.0189791542302976,
                        0.0208770696533273,
                        0.0227749850763571,
                        0.0246729004993869,
                        0.0265708159224166,
                        0.0284687313454464,
                    ],
                    units="m m^-1",
                ),
            ),
            IndependentParameter(
                name="Temperature",
                values=Quantity(
                    value=[
                        22,
                        22,
                        22,
                        22,
                        22,
                        22,
                        22,
                        22,
                        22,
                        22,
                        22,
                        22,
                        22,
                        22,
                        22,
                        22,
                        22,
                        22,
                        22,
                        22,
                        22,
                        22,
                        22,
                        22,
                        22,
                        22,
                        22,
                        22,
                        22,
                        22,
                        22,
                        22,
                        22,
                        22,
                        22,
                        22,
                        22,
                        22,
                        22,
                        22,
                        22,
                        22,
                        22,
                        22,
                        22,
                        22,
                        22,
                        22,
                        22,
                        22,
                        22,
                        22,
                        22,
                        22,
                        22,
                        22,
                        22,
                        22,
                        22,
                        22,
                        22,
                        52,
                        52,
                        52,
                        52,
                        52,
                        52,
                        52,
                        52,
                        52,
                        52,
                        52,
                        52,
                        52,
                        52,
                        52,
                        52,
                        52,
                        52,
                        52,
                        52,
                        52,
                        52,
                        52,
                        52,
                        52,
                        52,
                        52,
                        52,
                        52,
                        52,
                        52,
                        52,
                        52,
                        52,
                        52,
                        52,
                        52,
                        52,
                        52,
                        52,
                        52,
                        52,
                        52,
                        52,
                        52,
                        52,
                        52,
                        52,
                        52,
                        52,
                        52,
                        52,
                        52,
                        52,
                        52,
                        52,
                        52,
                        52,
                        52,
                        52,
                        52,
                    ],
                    unit="C",
                ),
            ),
        ],
    )

    material = Material(
        name="Material 2",
        material_id=2,
        models=[isotropic_hardening],
    )

    mapdl_writer = MapdlWriter(materials=[material])
    material_strings = mapdl_writer.write()

    material = Material(
        name="Material 2",
        material_id=2,
        models=[isotropic_hardening],
    )

    mapdl_writer = MapdlWriter(materials=[material])
    material_strings = mapdl_writer.write()

    with open(ISOTROPIC_HARDENING_MULTILINEAR_VARIABLE, "r") as file:
        data = file.read()
        assert data == material_strings[0]


def test_isotropic_hardening_bilinear_constant():
    isotropic_hardening = IsotropicHardening(
        model_qualifiers=[ModelQualifier(name="Definition", value="Bilinear")],
        yield_strength=Quantity(value=[225000000], units="Pa"),
        tangent_modulus=Quantity(value=[2091000000], units="Pa"),
    )

    material = Material(
        name="Material 5",
        material_id=5,
        models=[isotropic_hardening],
    )

    mapdl_writer = MapdlWriter(materials=[material])
    material_strings = mapdl_writer.write()

    with open(ISOTROPIC_HARDENING_BILINEAR_CONSTANT, "r") as file:
        data = file.read()
        assert data == material_strings[0]


def test_isotropic_hardening_bilinear_variable():
    isotropic_hardening = IsotropicHardening(
        model_qualifiers=[ModelQualifier(name="Definition", value="Bilinear")],
        yield_strength=Quantity(
            value=[225000000, 168000000, 115000000, 31000000, 15000000], units="Pa"
        ),
        tangent_modulus=Quantity(
            value=[2091000000, 1577000000, 708000000, 405000000, 265000000], units="Pa"
        ),
        independent_parameters=[
            IndependentParameter(
                name="Temperature",
                values=Quantity(value=[100, 300, 816, 1040, 1150], units="C"),
            )
        ],
    )

    material = Material(
        name="Material 6",
        material_id=6,
        models=[isotropic_hardening],
    )

    mapdl_writer = MapdlWriter(materials=[material])
    material_strings = mapdl_writer.write()
    with open(ISOTROPIC_HARDENING_BILINEAR_VARIABLE, "r") as file:
        data = file.read()
        assert data == material_strings[0]
