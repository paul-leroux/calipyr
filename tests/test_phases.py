from calipyr.phases.relationships import void_ratio_from_porosity

def test_void_ratio():
    assert abs(void_ratio_from_porosity(0.4) - 0.6667) < 1e-3