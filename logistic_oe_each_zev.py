import os
from constants import *
from config import CONFIG
import sys
from logistic_oe import OddsRatio


if __name__ == "__main__":
    years = [int(i) for i in sys.argv[1:]]
    CONFIG.update({"analysis_years": years})

    for state_code in ZEV_STATES:
        for urban_cluster in [1,2,3]:
            try:
                identifier = "{}_urban_{}".format(state_code, urban_cluster)
                other_filters ={
                    "MSCODE": urban_cluster
                }
                obj = OddsRatio(state_code=state_code, pop_type='CHILD', write_file=False, identifier=identifier,
                                other_filters=other_filters)
                obj.get_results()
            except Exception as e:
                print("Error with state {}".format(state_code), e)