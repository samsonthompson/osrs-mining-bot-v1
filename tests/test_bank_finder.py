import pytest
from Utilities.find_nearest_bank import BankFinder, BankLocation

@pytest.fixture
def bank_finder():
    return BankFinder()

def test_distance_calculation(bank_finder):
    # Test with known coordinates
    # New York City coordinates
    nyc_lat, nyc_lon = 40.7128, -74.0060
    # Boston coordinates
    boston_lat, boston_lon = 42.3601, -71.0589
    
    distance = bank_finder.calculate_distance(nyc_lat, nyc_lon, boston_lat, boston_lon)
    # The distance should be approximately 306 km
    assert 300 < distance < 310

def test_find_nearest_banks(bank_finder):
    # Test with sample coordinates (London)
    banks = bank_finder.find_nearest_banks(51.5074, -0.1278)
    
    # Should return a list of BankLocation objects
    assert isinstance(banks, list)
    if banks:  # If any banks found
        assert isinstance(banks[0], BankLocation)
        # First bank should be closest
        if len(banks) > 1:
            assert banks[0].distance <= banks[1].distance

def test_get_directions(bank_finder):
    # Test getting directions between two points
    directions = bank_finder.get_directions(
        51.5074, -0.1278,  # London
        51.5072, -0.1276   # Nearby point
    )
    
    assert isinstance(directions, dict)
    if directions:
        assert 'distance' in directions
        assert 'duration' in directions 