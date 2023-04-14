# This is a helper script to run src/invoiced/main.py.

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'src'))
from invoiced.main import main

if __name__ == "__main__":
    main()
