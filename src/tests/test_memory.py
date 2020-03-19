from ..memory import IFR1200Memory

def test_is_valid_fequency():
    assert IFR1200Memory.is_valid_fequency("10.0") == True
    assert IFR1200Memory.is_valid_fequency("100.0") == True
    assert IFR1200Memory.is_valid_fequency("999.9999") == True
    assert IFR1200Memory.is_valid_fequency("2400.000") == False
    assert IFR1200Memory.is_valid_fequency(300.0) == True

def test_is_valid_memory_location():
    assert IFR1200Memory.is_valid_memory_location(-1) == False
    assert IFR1200Memory.is_valid_memory_location(0) == True
    assert IFR1200Memory.is_valid_memory_location(15) == True
    assert IFR1200Memory.is_valid_memory_location(16) == False





