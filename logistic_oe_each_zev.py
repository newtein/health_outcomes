import os
from constants import *
from config import CONFIG
import sys
from logistic_oe import OddsRatio


if __name__ == "__main__":
    years = [int(i) for i in sys.argv[1:]]
    CONFIG.update({"analysis_years": years})

    for state_code in ZEV_STATES:
        try:
            obj = OddsRatio(state_code=state_code, pop_type='CHILD', write_file=False, identifier=state_code)
            obj.get_results()
        except Exception as e:
            print("Error with state {}".format(state_code), e)