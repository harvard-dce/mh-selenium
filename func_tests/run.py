
import os
import sys
import pytest

here = os.path.abspath(os.path.dirname(__file__))

if __name__ == '__main__':
    sys.argv.extend(['-x', here])
    sys.exit(pytest.main(sys.argv))
