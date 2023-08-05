from ..moc import MOC, World2ScreenMPL

from astropy import units as u
from astropy.coordinates import SkyCoord

import numpy as np

def test_create_from_polygon():
    lon = [83.71315909, 83.71378887, 83.71297292, 83.71233919] * u.deg
    lat = [-5.44217436,-5.44298864, -5.44361751, -5.4428033] * u.deg

    moc = MOC.from_polygon(lon=lon, lat=lat, max_depth=20)

    truth_ipix_d = {'17': [89921647231],
        '18': [359686588915,
                359686588918,
                359686588919,
                359686588921,
                359686588923,
                359686589268,
                359686589269,
                359686589608,
                359686589610,
                359686589952],
        '19': [1438746355657,
                1438746355659,
                1438746357060,
                1438746357061,
                1438746357063,
                1438746358408,
                1438746358410,
                1438746359814],
        '20': [5754985422603,
                5754985422606,
                5754985422607,
                5754985422618,
                5754985422619,
                5754985422622,
                5754985422623,
                5754985422625,
                5754985422627,
                5754985422633,
                5754985422635,
                5754985422664,
                5754985422665,
                5754985422666,
                5754985422667,
                5754985422668,
                5754985422669,
                5754985422670,
                5754985422671,
                5754985422680,
                5754985422681,
                5754985422682,
                5754985422683,
                5754985422684,
                5754985422685,
                5754985422686,
                5754985422687,
                5754985422721,
                5754985422724,
                5754985422725,
                5754985422726,
                5754985422727,
                5754985422732,
                5754985422733,
                5754985422734,
                5754985422735,
                5754985422756,
                5754985422757,
                5754985422758,
                5754985422759,
                5754985422765,
                5754985422767,
                5754985428229,
                5754985428231,
                5754985428237,
                5754985428248,
                5754985428249,
                5754985428250,
                5754985428251,
                5754985428272,
                5754985428273,
                5754985428274,
                5754985428275,
                5754985428276,
                5754985428277,
                5754985428278,
                5754985428279,
                5754985428320,
                5754985428321,
                5754985428322,
                5754985428323,
                5754985428324,
                5754985428325,
                5754985428326,
                5754985428327,
                5754985428336,
                5754985428337,
                5754985428338,
                5754985428339,
                5754985428340,
                5754985428341,
                5754985428342,
                5754985428343,
                5754985433608,
                5754985433609,
                5754985433610,
                5754985433611,
                5754985433612,
                5754985433613,
                5754985433614,
                5754985433615,
                5754985433636,
                5754985433637,
                5754985433638,
                5754985433639,
                5754985433644,
                5754985433645,
                5754985433646,
                5754985433647,
                5754985433656,
                5754985433658,
                5754985433744,
                5754985433746,
                5754985433752,
                5754985433754,
                5754985433755,
                5754985433776,
                5754985433777,
                5754985433778,
                5754985433779,
                5754985433784,
                5754985433785,
                5754985433786,
                5754985433787,
                5754985439248,
                5754985439249,
                5754985439250,
                5754985439251,
                5754985439252,
                5754985439254,
                5754985439260,
                5754985439262,
                5754985439264,
                5754985439265,
                5754985439266,
                5754985439267,
                5754985439268,
                5754985439269,
                5754985439270,
                5754985439271,
                5754985439280,
                5754985439281,
                5754985439282,
                5754985439283,
                5754985439284]}

    moc_truth = MOC.from_json(truth_ipix_d)
    assert(moc == moc_truth)

def test_polygon2_issue_44():
    from astropy import units as u
    from mocpy import MOC
    import numpy as np

    ra = [174.75937396073138, 185.24062603926856, 184.63292896369916, 175.3670710363009]
    dec = [-49.16744206799886, -49.16744206799887, -42.32049830486584, -42.32049830486584]

    moc = MOC.from_polygon(ra * u.deg, dec * u.deg)

    assert not moc.empty()

# Test from https://github.com/cds-astro/mocpy/issues/50
def test_polygon_issue_50():
    from mocpy import MOC
    from astropy.coordinates import SkyCoord
    from astropy import units as u
    coords = SkyCoord([(353.8156714, -56.33202193), (6.1843286, -56.33202193), (5.27558041, -49.49378172), (354.72441959, -49.49378172)], unit=u.deg)
    moc = MOC.from_polygon_skycoord(coords)
    assert not moc.empty()
