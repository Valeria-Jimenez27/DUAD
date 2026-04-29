import pytest
import sys
import os
from datetime import datetime

BASE_DIR = os.path.dirname(__file__)

if __name__ == "__main__":
    print("=" * 40)
    print("PET STORE API - TEST REPORT")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 40)
    result = pytest.main([os.path.join(BASE_DIR, "tests", "test_api.py"), "-v", "--tb=short"])

    print("\n" + "=" * 40)
    if result == 0:
        print("ALL TESTS PASSED")
    else:
        print("SOME TESTS FAILED")
    print("=" * 40)

    sys.exit(result)