import os
from constants import *
from config import CONFIG
import sys
from logistic_oe import OddsRatio


if __name__ == "__main__":
    state_lookup = {
        6: list(range(2012, 2016)),
        9: list(range(2010, 2017)),
        24: list(range(2010, 2015)),
        34: list(range(2010, 2016)),
        36: [2012],
        41: list(range(2010, 2016)),
        44: [2010, 2013, 2014, 2015],
        50: list(range(2010, 2016))
    }
    use_smote = True
    for state_code in ZEV_STATES:
        # for urban_cluster in [1,2,3]:
        # try:
            years = state_lookup.get(state_code)
            CONFIG.update({"analysis_years": years})
            identifier = "{}".format(state_code)
            # identifier = "{}_urban_{}".format(state_code, urban_cluster)
            # other_filters ={
            #     "MSCODE": urban_cluster
            # }
            obj = OddsRatio(state_code=state_code, pop_type='CHILD', write_file=False, identifier=identifier, use_smote=use_smote)
            obj.get_results()

        # except Exception as e:
        #     print("Error with state {}".format(state_code), e)