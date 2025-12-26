
import pandas as pd
from PJ9 import findCoordinates, findAddress



# ============================================
# UNIT TESTS
# ============================================

def test_address_UP():
    """Test findCoordinates with University of Portland address"""
    addresses = ["5000 N. Willamette blvd, Portland, OR 97203"]
    result = findCoordinates(addresses)

    assert len(result) == 1
    assert not pd.isna(result['lat'][0])
    assert not pd.isna(result['lng'][0])
    assert result['status_code'][0] == 200
    print("✓ test_address_UP PASSED")


def test_address_invalid():
    """Test findCoordinates with invalid address"""
    addresses = ["xyzinvalidaddress12345"]
    result = findCoordinates(addresses)

    assert len(result) == 1
    assert result['status_code'][0] is not None
    print("✓ test_address_invalid PASSED")


def test_mlb_parks():
    """Test findCoordinates with MLB stadium addresses"""
    addresses = ["Yankee Stadium, New York", "Fenway Park, Boston"]
    result = findCoordinates(addresses)

    assert len(result) == 2
    assert all(result['status_code'] == 200)
    print("✓ test_mlb_parks PASSED")


def test_state_capitols():
    """Test findCoordinates with US state capitol addresses"""
    addresses = ["Salem, Oregon", "Richmond, Virginia"]
    result = findCoordinates(addresses)

    assert len(result) == 2
    assert all(result['status_code'] == 200)
    print("✓ test_state_capitols PASSED")


def test_coordinates_UP():
    """Test findAddress with University of Portland coordinates"""
    lats = (45.524118,)
    lngs = (-122.683982,)
    result = findAddress(lats, lngs)

    assert result is not None
    assert len(result) == 1
    assert not pd.isna(result['address'][0])
    assert result['status_code'][0] == 200
    print("✓ test_coordinates_UP PASSED")


def test_coordinates_unequal():
    """Test findAddress with unequal lengths"""
    lats = (40.7128, 48.8584)
    lngs = (-74.0060,)
    result = findAddress(lats, lngs)

    assert result is None
    print("✓ test_coordinates_unequal PASSED")


def test_mlb_parks_reverse():
    """Test findAddress with MLB park coordinates"""
    # Yankee Stadium and Fenway Park
    lats = (40.829, 42.345)
    lngs = (-73.926, -71.098)
    result = findAddress(lats, lngs)

    assert result is not None
    assert len(result) == 2
    assert all(result['status_code'] == 200)
    print("✓ test_mlb_parks_reverse PASSED")


def test_non_tuple():
    """Test findAddress with list converted to tuple"""
    lats_list = [40.7128, 48.8584]
    lngs_list = [-74.0060, 2.2945]
    result = findAddress(tuple(lats_list), tuple(lngs_list))

    assert result is not None
    assert len(result) == 2
    print("✓ test_non_tuple PASSED")


def test_state_capitols_reverse():
    """Test findAddress with state capitol coordinates"""
    # Salem, OR and Richmond, VA
    lats = (44.9429, 37.5407)
    lngs = (-123.0351, -77.4360)
    result = findAddress(lats, lngs)

    assert result is not None
    assert len(result) == 2
    assert all(result['status_code'] == 200)
    print("✓ test_state_capitols_reverse PASSED")


def run_all_tests():
    """Run all unit tests"""
    print("=" * 80)
    print("Running Unit Tests")
    print("=" * 80)
    print()

    tests = [
        ("findCoordinates Tests", [
            test_address_UP,
            test_address_invalid,
            test_mlb_parks,
            test_state_capitols
        ]),
        ("findAddress Tests", [
            test_coordinates_UP,
            test_coordinates_unequal,
            test_mlb_parks_reverse,
            test_non_tuple,
            test_state_capitols_reverse
        ])
    ]

    passed = 0
    failed = 0

    for category, test_list in tests:
        print(f"\n{category}:")
        print("-" * 80)
        for test in test_list:
            try:
                test()
                passed += 1
            except AssertionError as e:
                print(f"✗ {test.__name__} FAILED: {e}")
                failed += 1
            except Exception as e:
                print(f"✗ {test.__name__} ERROR: {str(e)}")
                failed += 1

    print()
    print("=" * 80)
    print(f"Results: {passed} passed, {failed} failed out of {passed + failed} tests")
    print("=" * 80)

    return failed == 0


if __name__ == "__main__":
    run_all_tests()