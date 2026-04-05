import pytest
import sys
from datetime import datetime


if __name__ == "__main__":
    print("=" * 40)
    print("PET STORE API - TEST REPORT")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 40)
    result = pytest.main([
        "test_api.py",
        "-v",
        "--tb=short"
    ])

    print("\n" + "=" * 40)
    if result == 0:
        print("ALL TESTS PASSED")
    else:
        print("SOME TESTS FAILED")
    print("=" * 40)

    sys.exit(result)