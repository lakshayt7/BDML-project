import Span
import parse_cpt

import pandas as pd
import sys

if __name__ == "__main__":
    fname = sys.argv[-1]
    spans = parse_cpt.parse_dir(fname)
    print(len(spans))